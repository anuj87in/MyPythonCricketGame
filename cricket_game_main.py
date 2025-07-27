import os
import random
import time
import sys

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
            time.sleep(1.0 / loading_speed)
        index += 1
        sys.stdout.write("\b" * index + " " * index + "\b" * index)
        sys.stdout.flush()
        loading = False

def load_countdown():
    """Display countdown before innings starts"""
    count = 10
    global innings
    while (count >= 0):
        time.sleep(1)
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
    """Enhanced user input validation with better error handling"""
    global user_choice
    global team_display_ind
    choice_accepted = False
    while (choice_accepted != True):
        if (team_display_ind != "N"):
            team_diplay()
        try:
            user_choice = int(input("\nPlease enter your choice of {} for {}:\n".format(role_name, team_name)))
            if (user_choice <= 11 and user_choice >= 1):
                if (batsmen_selection_done == False):
                    if (user_choice in selected_batsmen):
                        print("Incorrect choice entered for {} for {}\n".format(role_name, team_name))
                        team_display_ind = "Y"
                    else:
                        choice_accepted = True
                else:
                    choice_accepted = True
            else:
                print("Incorrect choice entered for {} for {}\n".format(role_name, team_name))
                team_display_ind = "Y"
        except ValueError:
            print("Incorrect choice entered for {} for {}\n".format(role_name, team_name))
            team_display_ind = "Y"

# 


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

    time.sleep(30)
    print("\nNow lets get started with the game\n")
    print("\n\n\n")
    delivery_loading()
    time.sleep(2)
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

# Main game loop
while (1 == 1):
    Target = 999999  # Initialize target for first innings

    # Game introduction
    print("Welcome to the Cricket World Cup 2019 Finals\n"
          "\nIn an interesting turn of events after 50 Overs both teams stand equal in terms of runs Scored \n"
          "NZL batting first Scored 241/8 \t in reply ENG chasing got all out for 241 \n")

    time.sleep(5)

    print('It is now time for the Super Over to break the tie in this Cricket World Cup 2019 Final \n')

    time.sleep(5)

    innings = 1  # Start with first innings

    # Play both innings
    while (innings <= 2):

        time.sleep(5)
        team_diplay()
        team_display_ind = 'N'

        batsmen_selection_done = True
        selected_batsmen = []

        # Player selection phase
        validate_user_choice_new('Opening Batsmen at Striker End', Batting_Team_Name)
        strike_batsman = batting_team_squad[int(user_choice) - 1]
        print('{} is chosen as the Strike Batsmen for {} \n'.format(strike_batsman, Batting_Team_Name))
        selected_batsmen.append(user_choice)
        batsmen_selection_done = False

        validate_user_choice_new('Opening Batsmen at Non Striker End', Batting_Team_Name)
        non_strike_batsman = batting_team_squad[int(user_choice) - 1]
        print('{} is chosen as the Non-strike Batsmen for {} \n'.format(non_strike_batsman, Batting_Team_Name))
        selected_batsmen.append(user_choice)

        validate_user_choice_new('Third Batsmen', Batting_Team_Name)
        third_batsman = batting_team_squad[int(user_choice) - 1]
        print('{} is chosen as the Third Batsmen for {} \n'.format(third_batsman, Batting_Team_Name))
        batsmen_selection_done = True
        selected_batsmen.clear()

        # REPLACE the existing bowler selection with:
        while True:
            validate_user_choice_new('Opening Bowler', Bowling_Team_Name)
            selected_bowler = bowling_team_squad[int(user_choice) - 1]
            
            # Handle wicket-keeper scenario
            keeper_for_innings = handle_wicket_keeper_selection(Bowling_Team_Name, selected_bowler)
            
            if keeper_for_innings is not None:
                bowler_one_name = selected_bowler
                print(f"\n🏏 Super Over Setup:")
                print(f"Bowler: {bowler_one_name}")
                print(f"Wicket-keeper: {keeper_for_innings}")
                print(f"Captain: {TEAM_CONFIGS[Bowling_Team_Name]['captain']} (unchanged)")
                break
            else:
                print("Please select a different bowler.")

        # validate_user_choice_new('Opening Bowler', Bowling_Team_Name)
        # bowler_one_name = bowling_team_squad[int(user_choice) - 1]
        # print('{} is chosen as the Super Over Bowler for {} \n'.format(bowler_one_name, Bowling_Team_Name))

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
        time.sleep(2)
        load_countdown()
        time.sleep(2)

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
        time.sleep(2)
        delivery_loading()
        time.sleep(1)

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
                time.sleep(3)
                delivery_loading()
                time.sleep(2)
                break
                
            # Keep only last 3 balls for pressure calculation
            if len(recent_balls_runs) > 3:
                recent_balls_runs = recent_balls_runs[-3:]
            if delivery_result != 7:
                ball_no += 1
            time.sleep(2)
            delivery_loading()
            time.sleep(1)

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
            time.sleep(5)
        
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
            time.sleep(5)
            
        else:
            # Match conclusion
            innings += 1
            print("\n" + "="*100)
            print("MATCH RESULT".center(100))
            print("="*100)
            
            if batting_team_total_score >= Target:
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
                print("\n🤯 UNBELIEVABLE! THE SUPER OVER ALSO ENDS IN A TIE! 🤯".center(100))
                print("This is unprecedented in cricket history!".center(100))
                print("\nAs per ICC rules, the team with more boundaries in the main match wins...")
                print("England scored 26 boundaries vs New Zealand's 17 boundaries in the 50-over match")
                print("\n🏆 {} WINS ON BOUNDARY COUNT-BACK RULE! 🏆".format(Bowling_Team_Name).center(100))
                print("They are the Champions of the Cricket World Cup 2019!".center(100))
                print("\nThis will go down as one of the most dramatic finals in cricket history!")
                
            else:
                print("\n🏆 {} HAS WON THE MATCH! 🏆".format(Bowling_Team_Name).center(100))
                print("They are the Champions of the Cricket World Cup 2019!".center(100))
                print("\nMatch Summary:")
                print("First Innings: {} scored {}/{}".format(Bowling_Team_Name, Target-1, first_innings_wickets))
                print("Second Innings: {} scored {}/{} (Target: {})".format(Batting_Team_Name, batting_team_total_score, bowling_team_wickets, Target))
                print("\n{} won by {} runs!".format(
                    Bowling_Team_Name, 
                    (Target - 1) - batting_team_total_score
                ))

    # Game replay option
    print("\n" + "="*80)
    print("GAME OVER".center(80))
    print("="*80)
    
    game_over = input('\nDo you want to Play again?\nType Y or y for Yes, any other key for No: ')
    
    if game_over.lower() == 'y':
        print("\n🔄 Restarting the Game... Please wait! 🔄")
        print("Setting up new match...")
        time.sleep(3)
        print("Loading teams...")
        time.sleep(2)
        print("Preparing pitch...")
        time.sleep(2)
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
        print("Welcome back to the Cricket World Cup 2019 Finals!")
        time.sleep(2)
        
    else:
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
        time.sleep(3)
        delivery_loading()
        time.sleep(2)
        clear()
        
        # Final farewell message
        print("\n" + "="*60)
        print("CRICKET WORLD CUP 2019 FINAL SIMULATOR".center(60))
        print("Created by: Anuj Puranik".center(60))
        print("="*60)
        print("\n🏆 Thanks for reliving cricket history! 🏆")
        time.sleep(5)
        break

# End of main game loop
print("\nGame terminated successfully.")
sys.exit(0)

    
    