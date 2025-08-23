import os
import random
import time
import sys
import threading
import time
import csv
from datetime import datetime

'''
CRICKET GAME ENHANCEMENTS:
1. No Balls (+ Free hit )
2. Wides ( + Byes ) ✓ IMPLEMENTED
3. More dismissals ✓ IMPLEMENTED (Bowled, Caught, LBW, Run-out)
4. More commentary ✓ ENHANCED
5. Tied Super Over ✓ IMPLEMENTED
6. Byes and Legbyes
7. Dismissal types ( Run Outs , Catch etc ) ✓ IMPLEMENTED
8. Context-based probabilities ✓ IMPLEMENTED
9. Pressure-based aggression ✓ IMPLEMENTED
10. Strategic ball-by-ball aggression ✓ IMPLEMENTED
11. Dynamic first innings strategy ✓ IMPLEMENTED
12. Comprehensive second innings strategy ✓ IMPLEMENTED
'''



# GLOBAL PLAYER STATS AND TEAM CONFIGURATIONS
COMPLETE_PLAYER_STATS = {
    # ENGLAND FINALS XI
    "Jason Roy": {
        "strike_rate": 115.36, "batting_avg": 38.27, "boundary_pct": 42.1,
        "consistency": 6.5, "super_over_aggression": 9.5, "pressure_rating": 7.5,
        "bowling_economy": 0.0, "bowling_avg": 999, "wickets_per_match": 0.0,
        "super_over_threat": 2.0, "wicket_taking": 1.0, 
        "player_type": "batsman", "is_captain": False, "is_wicket_keeper": False
    },
    "Jonny Bairstow": {
        "strike_rate": 92.84, "batting_avg": 45.85, "boundary_pct": 38.2,
        "consistency": 7.5, "super_over_aggression": 8.5, "pressure_rating": 7.0,
        "bowling_economy": 0.0, "bowling_avg": 999, "wickets_per_match": 0.0,
        "super_over_threat": 2.0, "wicket_taking": 1.0, 
        "player_type": "batsman", "is_captain": False, "is_wicket_keeper": False
    },
    "Joe Root": {
        "strike_rate": 89.53, "batting_avg": 61.78, "boundary_pct": 28.4,
        "consistency": 9.0, "super_over_aggression": 7.0, "pressure_rating": 8.5,
        "bowling_economy": 0.0, "bowling_avg": 999, "wickets_per_match": 0.0,
        "super_over_threat": 2.0, "wicket_taking": 1.0, 
        "player_type": "batsman", "is_captain": False, "is_wicket_keeper": False
    },
    "Eoin Morgan": {
        "strike_rate": 111.08, "batting_avg": 42.29, "boundary_pct": 63.6,
        "consistency": 7.0, "super_over_aggression": 9.5, "pressure_rating": 9.5,
        "bowling_economy": 0.0, "bowling_avg": 999, "wickets_per_match": 0.0,
        "super_over_threat": 2.0, "wicket_taking": 1.0, 
        "player_type": "batsman", "is_captain": True, "is_wicket_keeper": False
    },
    "Ben Stokes": {
        "strike_rate": 93.19, "batting_avg": 66.43, "boundary_pct": 32.5,
        "consistency": 9.0, "super_over_aggression": 9.5, "pressure_rating": 10.0,
        "bowling_economy": 4.84, "bowling_avg": 40.71, "wickets_per_match": 0.64,
        "super_over_threat": 7.0, "wicket_taking": 6.5, 
        "player_type": "all_rounder", "is_captain": False, "is_wicket_keeper": False
    },
    "Jos Buttler": {
        "strike_rate": 122.83, "batting_avg": 34.67, "boundary_pct": 43.6,
        "consistency": 6.0, "super_over_aggression": 10.0, "pressure_rating": 8.5,
        "bowling_economy": 0.0, "bowling_avg": 999, "wickets_per_match": 0.0,
        "super_over_threat": 1.0, "wicket_taking": 0.5, 
        "player_type": "wicket_keeper", "is_captain": False, "is_wicket_keeper": True
    },
    "Chris Woakes": {
        "strike_rate": 95.45, "batting_avg": 35.5, "boundary_pct": 28.1,
        "consistency": 6.5, "super_over_aggression": 7.0, "pressure_rating": 8.0,
        "bowling_economy": 5.25, "bowling_avg": 27.88, "wickets_per_match": 1.45,
        "super_over_threat": 7.5, "wicket_taking": 7.0, 
        "player_type": "all_rounder", "is_captain": False, "is_wicket_keeper": False
    },
    "Liam Plunkett": {
        "strike_rate": 142.86, "batting_avg": 14.0, "boundary_pct": 60.0,
        "consistency": 2.0, "super_over_aggression": 6.0, "pressure_rating": 5.0,
        "bowling_economy": 4.86, "bowling_avg": 25.64, "wickets_per_match": 1.64,
        "super_over_threat": 8.0, "wicket_taking": 8.0, 
        "player_type": "bowler", "is_captain": False, "is_wicket_keeper": False
    },
    "Jofra Archer": {
        "strike_rate": 0.0, "batting_avg": 0.0, "boundary_pct": 0.0,
        "consistency": 1.0, "super_over_aggression": 3.0, "pressure_rating": 4.0,
        "bowling_economy": 4.57, "bowling_avg": 23.05, "wickets_per_match": 1.82,
        "super_over_threat": 9.5, "wicket_taking": 9.0, 
        "player_type": "bowler", "is_captain": False, "is_wicket_keeper": False
    },
    "Adil Rashid": {
        "strike_rate": 95.24, "batting_avg": 10.0, "boundary_pct": 40.0,
        "consistency": 2.0, "super_over_aggression": 5.0, "pressure_rating": 4.5,
        "bowling_economy": 5.72, "bowling_avg": 32.18, "wickets_per_match": 1.36,
        "super_over_threat": 6.0, "wicket_taking": 6.5, 
        "player_type": "bowler", "is_captain": False, "is_wicket_keeper": False
    },
    "Mark Wood": {
        "strike_rate": 0.0, "batting_avg": 0.0, "boundary_pct": 0.0,
        "consistency": 1.0, "super_over_aggression": 4.0, "pressure_rating": 5.0,
        "bowling_economy": 5.27, "bowling_avg": 31.33, "wickets_per_match": 1.0,
        "super_over_threat": 6.5, "wicket_taking": 6.0, 
        "player_type": "bowler", "is_captain": False, "is_wicket_keeper": False
    },

    # NEW ZEALAND FINALS XI
    "Martin Guptill": {
        "strike_rate": 84.16, "batting_avg": 20.67, "boundary_pct": 45.2,
        "consistency": 3.5, "super_over_aggression": 8.0, "pressure_rating": 6.0,
        "bowling_economy": 0.0, "bowling_avg": 999, "wickets_per_match": 0.0,
        "super_over_threat": 2.0, "wicket_taking": 1.0, 
        "player_type": "batsman", "is_captain": False, "is_wicket_keeper": False
    },
    "Henry Nicholls": {
        "strike_rate": 78.95, "batting_avg": 33.67, "boundary_pct": 28.1,
        "consistency": 6.0, "super_over_aggression": 6.5, "pressure_rating": 7.0,
        "bowling_economy": 0.0, "bowling_avg": 999, "wickets_per_match": 0.0,
        "super_over_threat": 2.0, "wicket_taking": 1.0, 
        "player_type": "batsman", "is_captain": False, "is_wicket_keeper": False
    },
    "Kane Williamson": {
        "strike_rate": 74.97, "batting_avg": 82.57, "boundary_pct": 37.7,
        "consistency": 9.5, "super_over_aggression": 7.5, "pressure_rating": 9.5,
        "bowling_economy": 0.0, "bowling_avg": 999, "wickets_per_match": 0.0,
        "super_over_threat": 2.0, "wicket_taking": 1.0, 
        "player_type": "batsman", "is_captain": True, "is_wicket_keeper": False
    },
    "Ross Taylor": {
        "strike_rate": 75.27, "batting_avg": 46.4, "boundary_pct": 35.8,
        "consistency": 8.0, "super_over_aggression": 7.0, "pressure_rating": 8.0,
        "bowling_economy": 0.0, "bowling_avg": 999, "wickets_per_match": 0.0,
        "super_over_threat": 2.0, "wicket_taking": 1.0, 
        "player_type": "batsman", "is_captain": False, "is_wicket_keeper": False
    },
    "Tom Latham": {
        "strike_rate": 68.18, "batting_avg": 29.5, "boundary_pct": 25.4,
        "consistency": 6.5, "super_over_aggression": 5.5, "pressure_rating": 7.5,
        "bowling_economy": 0.0, "bowling_avg": 999, "wickets_per_match": 0.0,
        "super_over_threat": 1.5, "wicket_taking": 1.0, 
        "player_type": "wicket_keeper", "is_captain": False, "is_wicket_keeper": True
    },
    "James Neesham": {
        "strike_rate": 78.91, "batting_avg": 33.14, "boundary_pct": 40.5,
        "consistency": 6.0, "super_over_aggression": 8.5, "pressure_rating": 8.0,
        "bowling_economy": 5.36, "bowling_avg": 25.33, "wickets_per_match": 1.67,
        "super_over_threat": 8.0, "wicket_taking": 8.5, 
        "player_type": "all_rounder", "is_captain": False, "is_wicket_keeper": False
    },
    "Colin de Grandhomme": {
        "strike_rate": 94.74, "batting_avg": 35.0, "boundary_pct": 42.1,
        "consistency": 5.5, "super_over_aggression": 7.5, "pressure_rating": 7.0,
        "bowling_economy": 4.16, "bowling_avg": 35.5, "wickets_per_match": 1.0,
        "super_over_threat": 6.5, "wicket_taking": 5.5, 
        "player_type": "all_rounder", "is_captain": False, "is_wicket_keeper": False
    },
    "Mitchell Santner": {
        "strike_rate": 84.62, "batting_avg": 13.0, "boundary_pct": 30.8,
        "consistency": 3.0, "super_over_aggression": 6.0, "pressure_rating": 6.0,
        "bowling_economy": 5.24, "bowling_avg": 51.0, "wickets_per_match": 0.8,
        "super_over_threat": 5.0, "wicket_taking": 4.0, 
        "player_type": "bowler", "is_captain": False, "is_wicket_keeper": False
    },
    "Matt Henry": {
        "strike_rate": 0.0, "batting_avg": 0.0, "boundary_pct": 0.0,
        "consistency": 1.0, "super_over_aggression": 3.0, "pressure_rating": 4.0,
        "bowling_economy": 5.68, "bowling_avg": 35.0, "wickets_per_match": 1.0,
        "super_over_threat": 6.0, "wicket_taking": 5.5, 
        "player_type": "bowler", "is_captain": False, "is_wicket_keeper": False
    },
    "Trent Boult": {
        "strike_rate": 85.71, "batting_avg": 6.0, "boundary_pct": 50.0,
        "consistency": 1.5, "super_over_aggression": 5.0, "pressure_rating": 4.0,
        "bowling_economy": 4.84, "bowling_avg": 28.18, "wickets_per_match": 1.7,
        "super_over_threat": 9.0, "wicket_taking": 8.5, 
        "player_type": "bowler", "is_captain": False, "is_wicket_keeper": False
    },
    "Lockie Ferguson": {
        "strike_rate": 66.67, "batting_avg": 4.0, "boundary_pct": 100.0,
        "consistency": 1.0, "super_over_aggression": 4.0, "pressure_rating": 3.0,
        "bowling_economy": 4.89, "bowling_avg": 19.48, "wickets_per_match": 2.33,
        "super_over_threat": 9.5, "wicket_taking": 9.5, 
        "player_type": "bowler", "is_captain": False, "is_wicket_keeper": False
    }
}

