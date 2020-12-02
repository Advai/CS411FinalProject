# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 12:02:51 2020
@author: hp
"""

from flask import Flask, render_template, request, flash, redirect,url_for, jsonify, session 
from flask import Response,send_file
import json

app = Flask(__name__)

import rds_db as db


@app.route('/', methods=['get'])
@app.route('/index', methods=['get', 'post'])
def index():
    return render_template('index.html')

class PlayerHistory:
    def __init__(self,_id,name,elo):
        self.id = _id
        self.name = name
        self.elo = elo
        self.set_history = set()
    def __str__(self):
        return f"{self.name}: {self.elo}"

class Sets:
    def __init__(self,entrants, winner_id, idA, idB, Ascore, Bscore, bracket):
        self.entrants = entrants
        self.winner_id = winner_id
        self.idA = idA
        self.idB = idB
        self.Ascore = Ascore
        self.Bscore = Bscore
        self.bracket = bracket

@app.route('/rankings', methods=['get'])
def eloRankings():
    pgr_player_tourneys = set()
    pgr50 = dict(db.get_pgr50())
    pgr50ids = list(pgr50.keys())
    setdata = db.get_sets_by_list_of_player_ids(pgr50ids)
    for s in setdata:
        pgr_player_tourneys.add(s[0])
    pgr_tourney_entrants = dict(db.get_entrants_by_list_of_tournaments(pgr_player_tourneys))
    player_ids = dict(db.get_gamertag_by_idlist(list(pgr50ids)))
    player_histories = {}
    sets = set()
    bracket = -1
    initeloA = initeloB = -1
    for s in setdata:
        # print(s)
        if s[0] not in pgr_tourney_entrants:
            continue
        entrants = pgr_tourney_entrants[s[0]]
        snippet = s[6][2:5]
        if 'L' in snippet or 'GFR' in snippet:
            bracket = 0
        elif 'W' in snippet or 'GF' in snippet:
            bracket = 1
        else:
            continue
        if 1 <= pgr50[s[2]] <= 10:
            initeloA = 2000
        elif 11 <= pgr50[s[2]] <= 20:
            initeloA = 1900
        elif 21 <= pgr50[s[2]] <= 30:
            initeloA = 1800
        elif 31 <= pgr50[s[2]] <= 40:
            initeloA = 1700
        elif 41 <= pgr50[s[2]] <= 50:
            initeloA = 1600
        else:
            initeloA = 1500
        if 1 <= pgr50[s[3]] <= 10:
            initeloB = 2000
        elif 11 <= pgr50[s[3]] <= 20:
            initeloB = 1900
        elif 21 <= pgr50[s[3]] <= 30:
            initeloB = 1800
        elif 31 <= pgr50[s[3]] <= 40:
            initeloB = 1700
        elif 41 <= pgr50[s[3]] <= 50:
            initeloB = 1600
        else:
            initeloB = 1500
        if s[2] not in player_histories:
            player_histories[s[2]] = PlayerHistory(s[2], player_ids[s[2]], initeloA)
            player_histories[s[2]].set_history.add(Sets(entrants,s[1],s[2],s[3],s[4],s[5],bracket))
        else:
            player_histories[s[2]].set_history.add(Sets(entrants,s[1],s[2],s[3],s[4],s[5],bracket))

        if s[3] not in player_histories:
            player_histories[s[3]] = PlayerHistory(s[3], player_ids[s[3]], initeloB)
            player_histories[s[3]].set_history.add(Sets(entrants,s[1],s[2],s[3],s[4],s[5],bracket))
        else:
            player_histories[s[2]].set_history.add(Sets(entrants,s[1],s[2],s[3],s[4],s[5],bracket))
    
        sets.add(Sets(entrants,s[1],s[2],s[3],s[4],s[5],bracket))

    for currset in sets:
        elo1 = player_histories[currset.idA].elo
        elo2 = player_histories[currset.idB].elo
        n = currset.entrants
        R = 1 if currset.winner_id == currset.idA else 0
        s1 = currset.Ascore
        s2 = currset.Bscore
        b = currset.bracket
        w1 = R
        h1 = len(player_histories[currset.idA].set_history)

        newElo1 = elo1 + 20 * (1 + b * 0.5 * w1) * (min(5/h1 + 0.4, 2)) * (1.95 + (-1.82 / (1 + (n/1040.56) ** 1.762))) * ((abs(s1-s2)) ** 0.9) * (R - (1/(1 + (10) ** (-1 * ((elo1 - elo2) / 400)))))

        player_histories[currset.idA].elo = newElo1

    final = sorted(player_histories.values(), key=lambda x: x.elo, reverse=True)
    final2 = {}
    for item in final:
        final2[item.name] = item.elo

    return jsonify(final2)

    return render_template('index.html')

def handle_request(request):
    # print(request.form)
    actions = set(['insert', 'search','update','delete'])
    if request.method == 'POST':
        for action in actions:
            if request.form.get("gamertag_" + action) != None:
                return request.form.get("gamertag_" + action), action

@app.route('/insert',methods = ['post'])
def insert():
    actions = set(['insert', 'search','update','delete'])
    action = request.form['chooseField']
    # print(f"This is the action: {action}")
    results = None
    if action == "search":
        gamertag = request.form['baseInput']
        print(gamertag)
        results = db.get_player_by_gamertag(gamertag)
        print(len(results))
    elif action == "insert":
        gamertag = request.form['baseInput']
        results = db.insert_player_by_gamertag(gamertag)
    elif action == "update":
        old_gamer_tag = request.form['updateField1']
        new_gamer_tag = request.form['updateField2']
        results = db.update_player_by_gamertag(old_gamer_tag, new_gamer_tag)
    elif action == "delete":
        gamertag = request.form['baseInput']
        results = db.delete_player_by_gamertag(gamertag)
    elif action == "placement":
        placement = request.form['baseInput']
        results = db.get_players_by_placement(placement)
        for detail in results:
            var = detail
        return render_template('blank.html', var=var)
    if results == None:
        return redirect('index', code=307)
    elif len(results) == 0:
        var = "Sorry! That record was not found"
        return render_template('index.html', var=var)
    return render_template('index.html', var=results)



if __name__ == "__main__":
    
    app.run(debug=True)