import csv
import os
import shutil
import tempfile
from typing import Dict, Tuple, Optional


class WinPredictor:
    """
    Lightweight, dependency-free predictor using empirical probabilities from
    `cricket_match_results.csv

    Assumptions:
    - Column names: Date, ENG, NZ, Winner, GameID
    - ENG string like "16 for 1" is England's super over total; NZ likewise.
    - In the historical dataset, England bats first and New Zealand chases.
    """

    def __init__(self, results_csv_path: str = "cricket_match_results.csv") -> None:
        self.results_csv_path: str = results_csv_path
        self._loaded: bool = False

        # Aggregates
        self.total_matches: int = 0
        self.total_eng_wins: int = 0
        self.total_nz_wins: int = 0

        # By first-innings score buckets (runs only)
        self.count_by_eng_runs: Dict[int, int] = {}
        self.eng_wins_by_eng_runs: Dict[int, int] = {}
        self.nz_wins_by_eng_runs: Dict[int, int] = {}

        # Also keep per NZ runs when NZ bats first in future (not used now but generic)
        self.count_by_nz_runs: Dict[int, int] = {}
        self.nz_wins_by_nz_runs: Dict[int, int] = {}
        self.eng_wins_by_nz_runs: Dict[int, int] = {}

    @staticmethod
    def _parse_runs_wkts(s: str) -> Optional[Tuple[int, int]]:
        if not s:
            return None
        try:
            # Formats seen: "16 for 1", may have spaces
            parts = s.strip().split(" for ")
            if len(parts) != 2:
                return None
            runs = int(parts[0].strip())
            wkts = int(parts[1].strip())
            return runs, wkts
        except Exception:
            return None

    @staticmethod
    def _is_england_win(winner: str) -> bool:
        if not winner:
            return False
        w = winner.strip().lower()
        return w.startswith("england")

    @staticmethod
    def _is_newzealand_win(winner: str) -> bool:
        if not winner:
            return False
        w = winner.strip().lower()
        return w.startswith("new zealand")

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        path = self.results_csv_path
        if not os.path.exists(path):
            # Keep gracefully usable even if file missing
            self._loaded = True
            return

        tmp_path = None
        try:
            fd, tmp_path = tempfile.mkstemp(prefix="winpred_", suffix=".csv")
            os.close(fd)
            shutil.copyfile(path, tmp_path)

            with open(tmp_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    eng = self._parse_runs_wkts(row.get("ENG", ""))
                    nz = self._parse_runs_wkts(row.get("NZ", ""))
                    winner = row.get("Winner", "")

                    if eng is None or nz is None:
                        continue

                    self.total_matches += 1

                    if self._is_england_win(winner):
                        self.total_eng_wins += 1
                    elif self._is_newzealand_win(winner):
                        self.total_nz_wins += 1

                    eng_runs = eng[0]
                    nz_runs = nz[0]

                    # By ENG runs
                    self.count_by_eng_runs[eng_runs] = self.count_by_eng_runs.get(eng_runs, 0) + 1
                    if self._is_england_win(winner):
                        self.eng_wins_by_eng_runs[eng_runs] = self.eng_wins_by_eng_runs.get(eng_runs, 0) + 1
                    elif self._is_newzealand_win(winner):
                        self.nz_wins_by_eng_runs[nz_runs if False else eng_runs] = self.nz_wins_by_eng_runs.get(eng_runs, 0) + 1

                    # By NZ runs (mirrors above; useful if NZ bats first in future)
                    self.count_by_nz_runs[nz_runs] = self.count_by_nz_runs.get(nz_runs, 0) + 1
                    if self._is_newzealand_win(winner):
                        self.nz_wins_by_nz_runs[nz_runs] = self.nz_wins_by_nz_runs.get(nz_runs, 0) + 1
                    elif self._is_england_win(winner):
                        self.eng_wins_by_nz_runs[eng_runs if False else nz_runs] = self.eng_wins_by_nz_runs.get(nz_runs, 0) + 1
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

        self._loaded = True

    # -------------------- Public API --------------------
    def predict_before_first(self, batting_first_team: str) -> float:
        """Return probability [0,1] that batting-first team wins before first ball.
        Uses overall win rates from historical data (England first innings).
        """
        self._ensure_loaded()
        if self.total_matches == 0:
            return 0.5

        eng_base = self.total_eng_wins / max(1, (self.total_eng_wins + self.total_nz_wins))
        if batting_first_team.strip().lower() == "england":
            return eng_base
        if batting_first_team.strip().lower() == "new zealand":
            return 1.0 - eng_base
        return 0.5

    def predict_before_second(self, first_innings_team: str, first_innings_runs: int, first_innings_wkts: int) -> Tuple[float, float]:
        """Return tuple (p_first_team_wins, p_second_team_wins) before second innings.
        Empirical: P(England wins | ENG_runs=r) if England batted first; otherwise
        P(New Zealand wins | NZ_runs=r) for NZ-first case.
        """
        self._ensure_loaded()

        def _safe_ratio(num: int, den: int) -> float:
            if den <= 0:
                return 0.5
            return max(0.0, min(1.0, num / den))

        team = first_innings_team.strip().lower()
        r = int(first_innings_runs)

        if team == "england":
            total = self.count_by_eng_runs.get(r, 0)
            e_w = self.eng_wins_by_eng_runs.get(r, 0)
            n_w = self.nz_wins_by_eng_runs.get(r, 0)
            if total == 0:
                # Fallback smoothing: look +/- 1 run, else use base rate
                for delta in (1, 2, 3):
                    total = self.count_by_eng_runs.get(r - delta, 0) + self.count_by_eng_runs.get(r + delta, 0)
                    e_w = self.eng_wins_by_eng_runs.get(r - delta, 0) + self.eng_wins_by_eng_runs.get(r + delta, 0)
                    n_w = self.nz_wins_by_eng_runs.get(r - delta, 0) + self.nz_wins_by_eng_runs.get(r + delta, 0)
                    if total > 0:
                        break
                if total == 0:
                    p_eng = self.total_eng_wins / max(1, (self.total_eng_wins + self.total_nz_wins))
                    return p_eng, 1.0 - p_eng
            p_eng = _safe_ratio(e_w, total)
            p_nz = _safe_ratio(n_w, total)
            # Normalize minor rounding
            s = p_eng + p_nz
            if s > 0:
                p_eng, p_nz = p_eng / s, p_nz / s
            return p_eng, p_nz

        if team == "new zealand":
            total = self.count_by_nz_runs.get(r, 0)
            n_w = self.nz_wins_by_nz_runs.get(r, 0)
            e_w = self.eng_wins_by_nz_runs.get(r, 0)
            if total == 0:
                for delta in (1, 2, 3):
                    total = self.count_by_nz_runs.get(r - delta, 0) + self.count_by_nz_runs.get(r + delta, 0)
                    n_w = self.nz_wins_by_nz_runs.get(r - delta, 0) + self.nz_wins_by_nz_runs.get(r + delta, 0)
                    e_w = self.eng_wins_by_nz_runs.get(r - delta, 0) + self.eng_wins_by_nz_runs.get(r + delta, 0)
                    if total > 0:
                        break
                if total == 0:
                    p_nz = self.total_nz_wins / max(1, (self.total_eng_wins + self.total_nz_wins))
                    return p_nz, 1.0 - p_nz
            p_nz = _safe_ratio(n_w, total)
            p_eng = _safe_ratio(e_w, total)
            s = p_eng + p_nz
            if s > 0:
                p_eng, p_nz = p_eng / s, p_nz / s
            return p_nz, p_eng

        # Unknown team label
        base = 0.5
        return base, 1.0 - base