# Team configurations
TEAM_CONFIGS = {
    "England": {
        "captain": "Eoin Morgan",
        "default_keeper": "Jos Buttler",
        "finals_xi": ["Jason Roy", "Jonny Bairstow", "Joe Root", "Eoin Morgan", 
                     "Ben Stokes", "Jos Buttler", "Chris Woakes", "Liam Plunkett",
                     "Jofra Archer", "Adil Rashid", "Mark Wood"]
    },
    "New Zealand": {
        "captain": "Kane Williamson", 
        "default_keeper": "Tom Latham",
        "finals_xi": ["Martin Guptill", "Henry Nicholls", "Kane Williamson", "Ross Taylor",
                     "Tom Latham", "James Neesham", "Colin de Grandhomme", "Mitchell Santner",
                     "Matt Henry", "Trent Boult", "Lockie Ferguson"]
    }
}


FAST_AUTOPLAY = False  # Default value

if len(sys.argv) > 1:
    if sys.argv[1].lower() in ['true', '1', 'yes', 'y', 'fast', 'auto']:
        FAST_AUTOPLAY = True
        print("🚀 FAST AUTOPLAY MODE ENABLED via command line!")
    elif sys.argv[1].lower() in ['false', '0', 'no', 'n', 'normal']:
        FAST_AUTOPLAY = False
        print("🎮 NORMAL MODE ENABLED via command line!")
    else:
        print(f"⚠️ Unknown parameter '{sys.argv[1]}'. Using default: NORMAL MODE")
        print("Valid options: true/false, 1/0, yes/no, y/n, fast/normal, auto")

def smart_sleep(seconds):
    """Sleep only if not in fast autoplay mode"""
    if not FAST_AUTOPLAY:
        time.sleep(seconds)

def log_match_result(eng_score, eng_wickets, nz_score, nz_wickets, winner):
    
    """Log match result to CSV file with simple format: Date,ENG,NZ,Winner"""
    full_timestamp = int(time.time() * 1000)  # Current time in milliseconds
    game_id = full_timestamp % 10000000  # Get last 7 digits (modulo 10,000,000)

    # Create the match result data (date/time when CSV is written)
    match_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    eng_result = f"{eng_score} for {eng_wickets}"
    nz_result = f"{nz_score} for {nz_wickets}"
    
    # Prepare the row data
    match_data = [match_date, eng_result, nz_result, winner,game_id]
    
    # File name for the CSV
    csv_filename = "cricket_match_results.csv"
    
    try:
        # Check if file exists to determine if we need headers
        file_exists = False
        try:
            with open(csv_filename, 'r') as f:
                file_exists = True
        except FileNotFoundError:
            file_exists = False
        
        # Write to CSV file
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header if file is new
            if not file_exists:
                writer.writerow(['Date', 'ENG', 'NZ', 'Winner','Game_ID'])
                print(f"\n📊 Created new match results file: {csv_filename}")
            
            # Write the match data
            writer.writerow(match_data)
            print(f"📊 Match result logged: {match_date} | ENG: {eng_result} | NZ: {nz_result} | Winner: {winner} | Game_ID: {game_id}")
            
    except Exception as e:
        print(f"⚠️ Error logging match result: {e}")
        print("Match will continue, but result won't be saved to file.")


def display_batting_team_for_selection(role_name, selected_batsmen_choices=None):
    """Display batting team with clear indicators for already selected players"""
    global batting_team_squad, Batting_Team_Name, innings
    
    if selected_batsmen_choices is None:
        selected_batsmen_choices = []
    
    print("\n" + "="*80)
    print(f"🏏 INNINGS {innings} - {role_name.upper()} SELECTION")
    print(f"🏏 {Batting_Team_Name.upper()} BATTING SQUAD")
    print("="*80)
    
    for player_no in range(len(batting_team_squad)):
        player_name = batting_team_squad[player_no]
        player_stats = COMPLETE_PLAYER_STATS.get(player_name, {})
        choice_number = player_no + 1
        
        # Get player info
        player_type = player_stats.get("player_type", "unknown")
        is_captain = player_stats.get("is_captain", False)
        is_keeper = player_stats.get("is_wicket_keeper", False)
        
        # Create status indicators
        status = ""
        if is_captain:
            status += " (C)"
        if is_keeper:
            status += " (WK)"
        if player_type == "all_rounder":
            status += " (AR)"
        elif player_type == "bowler":
            status += " (BWL)"
        elif player_type == "batsman":
            status += " (BAT)"
        
        # Check if player is already selected
        if choice_number in selected_batsmen_choices:
            # Find which role this player was selected for
            role_selected = ""
            if len(selected_batsmen_choices) >= 1 and choice_number == selected_batsmen_choices[0]:
                role_selected = "STRIKE BATSMAN"
            elif len(selected_batsmen_choices) >= 2 and choice_number == selected_batsmen_choices[1]:
                role_selected = "NON-STRIKE BATSMAN"
            else:
                role_selected = "SELECTED"
            
            # Display with cross (unavailable)
            print(f"❌ {choice_number:2d}. {player_name:<20} {status} - ALREADY CHOSEN AS {role_selected}")
        else:
            # Available for selection - show with tick
            recommendation = ""
            if player_type == "batsman":
                recommendation = " ⭐ RECOMMENDED"
            elif player_type == "all_rounder":
                recommendation = " 💡 GOOD OPTION"
            elif player_type == "bowler":
                recommendation = " ❓ UNUSUAL CHOICE"
            
            print(f"✅ {choice_number:2d}. {player_name:<20} {status}{recommendation}")
    
    print("="*80)
    print("Legend: (C) = Captain, (WK) = Wicket Keeper, (AR) = All Rounder")
    print("        (BAT) = Batsman, (BWL) = Bowler")
    print("✅ = Available for selection | ❌ = Already selected")
    print("⭐ = Best choice | 💡 = Good choice | ❓ = Unusual choice")
    print("="*80)

def display_bowling_team_for_selection():
    """Display bowling team for bowler selection"""
    global bowling_team_squad, Bowling_Team_Name, innings
    
    print("\n" + "="*80)
    print(f"🏏 INNINGS {innings} - SUPER OVER BOWLER SELECTION")
    print(f"🏏 {Bowling_Team_Name.upper()} BOWLING SQUAD")
    print("="*80)
    
    for player_no in range(len(bowling_team_squad)):
        player_name = bowling_team_squad[player_no]
        player_stats = COMPLETE_PLAYER_STATS.get(player_name, {})
        
        # Get player info
        player_type = player_stats.get("player_type", "unknown")
        is_captain = player_stats.get("is_captain", False)
        is_keeper = player_stats.get("is_wicket_keeper", False)
        
        # Create status indicators
        status = ""
        if is_captain:
            status += " (C)"
        if is_keeper:
            status += " (WK)"
        if player_type == "all_rounder":
            status += " (AR)"
        elif player_type == "bowler":
            status += " (BWL)"
        elif player_type == "batsman":
            status += " (BAT)"
        
        # Add bowling recommendation
        recommendation = ""
        if player_type == "bowler":
            recommendation = " ⭐ RECOMMENDED"
        elif player_type == "all_rounder":
            recommendation = " 💡 GOOD OPTION"
        elif is_keeper:
            recommendation = " ⚠️ WICKET-KEEPER (will need replacement)"
        else:
            recommendation = " ❓ UNUSUAL CHOICE"
        
        # All bowlers are available (no crosses needed)
        print(f"✅ {player_no + 1:2d}. {player_name:<20} {status}{recommendation}")
    
    print("="*80)
    print("Legend: (C) = Captain, (WK) = Wicket Keeper, (AR) = All Rounder")
    print("        (BAT) = Batsman, (BWL) = Bowler")
    print("⭐ = Best choice | 💡 = Good choice | ⚠️ = Special consideration | ❓ = Unusual")
    print("="*80)


def validate_user_choice_with_display(role_name, team_name, selected_batsmen_choices=None):
    """Enhanced validation with timer that properly handles invalid inputs"""
    global user_choice
    
    choice_accepted = False
    
    while not choice_accepted:
        try:
            # Show appropriate display based on role
            if "Bowler" in role_name:
                display_bowling_team_for_selection()
                max_choice = len(bowling_team_squad)
                
                # Get suggested bowler (first bowler in list)
                suggested_choice = 1
                for i, player in enumerate(bowling_team_squad):
                    player_stats = COMPLETE_PLAYER_STATS.get(player, {})
                    if player_stats.get("player_type") == "bowler":
                        suggested_choice = i + 1
                        break
                
                player_name = bowling_team_squad[suggested_choice - 1]
                print(f"\n💡 Our suggestion: Option {suggested_choice} - {player_name}")
                
            else:
                # For batsmen, show batting team with selection indicators
                display_batting_team_for_selection(role_name, selected_batsmen_choices or [])
                max_choice = len(batting_team_squad)
                
                # Get suggested batsman (first available batsman)
                suggested_choice = 1
                excluded_choices = selected_batsmen_choices or []
                
                for i, player in enumerate(batting_team_squad):
                    if (i + 1) not in excluded_choices:
                        player_stats = COMPLETE_PLAYER_STATS.get(player, {})
                        if player_stats.get("player_type") in ["batsman", "all_rounder"]:
                            suggested_choice = i + 1
                            break
                
                # If no batsman found, find any available player
                if suggested_choice in excluded_choices:
                    for i in range(len(batting_team_squad)):
                        if (i + 1) not in excluded_choices:
                            suggested_choice = i + 1
                            break
                
                player_name = batting_team_squad[suggested_choice - 1]
                print(f"\n💡 Our suggestion: Option {suggested_choice} - {player_name}")
            
            # FIXED TIMER INPUT - Reset for each attempt
            user_choice = universal_timed_input(
                f"\nSelect {role_name} for {team_name} (1-{max_choice}) [Auto-select in 15s]: ",
                timeout=15,
                default_value=suggested_choice,
                input_type="number"
            )
            
            # Validate the choice
            if 1 <= user_choice <= max_choice:
                # For batsmen, check if already selected
                if "Bowler" not in role_name and selected_batsmen_choices and user_choice in selected_batsmen_choices:
                    print(f"\n❌ ERROR: Player {user_choice} already selected! Please choose a different player.")
                    print("⏰ Restarting selection in 3 seconds...")
                    smart_sleep(3)
                    # Continue the loop - timer will reset for next attempt
                    continue
                else:
                    choice_accepted = True
                    selected_player = batting_team_squad[user_choice - 1] if "Bowler" not in role_name else bowling_team_squad[user_choice - 1]
                    print(f"\n✅ Valid selection: {user_choice} - {selected_player}")
            else:
                print(f"\n❌ ERROR: Invalid choice {user_choice}! Please enter a number between 1 and {max_choice}")
                print("⏰ Restarting selection in 3 seconds...")
                smart_sleep(3)
                # Continue the loop - timer will reset for next attempt
                
        except (ValueError, TypeError):
            print(f"\n❌ ERROR: Invalid input! Please enter a valid number between 1 and {max_choice}")
            print("⏰ Restarting selection in 3 seconds...")
            smart_sleep(3)
            # Continue the loop - timer will reset for next attempt
        except KeyboardInterrupt:
            print(f"\n\n🚫 Game interrupted by user. Exiting...")
            sys.exit()

