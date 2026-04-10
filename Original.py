import requests
import os

from dotenv import load_dotenv #Hides api key so it doesnt get abused on GitHub
load_dotenv()
OddsApi= os.environ.get("ODDS_API_KEY")

def calculate_ev(probability, odds): #Calculate ev
    return probability * odds - 1

def convert_american_to_decimal(american_odds): 
    if american_odds > 0:
        decimal = (american_odds/100)+1 # type: converts US odds to decimals
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
        ev = calculate_ev(game['implied_probability'], game['price'])
        if ev > threshold:
            filtered.append(game)
    return (filtered)


if __name__ == "__main__":
    nba_bets=implied_probability("basketball_nba")
    nba_bets[0]["implied_probability"]= 0.65 #This is just to test the filter function, we set the first bet to have a high implied probability so it should be the only one that gets through the filter
    
    soccer_bets=implied_probability("soccer_fifa_world_cup")
    soccer_bets[0]["implied_probability"]= 0.65 #This is just to test the filter function, we set the first bet to have a high implied probability so it should be the only one that gets through the filter
    
    tennis_bets=implied_probability("tennis_wta_charleston_open")
    tennis_bets[0]["implied_probability"]= 0.65

    bets = nba_bets + soccer_bets + tennis_bets

    print (filter_bets (bets, 0.05))
        

                
    





