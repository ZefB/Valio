from flask import Flask, jsonify, render_template,request #We import necessary tools
from supabase_client import supabase, supabase2 #Import Supabase to create user authentification
from claude_analyzer import claude_analyzer
from Original import implied_probability, filter_bets, calculate_ev #We import functions from python backend
app = Flask (__name__) #tells flask where project files are located



@app.route("/signup", methods=["POST"]) #Set up sign up page
def signup():
    data = request.get_json()
    password = data["password"]
    email = data ["email"]
    try:
        supabase.auth.sign_up({"email": email, "password": password})
        return jsonify({"message": "success"})
    except Exception as e:
        print (e)
        return jsonify({"error":str(e)}), 500
    

@app.route("/login", methods=["POST"]) #set up login page
def login():
    data = request.get_json()
    password = data["password"]
    email = data ["email"]
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return jsonify({"message": "success", "session": response.session.access_token})
    
    except Exception as e:
        print (e)
        return jsonify({"error":str(e)}), 500



@app.route("/") #decorator that tells flask what to do when it is initiated
def index():
    return render_template("index.html")

PRE_FILTER_THRESHOLD= 0.0  #I added 2 thresholds, 1 that is a prefilter to limit claude api calls and the other to gain precision in games that passed the first test
DISPLAY_THRESHOLD= 0.0002


@app.route("/scan")
def scan():
    sport = request.args.get("sport","all")
    try: 
        sports_tags ={
            "nba" : ["basketball_nba"],
            "soccer" : [#"soccer_epl" out of season, "soccer_france_ligue_one", "soccer_spain_la_liga",
                "soccer_uefa_champs_league", "soccer_fifa_world_cup",],
            "tennis" : ["tennis_atp_wimbledon", "tennis_wta_wimbledon",], # out of season"tennis_wta_italian_open", "tennis_atp_french_open", "tennis_wta_french_open"],
            "baseball" : ["baseball_mlb"],
            "all" :  ["basketball_nba", "soccer_uefa_champs_league", "soccer_fifa_world_cup", "tennis_atp_wimbledon", "tennis_wta_wimbledon", "baseball_mlb"
                     #out of season"soccer_epl", "soccer_france_ligue_one",soccer_spain_la_liga", "tennis_wta_italian_open","tennis_atp_french_open", "tennis_wta_french_open", 
                      ]
        }
        
        keys=[]
        seen_games = set()
        for key in sports_tags[sport]:
            bets=implied_probability(key)
            for bet in bets:
                if (bet["home_team"], bet["away_team"]) in seen_games:
                    continue

                else:
                    seen_games.add((bet["home_team"], bet["away_team"]))

                bet["sports_tag"]=key
                keys.append(bet)

        filtered=filter_bets(keys,PRE_FILTER_THRESHOLD) 
        print(len(filtered))
        
        claude_filtered = []
        for bet in filtered:
                result = claude_analyzer(bet["home_team"], bet["away_team"], bet["sports_tag"])
                print(result)
                if result == None:
                    bet["analyzed"]=False
                elif result != None:
                    bet["analyzed"] = True
                    bet["true_probability"]=result

                claude_filtered.append(bet)
 
        
        # Stage 2: Claude analyzes pre-filtered games → returns true probability per bet
                                    # claude_filtered = claude_analysis(filtered)  # TODO: implement in claude_analyzer.py

        for bet in claude_filtered:
            if bet["analyzed"] == True:
                ev=calculate_ev(bet["true_probability"],bet["price"] ) 
            
            else:
                ev=calculate_ev(bet["implied_probability"],bet["price"] )
            
            bet["ev"]=round(ev,2)   
            
        claude_filtered = [bet for bet in claude_filtered if bet ["analyzed"]==True] #We make sure to only keep and display bets that pass the threshold 

        
        final = filter_bets(claude_filtered, DISPLAY_THRESHOLD)
        return jsonify(final)


    except Exception as e:
        print (e)
        return jsonify({"error":str(e)}), 500
    
@app.route("/log_bet", methods=["POST"])
def log_bet():
    try : 
        data = request.get_json()
        token = data["token"]
        home_team = data["home_team"]
        away_team = data["away_team"]
        game_time = data["game_time"]
        team = data["team"]
        sports_tag = data ["sports_tag"]
        bookmaker = data["bookmaker"]
        price = data["price"]
        ev = data["ev"]
        user = supabase.auth.get_user(token)
        user_id = user.user.id
        supabase2.table("Bets").insert({"home_team" : home_team,"away_team" : away_team, "game_time" : game_time, "team" : team, "sports_tag" :  sports_tag, "bookmaker" : bookmaker, "price" : price, "ev" : ev, "user_id" : user_id}).execute()
        return jsonify({"message": "success"})
    
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route("/my_bets", methods=["POST"])
def my_bets():
    try : 
        data = request.get_json()
        token = data["token"]
        user = supabase.auth.get_user(token)
        user_id = user.user.id
        result = supabase2.table("Bets").select("*").eq("user_id", user_id).execute()
        return jsonify(result.data)

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


if __name__=="__main__": #only for dev not prod, it starts the server
    app.run(debug=True, host='0.0.0.0')