def team_diplay():
    """Initialize team squads based on innings"""
    global batting_team_squad, bowling_team_squad, Batting_Team_Name, Bowling_Team_Name
    
    # Use team configurations from TEAM_CONFIGS
    if innings == 1:
        # First innings: England bats, New Zealand bowls
        Batting_Team_Name = 'England'
        Bowling_Team_Name = 'New Zealand'
        batting_team_squad = TEAM_CONFIGS["England"]["finals_xi"].copy()
        bowling_team_squad = TEAM_CONFIGS["New Zealand"]["finals_xi"].copy()
    else:
        # Second innings: New Zealand bats, England bowls
        Batting_Team_Name = 'New Zealand'
        Bowling_Team_Name = 'England'
        batting_team_squad = TEAM_CONFIGS["New Zealand"]["finals_xi"].copy()
        bowling_team_squad = TEAM_CONFIGS["England"]["finals_xi"].copy()

    # Just show a brief header - detailed display will be handled by selection functions
    print("\n" + "="*100)
    print("CRICKET WORLD CUP 2019 FINAL - SUPER OVER".center(100))
    print("="*100)
    print(f"\n🏏 INNINGS {innings}: {Batting_Team_Name.upper()} BATTING vs {Bowling_Team_Name.upper()} BOWLING")
    print("="*100)
def display_batting_team_for_selection(role_name, selected_batsmen_choices=None):
    """Display batting team with clear indicators and unique player suggestions"""
    global batting_team_squad, Batting_Team_Name, innings
    
    if selected_batsmen_choices is None:
        selected_batsmen_choices = []
    
    print("\n" + "="*80)
    print(f"🏏 INNINGS {innings} - {role_name.upper()} SELECTION")
    print(f"🏏 {Batting_Team_Name.upper()} BATTING SQUAD")
    print("="*80)
    
    for player_no in range(len(batting_team_squad)):
        player_name = batting_team_squad[player_no]
        player_stats = COMPLETE_PLAYER_STATS.get(player_name, {})
        choice_number = player_no + 1
        
        # Get player info
        player_type = player_stats.get("player_type", "unknown")
        is_captain = player_stats.get("is_captain", False)
        is_keeper = player_stats.get("is_wicket_keeper", False)
        
        # Create status indicators
        status = ""
        if is_captain:
            status += " (C)"
        if is_keeper:
            status += " (WK)"
        if player_type == "all_rounder":
            status += " (AR)"
        elif player_type == "bowler":
            status += " (BWL)"
        elif player_type == "batsman":
            status += " (BAT)"
        
        # Check if player is already selected
        if choice_number in selected_batsmen_choices:
            # Find which role this player was selected for
            role_selected = ""
            if len(selected_batsmen_choices) >= 1 and choice_number == selected_batsmen_choices[0]:
                role_selected = "STRIKE BATSMAN"
            elif len(selected_batsmen_choices) >= 2 and choice_number == selected_batsmen_choices[1]:
                role_selected = "NON-STRIKE BATSMAN"
            else:
                role_selected = "SELECTED"
            
            # Display with cross (unavailable) - use the space for role info
            print(f"❌ {choice_number:2d}. {player_name:<20} {status:<15} - {role_selected}")
        else:
            # Available for selection - show unique suggestion for this player
            suggestion = get_unique_player_suggestion(player_name, role_name)
            print(f"✅ {choice_number:2d}. {player_name:<20} {status:<15} - {suggestion}")
    
    print("="*80)
    print("Legend: (C) = Captain, (WK) = Wicket Keeper, (AR) = All Rounder")
    print("        (BAT) = Batsman, (BWL) = Bowler")
    print("✅ = Available for selection | ❌ = Already selected")
    print("="*80)



def display_bowling_team_for_selection():
    """Display bowling team with unique suggestions for each bowler"""
    global bowling_team_squad, Bowling_Team_Name, innings
    
    print("\n" + "="*80)
    print(f"🏏 INNINGS {innings} - SUPER OVER BOWLER SELECTION")
    print(f"🏏 {Bowling_Team_Name.upper()} BOWLING SQUAD")
    print("="*80)
    
    for player_no in range(len(bowling_team_squad)):
        player_name = bowling_team_squad[player_no]
        player_stats = COMPLETE_PLAYER_STATS.get(player_name, {})
        
        # Get player info
        player_type = player_stats.get("player_type", "unknown")
        is_captain = player_stats.get("is_captain", False)
        is_keeper = player_stats.get("is_wicket_keeper", False)
        
        # Create status indicators
        status = ""
        if is_captain:
            status += " (C)"
        if is_keeper:
            status += " (WK)"
        if player_type == "all_rounder":
            status += " (AR)"
        elif player_type == "bowler":
            status += " (BWL)"
        elif player_type == "batsman":
            status += " (BAT)"
        
        # Get unique suggestion for this bowler
        suggestion = get_unique_bowler_suggestion(player_name)
        
        # All bowlers are available (no crosses needed)
        print(f"✅ {player_no + 1:2d}. {player_name:<20} {status:<15} - {suggestion}")
    
    print("="*80)
    print("Legend: (C) = Captain, (WK) = Wicket Keeper, (AR) = All Rounder")
    print("        (BAT) = Batsman, (BWL) = Bowler")
    print("✅ = Available for selection | ❌ = Already selected")
    print("="*80)

def get_unique_player_suggestion(player_name, role_name):
    """Get unique, specific suggestion for each player based on their real strengths"""
    player_stats = COMPLETE_PLAYER_STATS.get(player_name, {})
    
    # England players
    if player_name == "Jason Roy":
        if "striker" in role_name.lower():
            return "⭐ PERFECT - Explosive opener, ideal for strike"
        else:
            return "💡 GOOD - Aggressive style suits any batting role"
    
    elif player_name == "Jonny Bairstow":
        if "striker" in role_name.lower():
            return "⭐ EXCELLENT - Fearless aggressor, loves pressure"
        else:
            return "💡 SOLID - Reliable under pressure"
    
    elif player_name == "Joe Root":
        if "non" in role_name.lower():
            return "⭐ IDEAL - Master of singles, perfect anchor"
        elif "third" in role_name.lower():
            return "💡 RELIABLE - Calm finisher, rarely panics"
        else:
            return "💡 DEPENDABLE - Technique to handle any situation"
    
    elif player_name == "Eoin Morgan":
        if "third" in role_name.lower():
            return "⭐ CAPTAIN'S CHOICE - Ultimate finisher, ice-cool"
        else:
            return "💡 LEADER - Captain's experience invaluable"
    
    elif player_name == "Ben Stokes":
        if "third" in role_name.lower():
            return "⭐ MATCH-WINNER - Thrives in do-or-die moments"
        else:
            return "💡 HERO - Can turn impossible into possible"
    
    elif player_name == "Jos Buttler":
        if "striker" in role_name.lower():
            return "⭐ DESTROYER - 360° shots, can hit anywhere"
        elif "third" in role_name.lower():
            return "⭐ FINISHER - Best death-over batsman in world"
        else:
            return "💡 GENIUS - Innovative shots, game-changer"
    
    elif player_name == "Chris Woakes":
        return "⚠️ UNUSUAL - Bowler first, limited batting ability"
    
    elif player_name == "Liam Plunkett":
        return "⚠️ RISKY - Tail-ender, very limited batting"
    
    elif player_name == "Jofra Archer":
        return "⚠️ TAIL-ENDER - Can hit big but very risky"
    
    elif player_name == "Adil Rashid":
        return "⚠️ BOWLER - Minimal batting skills"
    
    elif player_name == "Mark Wood":
        return "⚠️ LAST RESORT - Pure bowler, can't bat"
    
    # New Zealand players
    elif player_name == "Martin Guptill":
        if "striker" in role_name.lower():
            return "⭐ PERFECT - Big-hitting opener, ideal choice"
        else:
            return "💡 POWER - Can clear boundaries easily"
    
    elif player_name == "Henry Nicholls":
        if "non" in role_name.lower():
            return "⭐ ANCHOR - Steady accumulator, perfect support"
        else:
            return "💡 RELIABLE - Solid technique, rarely fails"
    
    elif player_name == "Kane Williamson":
        if "non" in role_name.lower():
            return "⭐ CAPTAIN'S CLASS - Master of timing and placement"
        elif "third" in role_name.lower():
            return "⭐ GENIUS - Best finisher in NZ, never panics"
        else:
            return "💡 WORLD-CLASS - Captain's calm under pressure"
    
    elif player_name == "Ross Taylor":
        if "third" in role_name.lower():
            return "⭐ VETERAN - 20 years experience, clutch performer"
        else:
            return "💡 EXPERIENCED - Knows how to handle pressure"
    
    elif player_name == "Tom Latham":
        if "non" in role_name.lower():
            return "💡 KEEPER-BATSMAN - Solid technique, good support"
        else:
            return "💡 DEPENDABLE - Wicket-keeper with batting skills"
    
    elif player_name == "James Neesham":
        if "striker" in role_name.lower():
            return "💡 ALL-ROUNDER - Can hit big, good strike rate"
        elif "third" in role_name.lower():
            return "⭐ POWER-HITTER - Loves the big moments"
        else:
            return "💡 VERSATILE - All-rounder, can adapt to any role"
    
    elif player_name == "Colin de Grandhomme":
        if "third" in role_name.lower():
            return "💡 BIG-HITTER - Can clear boundaries when needed"
        else:
            return "💡 ALL-ROUNDER - Useful batting option"
    
    elif player_name == "Mitchell Santner":
        return "⚠️ BOWLER FIRST - Limited batting, risky choice"
    
    elif player_name == "Matt Henry":
        return "⚠️ TAIL-ENDER - Pure bowler, minimal batting"
    
    elif player_name == "Trent Boult":
        return "⚠️ BOWLER - Can swing hard but very risky"
    
    elif player_name == "Lockie Ferguson":
        return "⚠️ LAST RESORT - Fast bowler, can't bat"
    
    # Default fallback
    return "💡 Available for selection"

