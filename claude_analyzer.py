import os
from dotenv import load_dotenv

import anthropic

client = anthropic.Anthropic()

def claude_analyzer(home_team, away_team, sport):
    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens = 50,
            system="You are a sports probablity analyst and must return only a number between 0 and 1",
            messages=[
                {"role": "user", "content": f"Estimate home team win probability using home_team {home_team} versus away_team {away_team} in sport {sport}"}
            ],
        )
        print (message.content)
        return float(message.content[0].text.strip())


    except:
        return None 
    
    
