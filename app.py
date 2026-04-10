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
        if sport == "nba":
            bets=implied_probability("basketball_nba")
            for bet in bets:
                bet["sport"]="NBA"
        
        elif sport == "soccer":
            bets=implied_probability("soccer_fifa_world_cup")
            for bet in bets:
                bet["sport"]="Soccer"

        elif sport == "tennis":
            bets=implied_probability("tennis_wta_charleston_open")
            for bet in bets:
                bet["sport"]="Tennis"

        else:
            nba = implied_probability("basketball_nba")
            for bet in nba:
                bet["sport"]="NBA"
            soccer = implied_probability("soccer_fifa_world_cup")
            for bet in soccer:
                bet["sport"]="Soccer"
            tennis = implied_probability("tennis_wta_charleston_open")
            for bet in tennis:
                bet["sport"]="Tennis"
            bets = nba + soccer + tennis

        for bet in bets:
            bet["implied_probability"] = 0.75
        filtered=filter_bets(bets,0.01)
        print(len(filtered))
        for bet in filtered:
            ev=calculate_ev(0.6,bet["price"] ) #we hard code implied prob at 0.6 to test EV : this is real value bet["implied_probability"]
            bet["ev"]=round(ev,2)   
        return jsonify(filtered)

    except Exception as e:
        return jsonify({"error":str(e)}), 500



if __name__=="__main__": #only for dev not prod, it starts the server
    app.run(debug=True, host='0.0.0.0')