def get_unique_bowler_suggestion(player_name):
    """Get unique, specific bowling suggestion for each player"""
    
    # England bowlers
    if player_name == "Jofra Archer":
        return "⭐ PACE DEMON - 95mph+ thunderbolts, intimidating"
    
    elif player_name == "Mark Wood":
        return "⭐ EXPRESS PACE - Fastest in squad, 97mph missiles"
    
    elif player_name == "Chris Woakes":
        return "⭐ SWING MASTER - Perfect line & length, reliable"
    
    elif player_name == "Liam Plunkett":
        return "💡 DEATH SPECIALIST - Slower balls, hard to hit"
    
    elif player_name == "Adil Rashid":
        return "💡 SPIN WIZARD - Leg-spin variations, unpredictable"
    
    elif player_name == "Ben Stokes":
        return "💡 ALL-ROUNDER - Medium pace, can surprise batsmen"
    
    elif player_name == "Joe Root":
        return "⚠️ PART-TIME - Occasional off-spin, emergency option"
    
    elif player_name == "Eoin Morgan":
        return "⚠️ CAPTAIN ONLY - No bowling skills, leadership"
    
    elif player_name == "Jos Buttler":
        return "⚠️ KEEPER ISSUE - Would need replacement keeper"
    
    elif player_name == "Jason Roy":
        return "⚠️ BATSMAN - No bowling ability whatsoever"
    
    elif player_name == "Jonny Bairstow":
        return "⚠️ BATSMAN - No bowling skills at all"
    
    # New Zealand bowlers
    elif player_name == "Trent Boult":
        return "⭐ SWING KING - Left-arm magic, deadly accurate"
    
    elif player_name == "Lockie Ferguson":
        return "⭐ SPEED MACHINE - 95mph+ rockets, aggressive"
    
    elif player_name == "Matt Henry":
        return "💡 SEAM BOWLER - Consistent line, good variations"
    
    elif player_name == "Mitchell Santner":
        return "💡 LEFT-ARM SPIN - Tight lines, economical"
    
    elif player_name == "James Neesham":
        return "💡 MEDIUM PACE - All-rounder, useful option"
    
    elif player_name == "Colin de Grandhomme":
        return "💡 SWING BOWLER - Medium pace, can move ball"
    
    elif player_name == "Kane Williamson":
        return "⚠️ PART-TIME - Occasional off-spin, captain first"
    
    elif player_name == "Ross Taylor":
        return "⚠️ BATSMAN - No bowling ability, pure batsman"
    
    elif player_name == "Tom Latham":
        return "⚠️ KEEPER ISSUE - Would need replacement keeper"
    
    elif player_name == "Martin Guptill":
        return "⚠️ BATSMAN - No bowling skills whatsoever"
    
    elif player_name == "Henry Nicholls":
        return "⚠️ BATSMAN - No bowling ability at all"
    
    # Default fallback
    return "💡 Available for selection"


def universal_timed_input(prompt, timeout=20, default_value=1, input_type="number", excluded_choices=None):
    """Simplified timed input with proper countdown"""
    if FAST_AUTOPLAY:
        timeout=0
    if excluded_choices is None:
        excluded_choices = []
    
    print(prompt)
    print(f"⏰ You have {timeout} seconds to decide (or we'll pick option {default_value} for you)")
    
    user_input = [None]  # Use list to make it mutable in nested function
    result = [None]  # Use list to make it mutable in nested function
    def get_input():
        try:
            user_input = input(prompt).strip()
            if user_input == "":
                result[0] = default_value
            else:
                if input_type == "number":
                    result[0] = int(user_input)
                else:
                    result[0] = user_input
        except (ValueError, EOFError):
            result[0] = default_value
        except KeyboardInterrupt:
            result[0] = "INTERRUPT"
    
    # Start input thread
    input_thread = threading.Thread(target=get_input)
    input_thread.daemon = True
    input_thread.start()
    
    # Wait for input or timeout
    input_thread.join(timeout)
    
    if input_thread.is_alive():
        # Timeout occurred
        print(f"\n⏰ Time's up! Auto-selecting: {default_value}")
        result[0] = default_value
    
    if result[0] == "INTERRUPT":
        raise KeyboardInterrupt
    
    return result[0] if result[0] is not None else default_value

def timed_yes_no_input(prompt, timeout=15, default_value='y'):
    if FAST_AUTOPLAY:
        timeout=0
    """Timed yes/no input for game restart"""
    try:
        response = universal_timed_input(
            f"\n{prompt}\nType Y or y for Yes, any other key for No [Auto-restart in {timeout}s]: ",
            timeout=timeout,
            default_value=default_value,
            input_type="string"
        )
        return str(response).lower() == 'y'
    except KeyboardInterrupt:
        print(f"\n\n🚫 Game interrupted by user. Exiting...")
        sys.exit()

def get_smart_default(team_name, role_key, excluded_choices):
    """Get smart default suggestion for player selection"""
    team_config = TEAM_CONFIGS.get(team_name, {})
    smart_defaults = team_config.get("smart_defaults", {})
    
    # Get the suggested choice for this role
    suggested_choice = smart_defaults.get(role_key, 1)
    
    # If suggested choice is already selected, find next best option
    if suggested_choice in excluded_choices:
        # Find alternative based on role type
        alternatives = smart_defaults.get(f"{role_key}_alternatives", [])
        for alt in alternatives:
            if alt not in excluded_choices:
                return alt
        
        # If no alternatives, find any available choice
        for i in range(1, 12):
            if i not in excluded_choices:
                return i
    
    return suggested_choice

def get_player_name_from_choice(choice, team_type):
    """Get player name from choice number"""
    if team_type == "batting":
        if 1 <= choice <= len(batting_team_squad):
            return batting_team_squad[choice - 1]
    else:
        if 1 <= choice <= len(bowling_team_squad):
            return bowling_team_squad[choice - 1]
    return "Unknown Player"
def get_suggestion_reason(team_name, role_key, player_name):
    """Get reason for the suggestion"""
    player_stats = COMPLETE_PLAYER_STATS.get(player_name, {})
    player_type = player_stats.get("player_type", "unknown")
    is_captain = player_stats.get("is_captain", False)
    is_keeper = player_stats.get("is_wicket_keeper", False)
    
    if "striker" in role_key.lower():
        return "Aggressive opener, good for strike rotation"
    elif "non_striker" in role_key.lower():
        return "Solid technique, reliable partner"
    elif "third" in role_key.lower():
        return "Finisher, can handle pressure"
    elif "bowler" in role_key.lower():
        if player_type == "bowler":
            return "Specialist bowler, best option"
        elif player_type == "all_rounder":
            return "All-rounder, good bowling option"
        else:
            return "Can bowl if needed"
    
    return "Good choice for this role"
# Enhanced validation with smart suggestions
def validate_user_choice_with_suggestions(role_name, team_name, selected_choices=None):
    """Enhanced validation with helpful suggestions"""
    global user_choice
    global team_display_ind
    
    if selected_choices is None:
        selected_choices = []
    
    choice_accepted = False
    
    while not choice_accepted:
        if team_display_ind != "N":
            team_diplay()
        
        # FIXED: Better role key mapping
        role_key = role_name.lower()
        
        if "striker end" in role_key:
            role_key = "striker"
            team_type = "batting"
        elif "non striker end" in role_key or "non-striker end" in role_key:
            role_key = "non_striker"
            team_type = "batting"
        elif "third" in role_key:
            role_key = "third"
            team_type = "batting"
        elif "bowler" in role_key:
            role_key = "bowler"
            team_type = "bowling"
        elif "keeper" in role_key:
            role_key = "keeper"
            team_type = "bowling"
        else:
            role_key = "third"
            team_type = "batting"
        
        smart_suggestion = get_smart_default(team_name, role_key, selected_choices)
        player_name = get_player_name_from_choice(smart_suggestion, team_type)
        reason = get_suggestion_reason(team_name, role_key, player_name)
        
        # Enhanced prompt with player name and reason in one line
        prompt_text = f"\nSelect your {role_name} for {team_name}:\n💡 Our suggestion: Option {smart_suggestion} - {player_name} - {reason}"
        
        user_choice = universal_timed_input(
            prompt_text,
            timeout=20,
            default_value=smart_suggestion,
            input_type="number",
            excluded_choices=selected_choices
        )
        
        if 1 <= user_choice <= 11:
            if user_choice in selected_choices:
                print(f'\n❌ {role_name} already selected, let us suggest another option...')
                continue
            choice_accepted = True
        else:
            print('❌ Invalid choice, let us help you pick again...')
