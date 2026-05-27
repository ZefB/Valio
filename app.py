from flask import Flask, jsonify, render_template,request #We import necessary tools

from Original import implied_probability, filter_bets, calculate_ev #We import functions from python backend
app = Flask (__name__) #tells flask where project files are located

@app.route("/") #decorator that tells flask what to do when it is initiated
def index():
    return render_template("index.html")

@app.route("/scan")
def scan():
    sport = request.args.get("sport","all")
    try: 
        sports_tags ={
            "NBA" : ["basketball_nba"],
            "Soccer" : ["soccer_epl", "soccer_france_ligue_one", "soccer_uefa_champs_league","soccer_spain_la_liga"],
            "Tennis" : ["tennis_wta_italian_open"],
            "All" : ["basketball_nba", "soccer_epl", "soccer_france_ligue_one", "soccer_uefa_champs_league","soccer_spain_la_liga", "tennis_wta_italian_open"]
        }
        
        keys=[]
        for key in sports_tags[sport]:
            bets=implied_probability(key)
            for bet in bets:
                bet["sports_tag"]=key
            keys = keys + bets

        filtered=filter_bets(keys,0.01)
        print(len(filtered))
        for bet in filtered:
            ev=calculate_ev(0.6,bet["price"] ) #we hard code implied prob at 0.6 to test EV : this is real value bet["implied_probability"]
            bet["ev"]=round(ev,2)   
        return jsonify(filtered)

    except Exception as e:
        return jsonify({"error":str(e)}), 500



if __name__=="__main__": #only for dev not prod, it starts the server
    app.run(debug=True, host='0.0.0.0')
