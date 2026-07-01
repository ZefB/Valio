# Valio - AI Sports EV Calculator
Live at valioev.com

## What is Valio
Valio is an AI powered expected value calculator that scans live sports odds across bookmakers and identifies bets favoring the user.

## How it works
Expected value in sports betting is not about predicting which team will win — it is about identifying when a bookmaker has mispriced the odds in your favour.

Valio uses a two-stage filtering process. In the first stage, all available bets are filtered using a baseline formula based on the bookmaker's implied probability and odds. In the second stage, Claude AI estimates the true probability of each outcome independently, allowing Valio to recalculate EV with greater precision.

EV = (true probability × (odds - 1)) - (1 - true probability)

A positive EV means the odds are in your favour over the long run.

## Features
- Real-time odds scanning across major European bookmakers
- AI-powered true probability estimation via Claude
- Two-stage EV filtering to minimize API costs
- Deduplication across leagues and bookmakers
- Covers NBA, MLB, Soccer, and Tennis
- Mobile responsive

## Tech Stack
Python, HTML, CSS, JS,  Flask, Anthropic Claude, The Odds API, Railway 

## Installation
1. Clone the Valio repository
2. Install dependencies : `pip install -r requirements.txt`
3. Create a `.env` file with your API keys:
ANTHROPIC_API_KEY=your_key_here
ODDS_API_KEY=your_key_here
The `.env` file should never be pushed to GitHub. It must be stored in `.gitignore`
4. Run the app `python app.py`
5. Open localhost `http://localhost:5000`


## Disclaimer
This tool is solely a calculator and should not be considered gambling advice