def get_delivery_outcome(balls_remaining, runs_needed=0, recent_runs=0, balls_since_boundary=0, wickets_in_hand=0, recent_balls_runs=[], current_total=0, wicket_fell_last_ball=False, boundary_this_over=False, innings=1, current_batsman="Unknown", current_bowler="Unknown"):
    """    BALANCED strategy - making both innings competitive
    """
    base_weights = {
        0: 25,  # Dot ball
        1: 30,  # Single
        2: 15,  # Two runs
        3: 8,   # Three runs
        4: 12,  # Four runs
        5: 8,   # Wicket
        6: 7,   # Six runs
        7: 5    # Wide
    }


    if innings == 1:  # England batting first
        # Make it slightly harder to score big
        base_weights[4] = 10  # Reduce boundaries
        base_weights[6] = 5   # Reduce sixes
        base_weights[5] = 10  # Increase wicket chance
        base_weights[0] = 28  # Increase dots
    else:  # New Zealand chasing
        # Make it slightly easier to chase
        base_weights[4] = 14  # Increase boundaries
        base_weights[6] = 9   # Increase sixes
        base_weights[5] = 6   # Reduce wicket chance
        base_weights[0] = 22  # Reduce dots

    
    # Copy base weights to modify
    outcome_weights = base_weights.copy()

    
    if innings == 1:  # FIRST INNINGS - BALANCED AGGRESSION
        
        if balls_remaining == 6:  # BALL 1 - Solid start
            print("(Ball 1 - Solid start, set the tone)")
            outcome_weights[1] += 8   # Good singles
            outcome_weights[4] += 6   # Some boundaries
            outcome_weights[6] += 4   # Limited big shots
            
        elif balls_remaining == 5:  # BALL 2 - Build momentum
            print("(Ball 2 - Build momentum)")
            outcome_weights[4] += 10  # More boundaries
            outcome_weights[6] += 6   # Some sixes
            outcome_weights[1] += 6   # Value singles
                
        elif balls_remaining == 4:  # BALL 3 - Acceleration
            print("(Ball 3 - Acceleration phase)")
            outcome_weights[4] += 12  # Good boundaries
            outcome_weights[6] += 8   # Some big shots
            outcome_weights[1] += 5   # Still value singles
                
        elif balls_remaining == 3:  # BALL 4 - Power phase
            print("(Ball 4 - Power phase)")
            outcome_weights[4] += 15  # High boundary chance
            outcome_weights[6] += 12  # Good six chance
            outcome_weights[5] += 2   # Accept some risk
                
        elif balls_remaining == 2:  # BALL 5 - Launch mode
            print("(Ball 5 - Launch mode)")
            outcome_weights[4] += 16  # High boundary chance
            outcome_weights[6] += 15  # High six chance
            outcome_weights[5] += 3   # Accept risk
                
        elif balls_remaining == 1:  # BALL 6 - Final assault
            print("(Ball 6 - Final assault)")
            outcome_weights[4] += 18  # Very high boundary chance
            outcome_weights[6] += 20  # Very high six chance
            outcome_weights[5] += 4   # Accept high risk
            outcome_weights[0] = 8    # Some dots still possible
            
    
    else:  # SECOND INNINGS - PERFECTLY BALANCED CHASING
        print("(Second innings - chasing with realistic pressure)")
        
        # MINIMAL base pressure - just enough to be realistic
        outcome_weights[5] += 1   # Tiny pressure increase
        outcome_weights[0] += 1   # Tiny dot ball increase
        
        # TARGET ASSESSMENT - REALISTIC AND BALANCED
        if runs_needed <= 0:  # Already won
            print("(Target achieved! Play safe)")
            outcome_weights[1] += 20
            outcome_weights[0] += 15
            outcome_weights[5] -= 5
            
        elif runs_needed <= 4:  # VERY LOW TARGET - Should win easily
            print("(Very low target - easy chase)")
            outcome_weights[1] += 12  # More singles
            outcome_weights[4] += 5   # Some boundaries
            outcome_weights[5] += 0   # NO extra pressure
            outcome_weights[0] += 0   # NO extra dots
            
        elif runs_needed <= 8:  # LOW TARGET - Comfortable
            print("(Low target - comfortable chase)")
            outcome_weights[1] += 8   # Good singles
            outcome_weights[4] += 8   # Good boundaries
            outcome_weights[5] += 1   # Minimal pressure
            outcome_weights[0] += 1   # Minimal extra dots
            
        elif runs_needed <= 12:  # MEDIUM TARGET - Balanced
            print("(Medium target - balanced approach)")
            outcome_weights[1] += 5   # Some singles
            outcome_weights[4] += 10  # Good boundaries
            outcome_weights[6] += 5   # Some sixes
            outcome_weights[5] += 2   # Moderate pressure
            outcome_weights[0] += 2   # Moderate extra dots
            
        elif runs_needed <= 16:  # HIGH TARGET - Need aggression
            print("(High target - aggressive approach")
            outcome_weights[4] += 12  # More boundaries
            outcome_weights[6] += 12  # More sixes
            outcome_weights[5] += 3   # Some pressure
            outcome_weights[0] += 1   # Slight extra dots
            
        elif runs_needed <= 20:  # VERY HIGH TARGET - Go big
            print("(Very high target - big shots needed)")
            outcome_weights[4] += 15  # Many boundaries
            outcome_weights[6] += 18  # Many sixes
            outcome_weights[5] += 4   # Higher pressure
            outcome_weights[0] += 0   # NO extra dots (can't afford)
            
        else:  # EXTREMELY HIGH TARGET - Desperate but possible
            print("(Extremely high target - desperate measures)")
            outcome_weights[6] += 22  # Maximum sixes
            outcome_weights[4] += 18  # Maximum boundaries
            outcome_weights[5] += 6   # High pressure
            outcome_weights[0] = 8    # Some dots due to pressure
            outcome_weights[1] = 5    # Minimal singles
        
        # BALLS REMAINING PRESSURE - VERY CONSERVATIVE
        if balls_remaining <= 1:  # Last ball only
            print(f"(Last ball - final chance)")
            outcome_weights[5] += 2   # Moderate final ball pressure
            outcome_weights[0] += 1   # Slight extra dots
            
        elif balls_remaining <= 3:  # Last 3 balls
            print(f"(Last {balls_remaining} balls - crunch time)")
            outcome_weights[5] += 1   # Minimal pressure
            outcome_weights[0] += 1   # Minimal extra dots

    batsman_form_today = random.uniform(1, 10)
    bowler_form_today = random.uniform(1, 10)
    
    print(f"(Today's form: {current_batsman} {batsman_form_today:.1f}/10, {current_bowler} {bowler_form_today:.1f}/10)")
    
    # BATSMAN HAVING AN OFF DAY
    if batsman_form_today < 3.0:  # Really struggling today
        print(f"({current_batsman} is having a terrible day - struggling badly!)")
        outcome_weights[0] += 12  # Many more dots
        outcome_weights[5] += 8   # Much higher wicket chance
        outcome_weights[4] -= 8   # Far fewer boundaries
        outcome_weights[6] -= 10  # Far fewer sixes
        outcome_weights[1] -= 3   # Fewer singles
        
    elif batsman_form_today < 5.0:  # Below par performance
        print(f"({current_batsman} is below par today - not timing well)")
        outcome_weights[0] += 6   # More dots
        outcome_weights[5] += 4   # Higher wicket chance
        outcome_weights[4] -= 4   # Fewer boundaries
        outcome_weights[6] -= 5   # Fewer sixes
        
    elif batsman_form_today > 8.5:  # Exceptional day
        print(f"({current_batsman} is in sublime form today - everything is coming off!)")
        outcome_weights[4] += 12  # Many more boundaries
        outcome_weights[6] += 15  # Many more sixes
        outcome_weights[0] -= 6   # Far fewer dots
        outcome_weights[5] -= 4   # Lower wicket chance
        outcome_weights[1] += 5   # More singles
        
    elif batsman_form_today > 7.0:  # Good day
        print(f"({current_batsman} is timing the ball well today)")
        outcome_weights[4] += 6   # More boundaries
        outcome_weights[6] += 8   # More sixes
        outcome_weights[0] -= 3   # Fewer dots
        outcome_weights[5] -= 2   # Slightly lower wicket chance
    
    # BOWLER HAVING AN OFF DAY
    if bowler_form_today < 3.0:  # Really struggling today
        print(f"({current_bowler} is having a nightmare - can't find his line!)")
        outcome_weights[4] += 15  # Batsman gets many boundaries
        outcome_weights[6] += 18  # Batsman gets many sixes
        outcome_weights[7] += 8   # Many wides
        outcome_weights[0] -= 8   # Far fewer dots
        outcome_weights[5] -= 6   # Much lower wicket chance
        
    elif bowler_form_today < 5.0:  # Below par bowling
        print(f"({current_bowler} is struggling with his rhythm today)")
        outcome_weights[4] += 8   # More boundaries conceded
        outcome_weights[6] += 10  # More sixes conceded
        outcome_weights[7] += 4   # More wides
        outcome_weights[0] -= 4   # Fewer dots
        outcome_weights[5] -= 3   # Lower wicket chance
        
    elif bowler_form_today > 8.5:  # Exceptional bowling day
        print(f"({current_bowler} is unplayable today - everything is working!)")
        outcome_weights[0] += 15  # Many more dots
        outcome_weights[5] += 10  # Much higher wicket chance
        outcome_weights[4] -= 10  # Far fewer boundaries
        outcome_weights[6] -= 12  # Far fewer sixes
        outcome_weights[1] += 3   # Restrict to singles
        outcome_weights[7] -= 3   # Fewer wides
        
    elif bowler_form_today > 7.0:  # Good bowling day
        print(f"({current_bowler} has his radar working perfectly today)")
        outcome_weights[0] += 8   # More dots
        outcome_weights[5] += 5   # Higher wicket chance
        outcome_weights[4] -= 5   # Fewer boundaries
        outcome_weights[6] -= 6   # Fewer sixes
        outcome_weights[7] -= 2   # Fewer wides
    
    # PRESSURE MOMENTS - Random mental strength
    if innings == 2 and balls_remaining <= 3:  # High pressure situation
        mental_strength_batsman = random.uniform(1, 10)
        mental_strength_bowler = random.uniform(1, 10)
        
        print(f"(Pressure moment: {current_batsman} mental {mental_strength_batsman:.1f}/10, {current_bowler} mental {mental_strength_bowler:.1f}/10)")
        
        if mental_strength_batsman < 4.0:  # Batsman crumbles under pressure
            print(f"({current_batsman} is feeling the pressure - nerves showing!)")
            outcome_weights[5] += 8   # Much higher wicket chance
            outcome_weights[0] += 6   # More dots due to nerves
            
        elif mental_strength_batsman > 8.0:  # Batsman thrives under pressure
            print(f"({current_batsman} thrives under pressure - ice in the veins!)")
            outcome_weights[4] += 10  # More boundaries under pressure
            outcome_weights[6] += 12  # More sixes under pressure
            outcome_weights[5] -= 3   # Lower wicket chance
            
        if mental_strength_bowler < 4.0:  # Bowler crumbles under pressure
            print(f"({current_bowler} is feeling the heat - losing composure!)")
            outcome_weights[7] += 6   # More wides due to nerves
            outcome_weights[4] += 8   # More boundaries due to poor bowling
            outcome_weights[5] -= 4   # Lower wicket chance
            
        elif mental_strength_bowler > 8.0:  # Bowler excels under pressure
            print(f"({current_bowler} loves the big moments - pressure brings out his best!)")
            outcome_weights[5] += 8   # Higher wicket chance
            outcome_weights[0] += 6   # More dots under pressure
            outcome_weights[4] -= 5   # Fewer boundaries
    
    # MATCH SITUATION RANDOMNESS
    match_momentum = random.uniform(1, 10)
    
    if match_momentum < 3.0:  # Everything going wrong
        print("(Nothing is going right - one of those days!)")
        if innings == 1:  # Batting team struggling
            outcome_weights[0] += 8
            outcome_weights[5] += 5
        else:  # Chasing team struggling
            outcome_weights[5] += 6
            outcome_weights[0] += 6
            
    elif match_momentum > 8.0:  # Everything clicking
        print("(Everything is clicking perfectly - magic in the air!)")
        if innings == 1:  # Batting team flying
            outcome_weights[4] += 10
            outcome_weights[6] += 12
            outcome_weights[0] -= 4
        else:  # Chasing team in the zone
            outcome_weights[4] += 8
            outcome_weights[6] += 10
            outcome_weights[5] -= 3
    
    # CROWD FACTOR (Random crowd influence)
    crowd_factor = random.uniform(1, 10)
    
    if crowd_factor > 8.5:  # Crowd going wild
        print("(The crowd is going absolutely wild - electric atmosphere!)")
        if innings == 2:  # More impact when chasing
            outcome_weights[4] += 5  # Crowd lifts the batsman
            outcome_weights[6] += 6  # Big shots get the crowd going
            outcome_weights[5] -= 2  # Crowd support reduces pressure
    
    elif crowd_factor < 2.5:  # Tense silence
        print("(Pin-drop silence in the stadium - you can cut the tension!)")
        if innings == 2:  # More pressure when chasing
            outcome_weights[5] += 4  # Silence increases pressure
            outcome_weights[0] += 4  # Tension causes hesitation

    # Ensure no negative weights
    for key in outcome_weights:
        outcome_weights[key] = max(1, outcome_weights[key])
    
    # Create weighted list for random selection
    weighted_outcomes = []
    for outcome, weight in outcome_weights.items():
        weighted_outcomes.extend([outcome] * weight)
    
    return random.choice(weighted_outcomes)

def handle_wicket_keeper_selection(team_name, selected_bowler):
    """Handle wicket-keeper replacement if keeper is selected to bowl"""
    team_config = TEAM_CONFIGS[team_name]
    default_keeper = team_config["default_keeper"]
    finals_xi = team_config["finals_xi"]
    
    # Check if selected bowler is the wicket-keeper
    bowler_stats = COMPLETE_PLAYER_STATS.get(selected_bowler, {})
    is_keeper = bowler_stats.get("is_wicket_keeper", False)
    
    if is_keeper:
        print(f"\n⚠️  WARNING: {selected_bowler} is the wicket-keeper!")
        print("A wicket-keeper must be on the field at all times.")
        
        # Show remaining 10 players from Finals XI
        remaining_players = [player for player in finals_xi if player != selected_bowler]
        
        print(f"\nSelect ANY player from {team_name} Finals XI to keep wickets:")
        print("="*70)
        for i, player in enumerate(remaining_players, 1):
            player_type = COMPLETE_PLAYER_STATS.get(player, {}).get("player_type", "unknown")
            
            if player_type == "wicket_keeper":
                suggestion = " (⭐ Natural wicket-keeper)"
            elif player_type == "all_rounder":
                suggestion = " (💡 Good option - all-rounder)"
            elif player_type == "batsman":
                suggestion = " (⚠️  Batsman - can keep if needed)"
            else:
                suggestion = " (❌ Bowler - unusual choice but allowed)"
                
            print(f"{i:2d}. {player:<20} {suggestion}")
        
        print("="*70)
        print(f"💡 Suggestion: Choose a batsman or all-rounder for better keeping")
        print(f"🎮 Your choice: You can pick ANY of these {len(remaining_players)} players!")
        
        while True:
            try:
                choice = input(f"\nSelect replacement keeper (1-{len(remaining_players)}): ")
                replacement_keeper = remaining_players[int(choice) - 1]
                
                keeper_type = COMPLETE_PLAYER_STATS.get(replacement_keeper, {}).get("player_type", "unknown")
                
                print(f"\n🎯 You selected: {replacement_keeper} ({keeper_type})")
                
                if keeper_type == "bowler":
                    print("⚠️  Note: This is a bowler - unusual choice for keeping!")
                elif keeper_type == "wicket_keeper":
                    print("⭐ Excellent choice - natural wicket-keeper!")
                elif keeper_type == "all_rounder":
                    print("💡 Good choice - all-rounders often keep wickets!")
                else:
                    print("✅ Acceptable choice - batsmen can keep wickets!")
                
                confirm = input(f"\nConfirm {replacement_keeper} as wicket-keeper? (Y/N): ")
                if confirm.lower() == 'y':
                    print(f"\n✅ {replacement_keeper} will keep wickets for this Super Over")
                    print(f"✅ {selected_bowler} will bowl the Super Over")
                    return replacement_keeper
                else:
                    print("Please select again...")
                    
            except (ValueError, IndexError):
                print("❌ Invalid choice! Please enter a valid number.")
    
    return default_keeper


