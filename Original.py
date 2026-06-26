import requests
import os

from dotenv import load_dotenv #Hides api key so it doesnt get abused on GitHub
load_dotenv()
OddsApi= os.environ.get("ODDS_API_KEY")

def calculate_ev(probability, odds): #Calculate ev
    return (probability * (odds - 1))- ( 1- probability)

def convert_american_to_decimal(american_odds): 
    if american_odds > 0:
        decimal = (american_odds/100)+1 #type:converts_US odds to decimals
    elif american_odds < 0:
        decimal = (100/abs(american_odds))+1 #We take absolute value to avoid getting negative results
    return decimal


def implied_probability(sports):
    url = f"https://api.the-odds-api.com/v4/sports/{sports}/odds"
    response = requests.get(url,params={"apiKey": OddsApi, "regions": "eu", "markets": "h2h"})
    #print(response.json())
    results = []
    best_odds = {}
    for game in response.json():
        for bookmaker in game['bookmakers']:
            for market in bookmaker['markets']:
                if market['key'] == 'h2h':
                    for outcome in market['outcomes']:
                            team_name = outcome['name']
                            if team_name not in best_odds : 
                                best_odds[team_name] = {
                                    "price": outcome['price'],
                                    "bookmaker": bookmaker['title'],
                                    "home_team" : game['home_team'],
                                    "away_team" : game['away_team'],
                                    "game_time" : game['commence_time'],
                                }

                            elif outcome['price'] > best_odds[team_name]['price']:
                                best_odds[team_name] = {
                                    "price": outcome['price'],
                                    "bookmaker": bookmaker['title'],
                                    "home_team" : game['home_team'],
                                    "away_team" : game['away_team'],
                                    "game_time" : game['commence_time'],
                                }

                        

    for team_name, data in best_odds.items():
        game_result={
        "team" : team_name,
        "price" : data['price'],
        "home_team" : data['home_team'],
        "away_team": data['away_team'],
        "game_time": data['game_time'],
        "bookmaker" : data['bookmaker'],
        "implied_probability" : 1/data['price']}
        results.append(game_result)
    return results

                        

def filter_bets(bets, threshold):
    filtered = []
    for game in bets:
        if 'true_probability' in game:
            ev = calculate_ev(game['true_probability'], game['price'])
        else :
            ev = calculate_ev(game['implied_probability'], game['price'])
        
        if ev > threshold:
            filtered.append(game)
    return (filtered)

if __name__ == "__main__":
    sport_keys = [
    "basketball_nba",
    "soccer_epl",
    "soccer_france_ligue_one",
    "soccer_uefa_champs_league",
    "soccer_spain_la_liga",
    "tennis_wta_italian_open",
    "tennis_atp_french_open",
    "tennis_wta_french_open",
    "soccer_fifa_world_cup",
    ]

    all_bets = []
    for key in sport_keys:
        bets = implied_probability(key)
        for bet in bets :
            bet ["sport"] = key
        all_bets= all_bets + bets

    print(filter_bets(all_bets, 0.05))
        

                
    





