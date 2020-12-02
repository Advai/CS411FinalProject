# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 12:02:51 2020
@author: hp
"""
import collections
from flask import Flask, render_template, request, flash, redirect,url_for, jsonify, session, make_response
from flask import Response,send_file
import os
from flask_cors import CORS, cross_origin
import boto3
import ast
import json
import requests

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table("players")
app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
# https://medium.com/@eric.hung0404/deal-with-cors-without-flask-cors-an-example-of-react-and-flask-5832c44108a7
def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response
def build_actual_response(response):
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return response
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

@app.route("/plr", methods=["post"])
@cross_origin(support_credentials=True)
def eloRankings():
    pgr_player_tourneys = set()
    pgr50 = dict(db.get_pgr50_1())
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
    obj_list = []
    for row in final2:
        d = collections.OrderedDict()
        d['Player'] = row
        d['Elo'] = final2[row]
        obj_list.append(d)
    return jsonify(obj_list)

@app.route("/pgr", methods=["post"])
@cross_origin(support_credentials=True)
def get_pgru_rankings():
    pgr50 = dict(db.get_pgr50_2())
    # print(pgr50)
    pgr50ids = list(pgr50.keys())
    # print(pgr50ids)
    player_ids = dict(db.get_gamertag_by_idlist(list(pgr50ids)))
    result = {}
    for ids in pgr50.keys():
        result[player_ids[ids]] = pgr50[ids]
    obj_list = []
    for row in result:
        d = collections.OrderedDict()
        d['Player'] = row
        d['Elo'] = result[row]
        obj_list.append(d)
    return jsonify(obj_list)

def handle_request(request):
    # print(request.form)
    actions = set(['insert', 'search','update','delete'])
    if request.method == 'POST':
        for action in actions:
            if request.form.get("gamertag_" + action) != None:
                return request.form.get("gamertag_" + action), action


def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))



@app.route('/search', methods=['post'])
@cross_origin(supports_credentials=True)
def search():
    req = json.loads(request.data)
    gamertag = req['tag']
    # print(gamertag)
    results = db.get_player_by_gamertag(gamertag)
    # print(results[0][0])
    res = json.loads(results[0][0])
    # print(res)
    return build_actual_response(jsonify(res))


@app.route("/test", methods=["get", "post"])
@cross_origin(supports_credentials=True)
def get_pgr_players():
    results = db.export_pgr_players_to_json()
    obj_list = []
    for row in results:
        d = collections.OrderedDict()
        d['game'] = row[0]
        d['player_id'] = row[1]
        d['tag'] = row[2]
        d['all_tags'] = row[3]
        d['prefixes'] = row[4]
        d['social'] = row[5]
        d['country'] = row[6]
        d['state'] = row[7]
        d['region'] = row[8]
        d['placings'] = row[9]
        d['characters'] = row[10]
        d['alias'] = row[11]
        obj_list.append(d)
    j = json.dumps(obj_list)
    # with open('pgr_player_data.json', 'w') as f:
    #     f.write(j)
    return results

@app.route("/headtohead", methods=["post"])
@cross_origin(support_credentials=True)
def get_head_to_head():
    data = json.loads(request.data)
    p1 = data["player1"]
    p2 = data["player2"] 
    p1_data = table.get_item(Key={"tag" : p1})
    p2_data = table.get_item(Key={"tag" : p2})
    # print(p1_data["placings"])
    common_tournaments = {}
    var = json.loads(p1_data["Item"]["placings"])
    for i in var:
        common_tournaments[i["key"]] = [i["placing"]]
    var2 = json.loads(p2_data["Item"]["placings"])
    for i in var2:
        if i["key"] in common_tournaments:
            common_tournaments[i["key"]].append(i["placing"])
    actual = {}
    for k in common_tournaments:
        if len(common_tournaments[k]) == 2 and common_tournaments[k][0] > 0 and common_tournaments[k][1] > 0:
            actual[k] = common_tournaments[k]
    # print(actual)
    cleaned_names = db.get_cleaned_names_by_keys(actual)
    actual2 = {}
    
    for k in actual:
        actual2[cleaned_names[k]] = actual[k]

    
    
    id_tag = {}
    print(db.get_playerid_by_tag(p1))
    print(db.get_playerid_by_tag(p2))
    id_tag[db.get_playerid_by_tag(p1)[0][0]] = p1
    id_tag[db.get_playerid_by_tag(p2)[0][0]] = p2

        

    obj_list = []
    d = collections.OrderedDict()
    d['player1'] = p1
    d['player2'] = p2
    

    sets = collections.OrderedDict()
    sets[p1] = 0
    sets[p2] = 0
    

    games = collections.OrderedDict()
    games[p1] = 0
    games[p2] = 0

    results = db.get_set_game_count(p1, p2)
    for res in results:
        sets[id_tag[res[1]]] += 1
        games[id_tag[res[2]]] += res[4]
        games[id_tag[res[3]]] += res[5]
    obj_list.append(d)
    obj_list.append(sets)
    obj_list.append(games)
    set_list = []
    for res in results:
        set_data = collections.OrderedDict()
        set_data['Round'] = ast.literal_eval(res[6])[2]
        set_data['Tournament'] = cleaned_names[res[0]]
        set_data['player1'] = res[4]
        set_data['player2'] = res[5]
        set_list.append(set_data)
    print(set_list)
    obj_list.append(set_list)
    d = collections.OrderedDict()
    for row in actual2:
        d = collections.OrderedDict()
        d['tournament'] = row
        d['placings'] = actual2[row]
        obj_list.append(d)
    # print(actual2)
    # print(jsonify(j))
    return jsonify(obj_list)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 3000), debug=True)