def Diff_in_Days(date1, date2):
    """Calculate difference in days between two dates"""
    return (date2 - date1).days

def get_all_values(dictionary):
    """Extract all values from nested dictionary structure"""
    all_values = []
    for value in dictionary.values():
        all_values.extend(value)
    return all_values

def delivery_loading():
    """Display loading animation for delivery"""
    loading = True
    loading_speed = 1
    loading_string = "." * 6
    
    while loading:
        for index, char in enumerate(loading_string):
            sys.stdout.write(char)
            sys.stdout.flush()
            smart_sleep(1.0 / loading_speed)
        index += 1
        sys.stdout.write("\b" * index + " " * index + "\b" * index)
        sys.stdout.flush()
        loading = False

def load_countdown():
    """Display countdown before innings starts"""
    count = 10
    global innings
    while (count >= 0):
        smart_sleep(1)
        if (count == 0):
            if (innings == 1):
                print("LET'S PLAY !!!! \n".center(100))
            else:
                print("GAME ON !!!!! \n".center(100))
        else:
            print("{}\n".format(count).center(100))
        count -= 1

def clear():
    """Clear the console screen"""
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def validate_user_choice(user_input):
    """Validate user input for player selection"""
    global user_choice
    choice_accepted = 'False'
    while (choice_accepted != 'True'):
        if (user_input >= 1 and user_input <= 11):
            if (batsmen_selection_done == False):
                if (user_input in selected_batsmen):
                    choice_accepted = 'False'
                    team_diplay()
                    user_input = int(input('\n Batsman Previously selected, Please retry\n'))
                else:
                    choice_accepted = 'True'
                    user_choice = user_input
            else:
                choice_accepted = 'True'
                user_choice = user_input
        else:
            team_diplay()
            user_input = int(input('\n Incorrect Choice entered, Please retry\n'))

def validate_user_choice_new(role_name, team_name):
    """Enhanced validation with proper team displays and timeout"""
    global user_choice
    
    choice_accepted = False
    
    while not choice_accepted:
        try:
            # Show appropriate display based on role
            if "Bowler" in role_name:
                display_bowling_team_for_selection()
                max_choice = len(bowling_team_squad)
                
                # Get suggested bowler (first bowler in list)
                suggested_choice = 1
                for i, player in enumerate(bowling_team_squad):
                    player_stats = COMPLETE_PLAYER_STATS.get(player, {})
                    if player_stats.get("player_type") == "bowler":
                        suggested_choice = i + 1
                        break
                
                player_name = get_player_name_from_choice(suggested_choice, "bowling")
                reason = get_suggestion_reason(team_name, "bowler", player_name)
                
                prompt_text = f"\n💡 Our suggestion: Option {suggested_choice} - {player_name} - {reason}"
                
                user_choice = universal_timed_input(
                    prompt_text,
                    timeout=20,
                    default_value=suggested_choice,
                    input_type="number"
                )
            else:
                # For batsmen, show batting team with selection indicators
                display_batting_team_for_selection(role_name, selected_batsmen)
                max_choice = len(batting_team_squad)
                
                # Get suggested batsman (first available batsman)
                suggested_choice = 1
                for i, player in enumerate(batting_team_squad):
                    if (i + 1) not in selected_batsmen:
                        player_stats = COMPLETE_PLAYER_STATS.get(player, {})
                        if player_stats.get("player_type") in ["batsman", "all_rounder"]:
                            suggested_choice = i + 1
                            break
                
                # If no batsman found, find any available player
                if suggested_choice in selected_batsmen:
                    for i in range(len(batting_team_squad)):
                        if (i + 1) not in selected_batsmen:
                            suggested_choice = i + 1
                            break
                
                player_name = get_player_name_from_choice(suggested_choice, "batting")
                reason = get_suggestion_reason(team_name, role_name.lower(), player_name)
                
                prompt_text = f"\n💡 Our suggestion: Option {suggested_choice} - {player_name} - {reason}"
                
                user_choice = universal_timed_input(
                    prompt_text,
                    timeout=20,
                    default_value=suggested_choice,
                    input_type="number",
                    excluded_choices=selected_batsmen
                )
            
            # Validate the choice
            if 1 <= user_choice <= max_choice:
                # For batsmen, check if already selected
                if "Bowler" not in role_name and user_choice in selected_batsmen:
                    print(f"\n❌ ERROR: Player already selected! Please choose a different player.")
                    smart_sleep(2)
                    continue
                else:
                    choice_accepted = True
                    print(f"\n✅ Valid selection: {user_choice}")
            else:
                print(f"\n❌ ERROR: Please enter a number between 1 and {max_choice}")
                smart_sleep(2)
                
        except (ValueError, TypeError):
            print(f"\n❌ ERROR: Please enter a valid number between 1 and {max_choice}")
            smart_sleep(2)

def team_diplay():
    """Display team squads for player selection"""
    global batting_team_squad
    global bowling_team_squad
    global Batting_Team_Name
    global Bowling_Team_Name
    
    # Use team configurations from TEAM_CONFIGS
    if innings == 1:
        # First innings: England bats, New Zealand bowls
        Batting_Team_Name = 'England'
        Bowling_Team_Name = 'New Zealand'
        batting_team_squad = TEAM_CONFIGS["England"]["finals_xi"].copy()
        bowling_team_squad = TEAM_CONFIGS["New Zealand"]["finals_xi"].copy()
    else:
        # Second innings: New Zealand bats, England bowls
        Batting_Team_Name = 'New Zealand'
        Bowling_Team_Name = 'England'
        batting_team_squad = TEAM_CONFIGS["New Zealand"]["finals_xi"].copy()
        bowling_team_squad = TEAM_CONFIGS["England"]["finals_xi"].copy()

    # ADD THIS DISPLAY LOGIC ⬇️⬇️⬇️
    print("\n" + "="*100)
    print("CRICKET WORLD CUP 2019 FINAL - SUPER OVER".center(100))
    print("="*100)
    
    print(f"\n🏏 INNINGS {innings} - TEAM SELECTION")
    print(f"🏏 {Batting_Team_Name.upper()} BATTING vs {Bowling_Team_Name.upper()} BOWLING")
    
    # Display batting team
    print(f"\n🏏 {Batting_Team_Name.upper()} SQUAD (Batting):")
    print("="*70)
    for player_no in range(len(batting_team_squad)):
        player_name = batting_team_squad[player_no]
        player_stats = COMPLETE_PLAYER_STATS.get(player_name, {})
        
        # Get player info
        player_type = player_stats.get("player_type", "unknown")
        is_captain = player_stats.get("is_captain", False)
        is_keeper = player_stats.get("is_wicket_keeper", False)
        
        # Create status indicators
        status = ""
        if is_captain:
            status += " (C)"
        if is_keeper:
            status += " (WK)"
        if player_type == "all_rounder":
            status += " (AR)"
        elif player_type == "bowler":
            status += " (BWL)"
        elif player_type == "batsman":
            status += " (BAT)"
            
        print(f"{player_no + 1:2d}. {player_name:<20} {status}")
    
    # Display bowling team  
    print(f"\n🏏 {Bowling_Team_Name.upper()} SQUAD (Bowling):")
    print("="*70)
    for player_no in range(len(bowling_team_squad)):
        player_name = bowling_team_squad[player_no]
        player_stats = COMPLETE_PLAYER_STATS.get(player_name, {})
        
        # Get player info
        player_type = player_stats.get("player_type", "unknown")
        is_captain = player_stats.get("is_captain", False)
        is_keeper = player_stats.get("is_wicket_keeper", False)
        
        # Create status indicators
        status = ""
        if is_captain:
            status += " (C)"
        if is_keeper:
            status += " (WK)"
        if player_type == "all_rounder":
            status += " (AR)"
        elif player_type == "bowler":
            status += " (BWL)"
        elif player_type == "batsman":
            status += " (BAT)"
            
        print(f"{player_no + 1:2d}. {player_name:<20} {status}")
    
    print("="*70)
    print("Legend: (C) = Captain, (WK) = Wicket Keeper, (AR) = All Rounder")
    print("        (BAT) = Batsman, (BWL) = Bowler")
    print("="*70)



def loading_screen():
    """Display game introduction and disclaimer"""
    clear()
    print("\n")
    print("\n***************************************************************************************Disclaimer ********************************************************************\n")
    print("\n\n\n")
    print("\nThis game was created solely for entertainment purposes using real Player names")
    print("\nThe game is a by Product undergoing the python learning\n")
    print("\nPlayer names are copyrighted Intellectual property (IP)  of New Zealand Cricket (NZC) , England and Wales Cricket Board (ECB) and  International Cricket Council (ICC)")
    print("\nCommercial use of this game is strictly prohibited and is discouraged and may invite Legal implications from the above mentioned parties\n")
    print("\nThe author bears no resonsiblity if any such incident does occurs in the future \n")

    print("\n\n\n")

    print("\nPlease send your Comments and Suggestions to")
    print("Anuj Puranik - anuj87in@gmail.com\n")

    print("\n***************************************************************************************XXXXXXXXXX ********************************************************************\n")

    smart_sleep(30)
    print("\nNow lets get started with the game\n")
    print("\n\n\n")
    delivery_loading()
    smart_sleep(2)
    clear()

# Initialize global variables
innings = 1
Target = 999999
user_choice = 0
team_display_ind = 'N'
batsmen_selection_done = True
selected_batsmen = []
batting_team_squad = []
bowling_team_squad = []
Batting_Team_Name = ''
Bowling_Team_Name = ''
first_innings_wickets = 0

# Start the game
loading_screen()

