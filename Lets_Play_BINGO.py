import random
import time
import os
import sys
import threading
from datetime import datetime


class HTMLLogger:
    """Logger to generate HTML output for web viewing"""
    def __init__(self, filename="bingo_game.html"):
        self.filename = filename
        self.initialize_html()
    
    def initialize_html(self):
        """Create initial HTML file with CSS"""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="3">
    <title>🎲 BINGO Game Live</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 20px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .current-call {
            background: rgba(255, 255, 255, 0.95);
            color: #333;
            padding: 40px;
            border-radius: 20px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        .current-call .number {
            font-size: 5em;
            font-weight: bold;
            color: #667eea;
            margin: 20px 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }
        .current-call .commentary {
            font-size: 1.5em;
            font-style: italic;
            color: #555;
            margin-top: 20px;
        }
        .info-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }
        .info-box {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        .info-box h3 {
            margin-bottom: 15px;
            font-size: 1.5em;
        }
        .called-numbers {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .called-number {
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 15px;
            border-radius: 10px;
            font-weight: bold;
            font-size: 1.1em;
        }
        .players-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .player-card {
            background: rgba(255, 255, 255, 0.95);
            color: #333;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        .player-card.winner {
            border: 5px solid gold;
            animation: winner-glow 1s infinite;
        }
        @keyframes winner-glow {
            0%, 100% { box-shadow: 0 0 20px gold; }
            50% { box-shadow: 0 0 40px gold; }
        }
        .player-name {
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
            color: #667eea;
        }
        .bingo-card {
            display: grid;
            gap: 2px;
            background: #333;
            padding: 2px;
            border-radius: 10px;
        }
        .bingo-header {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 2px;
            margin-bottom: 2px;
        }
        .bingo-header div {
            background: #667eea;
            color: white;
            padding: 10px;
            text-align: center;
            font-weight: bold;
            font-size: 1.2em;
        }
        .bingo-row {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 2px;
        }
        .bingo-cell {
            background: white;
            padding: 15px;
            text-align: center;
            font-weight: bold;
            font-size: 1.1em;
        }
        .bingo-cell.marked {
            background: #764ba2;
            color: white;
        }
        .bingo-cell.free {
            background: #ffd700;
            color: #333;
        }
        .winners-section {
            background: rgba(255, 215, 0, 0.2);
            padding: 30px;
            border-radius: 20px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            text-align: center;
        }
        .winners-section h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
        }
        .winner-name {
            font-size: 2em;
            margin: 10px 0;
            color: gold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        .footer {
            text-align: center;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        .timestamp {
            font-size: 0.9em;
            opacity: 0.8;
        }
        @media (max-width: 768px) {
            .info-section {
                grid-template-columns: 1fr;
            }
            .players-section {
                grid-template-columns: 1fr;
            }
            .header h1 {
                font-size: 2em;
            }
            .current-call .number {
                font-size: 3em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎲 BINGO GAME LIVE 🎲</h1>
            <p>Auto-refreshes every 3 seconds</p>
        </div>
        <div class="current-call">
            <div>Waiting for game to start...</div>
        </div>
    </div>
</body>
</html>"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def update_game_state(self, game_data):
        """Update HTML with current game state"""
        current_number = game_data.get('current_number', '')
        current_letter = game_data.get('current_letter', '')
        commentary = game_data.get('commentary', '')
        round_num = game_data.get('round_num', 0)
        called_numbers = game_data.get('called_numbers', [])
        players = game_data.get('players', [])
        winners = game_data.get('winners', [])
        
        # Generate called numbers HTML
        recent_numbers = called_numbers[-15:] if len(called_numbers) > 15 else called_numbers
        called_html = ''.join([
            f'<div class="called-number">{self.get_letter_for_number(num)}-{num}</div>'
            for num in reversed(recent_numbers)
        ])
        
        # Generate players HTML
        players_html = ''
        for player_data in players:
            is_winner = player_data['name'] in [w['name'] for w in winners]
            winner_class = 'winner' if is_winner else ''
            
            card_html = '<div class="bingo-header">'
            for letter in ['B', 'I', 'N', 'G', 'O']:
                card_html += f'<div>{letter}</div>'
            card_html += '</div>'
            
            for row in range(5):
                card_html += '<div class="bingo-row">'
                for col in range(5):
                    num = player_data['card'][col][row]
                    marked = player_data['marked'][col][row]
                    
                    if num == 'FREE':
                        card_html += '<div class="bingo-cell free">★</div>'
                    elif marked:
                        card_html += f'<div class="bingo-cell marked">{num}</div>'
                    else:
                        card_html += f'<div class="bingo-cell">{num}</div>'
                card_html += '</div>'
            
            players_html += f'''
            <div class="player-card {winner_class}">
                <div class="player-name">{'🏆 ' if is_winner else ''}{player_data['name']}{'  🏆' if is_winner else ''}</div>
                <div class="bingo-card">{card_html}</div>
            </div>
            '''
        
        # Generate winners section
        winners_html = ''
        if winners:
            winners_html = '<div class="winners-section">'
            winners_html += '<h2>🏆 WINNERS 🏆</h2>'
            for winner in winners:
                winners_html += f'<div class="winner-name">★ {winner["name"]} ★</div>'
                if winner.get('patterns'):
                    winners_html += f'<div style="font-size: 1.2em; margin: 5px 0;">({", ".join(winner["patterns"])})</div>'
            winners_html += '</div>'
        
        # Generate current call section
        if current_number:
            current_call_html = f'''
            <div class="current-call">
                <div style="font-size: 1.5em; color: #764ba2;">🔊 Currently Calling</div>
                <div class="number">{current_letter}-{current_number}</div>
                <div class="commentary">💬 "{commentary}"</div>
            </div>
            '''
        else:
            current_call_html = '<div class="current-call"><div>Waiting for next number...</div></div>'
        
        # Build complete HTML
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="3">
    <title>🎲 BINGO Game Live - Round {round_num}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 20px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}
        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}
        .current-call {{
            background: rgba(255, 255, 255, 0.95);
            color: #333;
            padding: 40px;
            border-radius: 20px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.02); }}
        }}
        .current-call .number {{
            font-size: 5em;
            font-weight: bold;
            color: #667eea;
            margin: 20px 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .current-call .commentary {{
            font-size: 1.5em;
            font-style: italic;
            color: #555;
            margin-top: 20px;
        }}
        .info-section {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .info-box {{
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }}
        .info-box h3 {{
            margin-bottom: 15px;
            font-size: 1.5em;
        }}
        .called-numbers {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .called-number {{
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 15px;
            border-radius: 10px;
            font-weight: bold;
            font-size: 1.1em;
        }}
        .players-section {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .player-card {{
            background: rgba(255, 255, 255, 0.95);
            color: #333;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}
        .player-card.winner {{
            border: 5px solid gold;
            animation: winner-glow 1s infinite;
        }}
        @keyframes winner-glow {{
            0%, 100% {{ box-shadow: 0 0 20px gold; }}
            50% {{ box-shadow: 0 0 40px gold; }}
        }}
        .player-name {{
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
            color: #667eea;
        }}
        .bingo-card {{
            display: grid;
            gap: 2px;
            background: #333;
            padding: 2px;
            border-radius: 10px;
        }}
        .bingo-header {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 2px;
            margin-bottom: 2px;
        }}
        .bingo-header div {{
            background: #667eea;
            color: white;
            padding: 10px;
            text-align: center;
            font-weight: bold;
            font-size: 1.2em;
        }}
        .bingo-row {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 2px;
        }}
        .bingo-cell {{
            background: white;
            padding: 15px;
            text-align: center;
            font-weight: bold;
            font-size: 1.1em;
        }}
        .bingo-cell.marked {{
            background: #764ba2;
            color: white;
        }}
        .bingo-cell.free {{
            background: #ffd700;
            color: #333;
        }}
        .winners-section {{
            background: rgba(255, 215, 0, 0.2);
            padding: 30px;
            border-radius: 20px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            text-align: center;
        }}
        .winners-section h2 {{
            font-size: 2.5em;
            margin-bottom: 20px;
        }}
        .winner-name {{
            font-size: 2em;
            margin: 10px 0;
            color: gold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }}
        .timestamp {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        @media (max-width: 768px) {{
            .info-section {{
                grid-template-columns: 1fr;
            }}
            .players-section {{
                grid-template-columns: 1fr;
            }}
            .header h1 {{
                font-size: 2em;
            }}
            .current-call .number {{
                font-size: 3em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎲 BINGO GAME LIVE 🎲</h1>
            <p>Round {round_num} • Auto-refreshes every 3 seconds</p>
        </div>
        
        {current_call_html}
        
        {winners_html}
        
        <div class="info-section">
            <div class="info-box">
                <h3>📊 Game Stats</h3>
                <p><strong>Round:</strong> {round_num}</p>
                <p><strong>Numbers Called:</strong> {len(called_numbers)}</p>
                <p><strong>Players:</strong> {len(players)}</p>
                <p><strong>Winners:</strong> {len(winners)}</p>
            </div>
            <div class="info-box">
                <h3>🎯 Recently Called Numbers</h3>
                <div class="called-numbers">
                    {called_html if called_html else '<p>No numbers called yet</p>'}
                </div>
            </div>
        </div>
        
        <h2 style="text-align: center; margin-bottom: 20px; font-size: 2em;">👥 Players</h2>
        <div class="players-section">
            {players_html}
        </div>
        
        <div class="footer">
            <p class="timestamp">Last updated: {timestamp}</p>
            <p style="margin-top: 10px;">🎲 Enjoy the game! Good luck! 🍀</p>
        </div>
    </div>
</body>
</html>"""
        
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def get_letter_for_number(self, number):
        """Get the BINGO letter for a number"""
        if 1 <= number <= 15:
            return 'B'
        elif 16 <= number <= 30:
            return 'I'
        elif 31 <= number <= 45:
            return 'N'
        elif 46 <= number <= 60:
            return 'G'
        elif 61 <= number <= 75:
            return 'O'
        return '?'


class TimedInput:
    """Helper class for timed input with countdown"""
    def __init__(self):
        self.input_value = None
        self.timer_expired = False
    
    def get_input_with_timer(self, prompt, timeout=10):
        """Get input with a countdown timer"""
        self.input_value = None
        self.timer_expired = False
        
        def input_thread():
            try:
                self.input_value = input(prompt)
            except:
                pass
        
        # Start input thread
        thread = threading.Thread(target=input_thread, daemon=True)
        thread.start()
        
        # Countdown timer
        for remaining in range(timeout, 0, -1):
            if self.input_value is not None:
                return self.input_value
            
            # Display countdown
            sys.stdout.write(f"\r  ⏱️  Auto-calling next number in {remaining} seconds... (Press Enter to continue, 'c' for cards, 'q' to quit)  ")
            sys.stdout.flush()
            time.sleep(1)
        
        # Timer expired
        if self.input_value is None:
            self.timer_expired = True
            sys.stdout.write("\r  ⏰ Time's up! Calling next number...                                                                     \n")
            sys.stdout.flush()
            return ""
        
        return self.input_value


class BingoCard:
    def __init__(self, player_name):
        self.player_name = player_name
        self.card = self.generate_card()
        self.marked = [[False] * 5 for _ in range(5)]
        self.marked[2][2] = True  # Center is free space
        
    def generate_card(self):
        """Generate a standard 5x5 BINGO card"""
        card = []
        # B: 1-15, I: 16-30, N: 31-45, G: 46-60, O: 61-75
        ranges = [(1, 15), (16, 30), (31, 45), (46, 60), (61, 75)]
        
        for col in range(5):
            start, end = ranges[col]
            numbers = random.sample(range(start, end + 1), 5)
            card.append(numbers)
        
        # Make center space FREE
        card[2][2] = 'FREE'
        
        return card
    
    def mark_number(self, number):
        """Mark a number on the card if it exists"""
        for i in range(5):
            for j in range(5):
                if self.card[i][j] == number:
                    self.marked[i][j] = True
                    return True
        return False
    
    def check_win(self):
        """Check for winning patterns: rows, columns, diagonals, or full card"""
        patterns = []
        
        # Check rows
        for i in range(5):
            if all(self.marked[i]):
                patterns.append(f"Row {i + 1}")
        
        # Check columns
        for j in range(5):
            if all(self.marked[i][j] for i in range(5)):
                patterns.append(f"Column {j + 1} ({['B', 'I', 'N', 'G', 'O'][j]})")
        
        # Check diagonals
        if all(self.marked[i][i] for i in range(5)):
            patterns.append("Diagonal (top-left to bottom-right)")
        
        if all(self.marked[i][4 - i] for i in range(5)):
            patterns.append("Diagonal (top-right to bottom-left)")
        
        # Check full card (blackout)
        if all(all(row) for row in self.marked):
            patterns.append("BLACKOUT (Full Card)")
        
        return patterns
    
    def display(self):
        """Display the BINGO card with marked numbers"""
        print(f"\n{'=' * 50}")
        print(f"  {self.player_name}'s BINGO Card")
        print(f"{'=' * 50}")
        print("  B     I     N     G     O  ")
        print("-" * 50)
        
        for row in range(5):
            line = ""
            for col in range(5):
                num = self.card[col][row]
                if self.marked[col][row]:
                    if num == 'FREE':
                        line += " [**] "
                    else:
                        line += f" [XX] "
                else:
                    if num == 'FREE':
                        line += " FREE "
                    else:
                        line += f" {num:>2}   "
            print(line)
        print("-" * 50)


class BingoGame:
    def __init__(self, num_players, enable_html=False, html_filename="bingo_game.html"):
        self.num_players = num_players
        self.players = []
        self.called_numbers = []
        self.all_numbers = list(range(1, 76))
        random.shuffle(self.all_numbers)
        self.winners = []
        self.timed_input = TimedInput()
        self.funny_comments = self.load_funny_comments()
        self.enable_html = enable_html
        self.html_logger = HTMLLogger(html_filename) if enable_html else None
    
    def load_funny_comments(self):
        """Load funny commentary for each number"""
        comments = {
            1: "Number ONE! We're just getting started!",
            2: "Two little ducks, quack quack! 🦆",
            3: "Three's a crowd... but we love crowds!",
            4: "Four corners of the world! 🌍",
            5: "High five! ✋",
            6: "Six pack abs! (Virtual ones count too 😅)",
            7: "Lucky SEVEN! 🍀",
            8: "Infinity on its side! ♾️",
            9: "Cloud NINE! ☁️",
            10: "Perfect TEN! 💯",
            11: "Legs ELEVEN! Two sticks!",
            12: "Vitamin B-12! Did you take it today? 💊",
            13: "THIRTEEN - Unlucky for some, lucky for you!",
            14: "Valentine's Day! February 14th! ❤️",
            15: "FIFTEEN - Young, wild & free!",
            16: "Sweet SIXTEEN! 🎂",
            17: "Dancing QUEEN was seventeen! 💃",
            18: "EIGHTEEN - Time to vote! 🗳️",
            19: "NINETEEN - Edge of 20!",
            20: "TWENTY - Score! Like in 'four score and seven years'",
            21: "TWENTY-ONE - Legal everywhere! 🍻",
            22: "Two little DUCKS in a row! 🦆🦆",
            23: "Michael Jordan's number! 🏀",
            24: "Twenty-four seven! We're always on!",
            25: "Quarter century! You're getting old... I mean wise! 🧙",
            26: "TWENTY-SIX - Two dozen plus two!",
            27: "Cube of 3! Math nerds unite! 🤓",
            28: "February has 28 days... except when it doesn't!",
            29: "TWENTY-NINE - Almost dirty thirty!",
            30: "THIRTY - Flirty and thriving! ✨",
            31: "THIRTY-ONE flavors at Baskin Robbins! 🍦",
            32: "Freezing point in Fahrenheit! ❄️",
            33: "All the THREES! Dirty birdy!",
            34: "THIRTY-FOUR - Rule 34... Google it! Wait, don't! 😳",
            35: "THIRTY-FIVE - Halfway to 70!",
            36: "Six squared! Another one for math lovers! 📐",
            37: "THIRTY-SEVEN - The random number everyone picks!",
            38: "THIRTY-EIGHT special! (It's a revolver 🔫)",
            39: "THIRTY-NINE steps to the top!",
            40: "Life begins at FORTY! 🎉",
            41: "Sum of the first six prime numbers! (Nerd alert 🤓)",
            42: "Answer to life, universe and EVERYTHING! 🌌",
            43: "FORTY-THREE - George W. Bush!",
            44: "All the FOURS! Droopy drawers!",
            45: "Halfway to NINETY! ⚡",
            46: "FORTY-SIX - Up to tricks!",
            47: "Four and seven! Almost 50!",
            48: "Four dozen! That's a lot of donuts! 🍩",
            49: "FORTY-NINE - PC from '49!",
            50: "FIFTY - Half a century! You made it! 🎊",
            51: "FIFTY-ONE - Tweak of the thumb!",
            52: "Deck of cards! Time to shuffle! 🃏",
            53: "FIFTY-THREE - Stuck in the tree!",
            54: "Clean the floor! 🧹",
            55: "FIFTY-FIVE - Snakes alive! 🐍",
            56: "FIFTY-SIX - Was she worth it?",
            57: "Heinz varieties! 🍅",
            58: "FIFTY-EIGHT - Make them wait!",
            59: "FIFTY-NINE - Brighton line!",
            60: "SIXTY - Five dozen! Grandma's age! 👵",
            61: "SIXTY-ONE - Bakers bun!",
            62: "Tickety-boo! SIXTY-TWO!",
            63: "SIXTY-THREE - Tickle me!",
            64: "Nintendo SIXTY-FOUR! Classic gaming! 🎮",
            65: "Retirement age! Time to relax! 😌",
            66: "Clickety-CLICK! All the sixes! Route 66! 🛣️",
            67: "Made in heaven! SIXTY-SEVEN!",
            68: "Saving grace! SIXTY-EIGHT!",
            69: "Either way up! SIXTY-NINE! 😏",
            70: "Three score and TEN! Biblical!",
            71: "Bang on the drum! SEVENTY-ONE! 🥁",
            72: "SEVENTY-TWO - Six dozen wise men!",
            73: "SEVENTY-THREE - Queen bee! 🐝",
            74: "SEVENTY-FOUR - Candy store!",
            75: "TOP OF THE SHOP! SEVENTY-FIVE! The highest number! 🏆"
        }
        return comments
    
    def get_funny_comment(self, number):
        """Get a funny comment for the called number"""
        return self.funny_comments.get(number, "Let's see who has this one!")
    
    def update_html_output(self, current_number=None, current_letter='', commentary='', round_num=0):
        """Update HTML file with current game state"""
        if not self.enable_html or not self.html_logger:
            return
        
        # Prepare players data
        players_data = []
        for player in self.players:
            players_data.append({
                'name': player.player_name,
                'card': player.card,
                'marked': player.marked
            })
        
        # Prepare winners data
        winners_data = []
        for winner in self.winners:
            patterns = winner.check_win()
            winners_data.append({
                'name': winner.player_name,
                'patterns': patterns
            })
        
        # Update HTML
        game_data = {
            'current_number': current_number,
            'current_letter': current_letter,
            'commentary': commentary,
            'round_num': round_num,
            'called_numbers': self.called_numbers,
            'players': players_data,
            'winners': winners_data
        }
        
        self.html_logger.update_game_state(game_data)
        
    def setup_players(self):
        """Setup players and their cards"""
        print("\n" + "=" * 50)
        print(" " * 15 + "BINGO HALL")
        print("=" * 50)
        
        for i in range(self.num_players):
            name = input(f"\nEnter name for Player {i + 1}: ").strip()
            if not name:
                name = f"Player {i + 1}"
            self.players.append(BingoCard(name))
        
        print("\n✅ All players registered! Generating BINGO cards...")
        time.sleep(1)
        
    def show_all_cards(self):
        """Display all players' cards"""
        for player in self.players:
            player.display()
            input("\nPress Enter to continue...")
        
    def call_number(self):
        """Call the next number"""
        if not self.all_numbers:
            return None
        
        number = self.all_numbers.pop(0)
        self.called_numbers.append(number)
        return number
    
    def get_letter_for_number(self, number):
        """Get the BINGO letter for a number"""
        if 1 <= number <= 15:
            return 'B'
        elif 16 <= number <= 30:
            return 'I'
        elif 31 <= number <= 45:
            return 'N'
        elif 46 <= number <= 60:
            return 'G'
        elif 61 <= number <= 75:
            return 'O'
        return '?'
    
    def display_called_numbers(self):
        """Display the last 10 called numbers"""
        print("\n" + "=" * 50)
        print("  Last Called Numbers:")
        print("=" * 50)
        
        recent = self.called_numbers[-10:]
        for num in recent:
            letter = self.get_letter_for_number(num)
            print(f"  {letter}-{num}", end="  ")
        print(f"\n  (Total called: {len(self.called_numbers)})")
        print("=" * 50)
    
    def check_all_winners(self):
        """Check if any player has won"""
        new_winners = []
        for player in self.players:
            if player not in self.winners:
                patterns = player.check_win()
                if patterns:
                    new_winners.append((player, patterns))
        return new_winners
    
    def play(self):
        """Main game loop"""
        self.setup_players()
        
        print("\n" + "=" * 50)
        print("  Let's see everyone's cards!")
        print("=" * 50)
        time.sleep(1)
        
        self.show_all_cards()
        
        # Initial HTML update
        if self.enable_html:
            self.update_html_output(round_num=0)
            print("\n  ✅ HTML output enabled! File: bingo_game.html")
        
        print("\n" + "=" * 50)
        print("  🎲 Starting BINGO Game!")
        print("=" * 50)
        input("\nPress Enter to start calling numbers...")
        
        game_running = True
        round_num = 0
        
        while game_running and self.all_numbers:
            round_num += 1
            
            # Clear screen (works on Windows and Unix)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"\n{'=' * 50}")
            print(f"  Round {round_num}")
            print(f"{'=' * 50}")
            
            # Call a number
            number = self.call_number()
            if number is None:
                print("\n🎱 All numbers have been called!")
                break
            
            letter = self.get_letter_for_number(number)
            print(f"\n  🔊 Calling: {letter}-{number}")
            
            # Display funny commentary
            comment = self.get_funny_comment(number)
            print(f"\n  💬 \"{comment}\"")
            
            print(f"\n  {'*' * 50}")
            
            # Mark the number on all cards
            for player in self.players:
                if player.mark_number(number):
                    print(f"  ✓ {player.player_name} has {letter}-{number}!")
            
            # Update HTML with current state
            if self.enable_html:
                self.update_html_output(
                    current_number=number,
                    current_letter=letter,
                    commentary=comment,
                    round_num=round_num
                )
            
            # Display called numbers
            self.display_called_numbers()
            
            # Check for winners
            new_winners = self.check_all_winners()
            
            if new_winners:
                for player, patterns in new_winners:
                    print(f"\n{'🎉' * 25}")
                    print(f"\n  🏆 BINGO! {player.player_name} WINS! 🏆")
                    print(f"\n  Winning Pattern(s): {', '.join(patterns)}")
                    print(f"\n{'🎉' * 25}")
                    
                    player.display()
                    self.winners.append(player)
                
                # Update HTML immediately after winner is detected
                if self.enable_html:
                    self.update_html_output(
                        current_number=number,
                        current_letter=letter,
                        commentary=comment,
                        round_num=round_num
                    )
                
                if len(self.winners) == self.num_players:
                    print("\n  All players have won! Game Over!")
                    game_running = False
                else:
                    choice = input("\n  Continue playing for more winners? (y/n): ").lower()
                    if choice != 'y':
                        game_running = False
            
            if game_running:
                # Use timed input with 10-second countdown
                choice = self.timed_input.get_input_with_timer("\n  ", timeout=15)
                
                # If timer expired, give a brief pause
                if self.timed_input.timer_expired:
                    time.sleep(1)
                
                if choice.lower() == 'q':
                    game_running = False
                elif choice.lower() == 'c':
                    self.show_all_cards()
                    input("\nPress Enter to continue...")
        
        # Game over
        print("\n" + "=" * 50)
        print("  🎮 GAME OVER 🎮")
        print("=" * 50)
        
        if self.winners:
            print("\n  🏆 WINNERS 🏆")
            for i, winner in enumerate(self.winners, 1):
                print(f"  {i}. {winner.player_name}")
        else:
            print("\n  No winners this round!")
        
        # Show final statistics
        print("\n  📊 Game Statistics:")
        print(f"  - Total numbers called: {len(self.called_numbers)}")
        print(f"  - Total rounds played: {round_num}")
        print(f"  - Total winners: {len(self.winners)}")
        
        # Final HTML update with game over state
        if self.enable_html:
            last_num = self.called_numbers[-1] if self.called_numbers else None
            last_letter = self.get_letter_for_number(last_num) if last_num else ''
            last_comment = self.get_funny_comment(last_num) if last_num else ''
            self.update_html_output(
                current_number=last_num,
                current_letter=last_letter,
                commentary=last_comment,
                round_num=round_num
            )
        
        print("\n  Thanks for playing BINGO! 🎲")
        print("=" * 50)


def main():
    """Main entry point"""
    play_again = True
    
    while play_again:
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n" + "=" * 50)
        print(" " * 10 + "🎲 WELCOME TO BINGO! 🎲")
        print("=" * 50)
        print("\n  Rules:")
        print("  - Each player gets a 5x5 BINGO card")
        print("  - Numbers will be called randomly")
        print("  - Mark numbers on your card as they're called")
        print("  - Win by completing: row, column, diagonal, or full card!")
        print("  - Center space is FREE for everyone")
        print("\n  ⏰ Timer Feature:")
        print("  - After each number, you have 15 seconds")
        print("  - Press Enter anytime to skip the timer")
        print("  - Timer reaches 0? Next number is auto-called!")
        print("\n  😄 Bonus Feature:")
        print("  - Enjoy funny commentary with each number!")
        print("  - From 'Vitamin B-12' to 'Lucky Seven' and more!")
        print("=" * 50)
        
        while True:
            try:
                num_players = int(input("\n  How many players? (1-10): "))
                if 1 <= num_players <= 10:
                    break
                else:
                    print("  Please enter a number between 1 and 10")
            except ValueError:
                print("  Please enter a valid number")
        
        # Ask if HTML output is needed
        print("\n" + "=" * 50)
        print("  🌐 Web Output Feature")
        print("=" * 50)
        print("\n  Do you want to generate HTML output for web viewing?")
        print("  (Perfect for hosting on a server and sharing live!)")
        
        while True:
            html_choice = input("\n  Enable HTML output? (y/n): ").lower().strip()
            if html_choice in ['y', 'yes', 'yeah', 'yep']:
                enable_html = True
                html_file = input("\n  Enter HTML filename (default: bingo_game.html): ").strip()
                if not html_file:
                    html_file = "bingo_game.html"
                elif not html_file.endswith('.html'):
                    html_file += '.html'
                print(f"\n  ✅ HTML output will be saved to: {html_file}")
                print("  📱 Auto-refreshes every 3 seconds!")
                break
            elif html_choice in ['n', 'no', 'nah', 'nope']:
                enable_html = False
                html_file = "bingo_game.html"
                print("\n  ✅ HTML output disabled. Terminal only!")
                break
            else:
                print("  Please enter 'y' for yes or 'n' for no")
        
        game = BingoGame(num_players, enable_html=enable_html, html_filename=html_file)
        game.play()
        
        # Ask if they want to play again
        print("\n" + "=" * 50)
        print("  🔄 PLAY AGAIN?")
        print("=" * 50)
        
        while True:
            restart = input("\n  Do you want to play another round? (y/n): ").lower().strip()
            if restart in ['y', 'yes', 'yeah', 'yep', 'sure', 'ok','bingo']:
                print("\n  🎉 Great! Starting a new game...")
                time.sleep(1.5)
                play_again = True
                break
            elif restart in ['n', 'no', 'nah', 'nope']:
                play_again = False
                print("\n" + "=" * 50)
                print("  👋 Thanks for playing BINGO!")
                print("  See you next time! Goodbye! 🎲")
                print("=" * 50 + "\n")
                break
            else:
                print("  Please enter 'y' for yes or 'n' for no")


if __name__ == "__main__":
    main()