# Main game loop with proper restart logic
while True:
    Target = 999999  # Initialize target for first innings

    # Game introduction
    print("Welcome to the Cricket World Cup 2019 Finals\n"
          "\nIn an interesting turn of events after 50 Overs both teams stand equal in terms of runs Scored \n"
          "NZL batting first Scored 241/8 \t in reply ENG chasing got all out for 241 \n")

    smart_sleep(5)

    print('It is now time for the Super Over to break the tie in this Cricket World Cup 2019 Final \n')

    smart_sleep(5)

    innings = 1  # Start with first innings


    # Play both innings
    while (innings <= 2):

        smart_sleep(5)
        team_diplay()  # Initialize teams and show header
        team_display_ind = 'N'

        batsmen_selection_done = True
        # Player selection phase with optimized displays
        selected_batsmen = []

        # Strike Batsman Selection
        print("\n🏏 PLAYER SELECTION PHASE")
        print("=" * 50)
        
        validate_user_choice_with_display('Opening Batsmen at Striker End', Batting_Team_Name, selected_batsmen)
        strike_batsman = batting_team_squad[int(user_choice) - 1]
        print(f'\n✅ {strike_batsman} is chosen as the Strike Batsman for {Batting_Team_Name}')
        selected_batsmen.append(user_choice)
        batsmen_selection_done = False
        smart_sleep(2)

        # Non-Strike Batsman Selection  
        validate_user_choice_with_display('Opening Batsmen at Non Striker End', Batting_Team_Name, selected_batsmen)
        non_strike_batsman = batting_team_squad[int(user_choice) - 1]
        print(f'\n✅ {non_strike_batsman} is chosen as the Non-Strike Batsman for {Batting_Team_Name}')
        selected_batsmen.append(user_choice)
        smart_sleep(2)

        # Third Batsman Selection
        validate_user_choice_with_display('Third Batsmen', Batting_Team_Name, selected_batsmen)
        third_batsman = batting_team_squad[int(user_choice) - 1]
        print(f'\n✅ {third_batsman} is chosen as the Third Batsman for {Batting_Team_Name}')
        batsmen_selection_done = True
        selected_batsmen.clear()
        smart_sleep(2)

        # Bowler Selection
        print(f"\n🏏 Now selecting bowler for {Bowling_Team_Name}...")
        smart_sleep(1)
        
        while True:
            validate_user_choice_with_display('Opening Bowler', Bowling_Team_Name)
            selected_bowler = bowling_team_squad[int(user_choice) - 1]
            
            # Handle wicket-keeper scenario
            keeper_for_innings = handle_wicket_keeper_selection(Bowling_Team_Name, selected_bowler)
            
            if keeper_for_innings is not None:
                bowler_one_name = selected_bowler
                print(f"\n🏏 Super Over Setup Complete:")
                print(f"\n")
                print(f"✅ Strike Batsman: {strike_batsman}")
                print(f"✅ Non-Strike Batsman: {non_strike_batsman}")
                print(f"✅ Third Batsman: {third_batsman}")
                print(f"✅ Batting Team Captain: {TEAM_CONFIGS[Batting_Team_Name]['captain']} ")
                print(f"\n")
                print(f"✅ Bowler: {bowler_one_name}")
                print(f"✅ Wicket-keeper: {keeper_for_innings}")
                print(f"✅ Fielding Team Captain: {TEAM_CONFIGS[Bowling_Team_Name]['captain']} ")
                print(f"\n")
                smart_sleep(3)
                break
            else:
                print("❌ Please select a different bowler.")
                smart_sleep(2)

        # Initialize batting lineup
        batting_lineup = [
            strike_batsman,
            non_strike_batsman,
            third_batsman
        ]

        batsman_one_status = "*"
        batsman_two_status = "*"
        batsman_three_status = "DNB"

        print("Innings #{} of the Super Over coming up. \n".format(innings))
        smart_sleep(2)
        load_countdown()
        smart_sleep(2)

        print("{} Steaming in to bowl to {}\n".format(bowler_one_name, strike_batsman))

        # Initialize match variables
        batting_team_total_score = 0
        batsman_one_total_score = 0
        batsman_two_total_score = 0
        batsman_three_total_score = 0
        bowling_team_wickets = 0
        bowler_wickets = 0
        over_summary = []
        
        # Initialize tracking variables for strategy
        ball_no = 1
        balls_bowled = 0  # Track actual legal deliveries
        recent_balls_runs = []  # Track last 3 balls for pressure calculation
        balls_since_boundary = 0  # Track balls since last 4 or 6
        wicket_fell_last_ball = False  # Track if wicket fell on previous ball
        boundary_this_over = False     # Track if boundary hit this over
        # Main over loop - 6 legal deliveries

        # Add suspense before the first ball
        print("Here comes the first ball of the Super Over...")
        smart_sleep(2)
        delivery_loading()
        smart_sleep(1)

        while balls_bowled < 6 and bowling_team_wickets < 2:

            if innings == 2:
                runs_still_needed = Target - batting_team_total_score
                if balls_bowled == 0:
                    # First ball of second innings - only show target
                    print(f"\n🎯 Target to win: {Target} runs")
                else:
                    # Subsequent balls - show target and runs needed
                    if runs_still_needed > 0:
                        print(f"\n🎯 Target: {Target} | Need {runs_still_needed} more runs | {6-balls_bowled} balls remaining")
                    else:
                        print(f"\n🏆 Target achieved! {Batting_Team_Name} wins!")
            else:
                # First innings - just show balls remaining
                print(f"\n🏏 First innings | {6-balls_bowled} balls remaining")
            
            # Calculate strategy parameters
            balls_remaining = 6 - balls_bowled
            runs_needed = Target - batting_team_total_score if innings == 2 else 0
            recent_runs = sum(recent_balls_runs[-3:]) if len(recent_balls_runs) >= 3 else sum(recent_balls_runs)
            wickets_in_hand = 2 - bowling_team_wickets
            
            # Get delivery outcome based on strategy
            delivery_result = get_delivery_outcome(
                balls_remaining=balls_remaining,
                runs_needed=runs_needed,
                recent_runs=recent_runs,
                balls_since_boundary=balls_since_boundary,
                wickets_in_hand=wickets_in_hand,
                recent_balls_runs=recent_balls_runs,
                current_total=batting_team_total_score,
                wicket_fell_last_ball=wicket_fell_last_ball,
                boundary_this_over=boundary_this_over,
                innings=innings,
                current_batsman=strike_batsman,
                current_bowler=bowler_one_name
            )
            
            # Reset wicket flag
            wicket_fell_last_ball = False
            
            # Process delivery outcome
            if delivery_result == 0:  # Dot ball
                print("Ball {}: Dot ball! {} couldn't get it away.".format(ball_no, strike_batsman))
                balls_bowled += 1
                balls_since_boundary += 1
                recent_balls_runs.append(0)
                over_summary.append(".")  # Add dot ball to summary
                
            elif delivery_result == 1:  # Single
                print("Ball {}: Single! {} works it for one run.".format(ball_no, strike_batsman))
                batting_team_total_score += 1
                if strike_batsman == batting_lineup[0]:
                    batsman_one_total_score += 1
                elif strike_batsman == batting_lineup[1]:
                    batsman_two_total_score += 1
                else:
                    batsman_three_total_score += 1
                
                # Swap batsmen
                strike_batsman, non_strike_batsman = non_strike_batsman, strike_batsman
                balls_bowled += 1
                balls_since_boundary += 1
                recent_balls_runs.append(1)
                over_summary.append("1")  # Add single to summary
                
            elif delivery_result == 2:  # Two runs
                print("Ball {}: Two runs! {} finds the gap and comes back for the second.".format(ball_no, strike_batsman))
                batting_team_total_score += 2
                if strike_batsman == batting_lineup[0]:
                    batsman_one_total_score += 2
                elif strike_batsman == batting_lineup[1]:
                    batsman_two_total_score += 2
                else:
                    batsman_three_total_score += 2
                
                balls_bowled += 1
                balls_since_boundary += 1
                recent_balls_runs.append(2)
                over_summary.append("2")  # Add two runs to summary
                
            elif delivery_result == 3:  # Three runs
                print("Ball {}: Three runs! {} places it perfectly and they run hard for three.".format(ball_no, strike_batsman))
                batting_team_total_score += 3
                if strike_batsman == batting_lineup[0]:
                    batsman_one_total_score += 3
                elif strike_batsman == batting_lineup[1]:
                    batsman_two_total_score += 3
                else:
                    batsman_three_total_score += 3
                
                # Swap batsmen (odd number of runs)
                strike_batsman, non_strike_batsman = non_strike_batsman, strike_batsman
                balls_bowled += 1
                balls_since_boundary += 1
                recent_balls_runs.append(3)
                over_summary.append("3")  # Add three runs to summary
                
            elif delivery_result == 4:  # Four runs
                boundary_comments = [
                    "FOUR! {} finds the boundary with a cracking shot!",
                    "FOUR! Brilliant stroke from {} - that's raced to the fence!",
                    "FOUR! {} times it perfectly and it speeds away to the boundary!",
                    "FOUR! What a shot! {} sends it to the rope with authority!",
                    "FOUR! {} finds the gap and the ball races away for four!"
                ]
                print("Ball {}: {}".format(ball_no, random.choice(boundary_comments).format(strike_batsman)))
                
                batting_team_total_score += 4
                if strike_batsman == batting_lineup[0]:
                    batsman_one_total_score += 4
                elif strike_batsman == batting_lineup[1]:
                    batsman_two_total_score += 4
                else:
                    batsman_three_total_score += 4
                
                balls_bowled += 1
                balls_since_boundary = 0  # Reset boundary counter
                boundary_this_over = True
                recent_balls_runs.append(4)
                over_summary.append("4")  # Add four to summary
                
            elif delivery_result == 6:  # Six runs
                six_comments = [
                    "SIX! {} launches it into the stands! What a massive hit!",
                    "SIX! {} goes big and sends it sailing over the boundary!",
                    "SIX! Enormous hit from {} - that's gone way back into the crowd!",
                    "SIX! {} connects perfectly and it's gone all the way!",
                    "SIX! {} swings through the line and sends it into orbit!"
                ]
                print("Ball {}: {}".format(ball_no, random.choice(six_comments).format(strike_batsman)))
                
                batting_team_total_score += 6
                if strike_batsman == batting_lineup[0]:
                    batsman_one_total_score += 6
                elif strike_batsman == batting_lineup[1]:
                    batsman_two_total_score += 6
                else:
                    batsman_three_total_score += 6
                
                balls_bowled += 1
                balls_since_boundary = 0  # Reset boundary counter
                boundary_this_over = True
                recent_balls_runs.append(6)
                over_summary.append("6")  # Add six to summary
                
            elif delivery_result == 5:  # Wicket
                wicket_types = [
                    ("BOWLED! {} is clean bowled! The stumps are shattered!", True),
                    ("CAUGHT! {} holes out! Brilliant catch in the deep!", True),
                    ("LBW! {} is trapped in front! The finger goes up!", True),
                    ("RUN OUT! {} is short of his ground! Direct hit!", False)
                ]
                wicket_comment, bowler_gets_wicket = random.choice(wicket_types)
                print("Ball {}: {}".format(ball_no, wicket_comment.format(strike_batsman)))
                
                bowling_team_wickets += 1
                wicket_fell_last_ball = True

                # Track bowler's wickets separately (only for non-run-out dismissals)
                if bowler_gets_wicket:
                    bowler_wickets += 1
                
                # Update batsman status
                if strike_batsman == batting_lineup[0]:
                    batsman_one_status = "OUT"
                elif strike_batsman == batting_lineup[1]:
                    batsman_two_status = "OUT"
                else:
                    batsman_three_status = "OUT"
                
                balls_bowled += 1

                # Only bring in next batsman if there are more balls AND only 1 wicket has fallen
                if bowling_team_wickets == 1 and balls_bowled < 6:
                    # Bring in the third batsman
                    strike_batsman = batting_lineup[2]
                    batsman_three_status = "*"
                    print("{} comes to the crease.".format(strike_batsman))
                elif balls_bowled >= 6:
                    print("That's the end of the over!")
                # Note: If bowling_team_wickets == 2, the while loop will exit automatically
                
                balls_since_boundary += 1
                recent_balls_runs.append(0)  # Wicket counts as 0 runs for pressure calculation
                over_summary.append("W")
                
            elif delivery_result == 7:  # Wide
                wide_comments = [
                    "WIDE! {} strays down the leg side - that's an extra run!",
                    "WIDE! {} bowls it too wide outside off stump!",
                    "WIDE! {} loses his line and that's called wide!",
                    "WIDE! {} sprays it down the leg side - bonus run!"
                ]
                print("Ball {}: {}".format(ball_no, random.choice(wide_comments).format(bowler_one_name)))
                
                batting_team_total_score += 1
                #balls_since_boundary += 1
                # Wide doesn't count as a legal delivery, so balls_bowled doesn't increment
                # Don't add to recent_balls_runs as it's not a legal delivery
                over_summary.append("wd")  # Add wide to summary
                
            # Display current score after each delivery
            
            # Display current score after each delivery
            print("Score: {}/{} after {} balls".format(batting_team_total_score, bowling_team_wickets, balls_bowled))
            
            # Check for match-ending conditions in second innings
            match_ended = False
            if innings == 2:
                if batting_team_total_score >= Target:
                    print("\n🏆 TARGET ACHIEVED! {} WINS!".format(Batting_Team_Name))
                    print("\nWhat a finish! Let's see the final result...")
                    match_ended = True
                else:
                    # Only show target if match is still ongoing
                    runs_still_needed = Target - batting_team_total_score
                    print("🎯 Target: {} | Need {} more runs to win".format(Target, runs_still_needed))
            else:
                # First innings - check if over completed or all out
                if bowling_team_wickets >= 2:
                    print("\nAll out! {} is bowled out!".format(Batting_Team_Name))
                    match_ended = True
                elif balls_bowled >= 6:
                    print("\nOver completed!")
                    match_ended = True
            
            # Add suspense and delivery loading for match-ending scenarios
            if match_ended:
                smart_sleep(3)
                delivery_loading()
                smart_sleep(2)
                break
                
            # Keep only last 3 balls for pressure calculation
            if len(recent_balls_runs) > 3:
                recent_balls_runs = recent_balls_runs[-3:]
            if delivery_result != 7:
                ball_no += 1
            smart_sleep(2)
            delivery_loading()
            smart_sleep(1)

        # End of innings summary
        print("\n" + "="*80)
        print("END OF INNINGS {}".format(innings).center(80))
        print("="*80)
        
        print("\n{} finished their Super Over:".format(Batting_Team_Name))
        print("Total Score: {}/{}".format(batting_team_total_score, bowling_team_wickets))
        
        print("\nBatting Performance:")
        print("{}: {} {}".format(batting_lineup[0], batsman_one_total_score, batsman_one_status))
        print("{}: {} {}".format(batting_lineup[1], batsman_two_total_score, batsman_two_status))
        print("{}: {} {}".format(batting_lineup[2], batsman_three_total_score, batsman_three_status))
        
        print("\nBowling Performance:")
        print("{}: {}/{} in 1 over".format(bowler_one_name, batting_team_total_score, bowler_wickets))
        
         # Display Over Summary
        print("\nOver Summary:")
        if over_summary:
            over_display = " - ".join(["[{}]".format(ball) for ball in over_summary])
            print("{}:  {}".format(bowler_one_name, over_display))
            
            # Additional over statistics
            legal_deliveries = len([ball for ball in over_summary if ball != "wd"])
            extras = len([ball for ball in over_summary if ball == "wd"])
            boundaries = len([ball for ball in over_summary if ball in ["4", "6"]])
            wickets_in_over = len([ball for ball in over_summary if ball == "W"])
            
            print("Legal deliveries: {} | Extras: {} | Boundaries: {} | Wickets: {}".format(
                legal_deliveries, extras, boundaries, wickets_in_over))
        else:
            print("No deliveries bowled")



        # Set target for second innings
        if innings == 1:
            first_innings_team = Batting_Team_Name
            first_innings_score = batting_team_total_score
            first_innings_wickets = bowling_team_wickets
            Target = batting_team_total_score + 1
            print("\n{} needs {} runs to win from their Super Over!".format(Bowling_Team_Name, Target))
            smart_sleep(5)
        
        # Reset variables for next innings
        boundary_this_over = False
        balls_since_boundary = 0
        recent_balls_runs = []
        wicket_fell_last_ball = False
        # Move to next innings or conclude match
        if innings == 1:
            innings += 1
            print("\n" + "="*80)
            print("INNINGS BREAK".center(80))
            print("="*80)
            print("\nFirst innings complete!")
            print("{} scored: {}/{}".format(Batting_Team_Name, batting_team_total_score, bowling_team_wickets))
            print("{} needs {} runs to win!".format(Bowling_Team_Name, Target))
            print("\nPreparing for the second innings...")
            smart_sleep(5)
            
        else:
            # Match conclusion
            innings += 1
            print("\n" + "="*100)
            print("MATCH RESULT".center(100))
            print("="*100)
            
            # Determine scores for logging
            if innings == 3:  # After second innings
                if Batting_Team_Name == "England":
                    eng_score = batting_team_total_score
                    eng_wickets = bowling_team_wickets
                    nz_score = first_innings_score
                    nz_wickets = first_innings_wickets
                else:
                    nz_score = batting_team_total_score
                    nz_wickets = bowling_team_wickets
                    eng_score = first_innings_score
                    eng_wickets = first_innings_wickets
            
            if batting_team_total_score >= Target:
                winner = Batting_Team_Name
                print("\n🏆 {} HAS WON THE MATCH! 🏆".format(Batting_Team_Name).center(100))
                print("They are the Champions of the Cricket World Cup 2019!".center(100))
                print("\nMatch Summary:")
                print("First Innings: {} scored {}/{}".format(first_innings_team, first_innings_score, first_innings_wickets))
                print("Second Innings: {} scored {}/{} (Target: {})".format(Batting_Team_Name, batting_team_total_score, bowling_team_wickets, Target))
                print("\n{} won by {} wickets with {} balls remaining!".format(
                    Batting_Team_Name, 
                    2 - bowling_team_wickets, 
                    6 - balls_bowled
                ))
                
            elif batting_team_total_score == Target - 1:
                # Handle tie scenario
                winner = "TIE"
                print("\n🤯 UNBELIEVABLE! THE SUPER OVER ALSO ENDS IN A TIE! 🤯".center(100))
                print("This is unprecedented in cricket history!".center(100))
                print("\nAs per ICC rules, the team with more boundaries in the main match wins...")
                print("England scored 26 boundaries vs New Zealand's 17 boundaries in the 50-over match")
                
                # In the actual 2019 final, England won on boundary count
                if Bowling_Team_Name == "England":
                    winner = "England (Boundary Count)"
                    print("\n🏆 {} WINS ON BOUNDARY COUNT-BACK RULE! 🏆".format("England").center(100))
                else:
                    winner = "New Zealand (Boundary Count)"
                    print("\n🏆 {} WINS ON BOUNDARY COUNT-BACK RULE! 🏆".format("New Zealand").center(100))
                
                print("They are the Champions of the Cricket World Cup 2019!".center(100))
                print("\nThis will go down as one of the most dramatic finals in cricket history!")
                
            else:
                winner = Bowling_Team_Name
                print("\n🏆 {} HAS WON THE MATCH! 🏆".format(Bowling_Team_Name).center(100))
                print("They are the Champions of the Cricket World Cup 2019!".center(100))
                print("\nMatch Summary:")
                print("First Innings: {} scored {}/{}".format(first_innings_team, first_innings_score, first_innings_wickets))
                print("Second Innings: {} scored {}/{} (Target: {})".format(Batting_Team_Name, batting_team_total_score, bowling_team_wickets, Target))
                print("\n{} won by {} runs!".format(
                    Bowling_Team_Name, 
                    (Target - 1) - batting_team_total_score
                ))

            # Log the match result to CSV
            try:
                log_match_result(eng_score, eng_wickets, nz_score, nz_wickets, winner)
            except Exception as e:
                print(f"\n⚠️ Note: Could not save match result to file: {e}")
                print("Game will continue normally.")

            break

    # Game replay option
    print("\n" + "="*80)
    print("GAME OVER".center(80))
    print("="*80)
    
    # Use the timed input function for restart decision
    try:
        restart_game = timed_yes_no_input(
            "🎮 Do you want to play another match?", 
            timeout=20, 
            default_value='y'
        )
        
        if restart_game:
            print("\n🔄 Restarting the Game... Please wait! 🔄")
            print("Setting up new match...")
            smart_sleep(3)
            print("Loading teams...")
            smart_sleep(2)
            print("Preparing pitch...")
            smart_sleep(2)
            clear()
            
            # Reset all global variables for new game
            innings = 1
            Target = 999999
            user_choice = 0
            team_display_ind = 'N'
            batsmen_selection_done = True
            selected_batsmen = []
            batting_team_squad = []
            bowling_team_squad = []
            Batting_Team_Name = ''
            Bowling_Team_Name = ''
            first_innings_wickets = 0
            
            print("🏏 NEW MATCH STARTING! 🏏".center(80))
            smart_sleep(2)
            continue  # Continue to next iteration of main game loop
            
        else:
            # User chose not to restart - exit the game
            print(f"\n✅ Exiting game...")
            print("\n" + "="*80)
            print("THANK YOU FOR PLAYING!".center(80))
            print("="*80)
            print("\n🏏 Hope you enjoyed this thrilling cricket experience! 🏏")
            print("\nThis game recreated one of the most dramatic moments in cricket history.")
            print("The 2019 Cricket World Cup Final between England and New Zealand")
            print("will forever be remembered as one of the greatest matches ever played.")
            
            print("\n📧 Send your comments and suggestions to:")
            print("Anuj Puranik - anuj87in@gmail.com")
            
            print("\n🙏 Thank you for playing!")
            print("We look forward to your company next time.")
            print("Goodbye and keep playing cricket! 🏏")
            
            # Final loading animation before exit
            print("\nClosing game...")
            smart_sleep(3)
            delivery_loading()
            smart_sleep(2)
            clear()
            
            # Final farewell message
            print("\n" + "="*60)
            print("CRICKET WORLD CUP 2019 FINAL SIMULATOR".center(60))
            print("Created by: Anuj Puranik".center(60))
            print("="*60)
            print("\n🏆 Thanks for reliving cricket history! 🏆")
            smart_sleep(5)
            
            # EXIT THE MAIN GAME LOOP
            break  # This will exit the while (1 == 1) loop
            
    except KeyboardInterrupt:
        print("\n\n🛑 Game interrupted by user. Goodbye!")
        break  # Exit the main loop
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Exiting game due to error...")
        break  # Exit the main loop

# End of main game loop - this should be OUTSIDE the while loop
print("\nGame terminated successfully.")
sys.exit(0)
