# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 13:34:18 2020
@author: hp
"""
import json
from aws_credentials import create_connection

#Table Creation
#cursor=conn.cursor()
#create_table="""
#create table Details (name varchar(200),email varchar(200),comment varchar(200),gender varchar(20) )
#
#"""
#cursor.execute(create_table)


'''
insert_player(playerId)
get_player(playerId)
'''
PGR_Players = (
    "MkLeo", "Samsora", "Tweek", "Nairo", "Marss", "Maister", "zackray",
    "Glutonny", "Dabuz", "Light", "Kameme", "Tea", "Shuton", "ESAM",
    "T", "Raito", "Kuro", "ProtoBanham", "WaDi", "Lea", "Dark Wizzy",
    "Cosmos", "Abadango", "Kome", "Choco", "Nietono", "LeoN", "Gackt",
    "Salem", "Raffi-X", "Elegant", "Pandarian", "Etsuji", "Umeki", "Nicko",
    "Ned", "VoiD", "Lui$", "ScAtt", "HIKARU", "Goblin", "BestNess", "Mr.R",
    "RFang", "Kola", "Riddles", "Kirihara", "Big D", "Ron"
)

def get_player_by_gamertag(tag):
    query = f"SELECT placings FROM players where tag='{tag}'"
    cur=create_connection().cursor()
    cur.execute(query)
    details = cur.fetchall()
    cur.close()
    # player_list = []
    # for i in details:
    #     t = (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11])
    #     player_list.append(t)
    # j = json.dumps(player_list, indent=2)
    # print(j)
    # with open("player_data.json", "w") as f:
    #     f.write(j)
    return details

def delete_player_by_gamertag(tag):
    query = f"DELETE FROM players where tag='{tag}'"
    conn=create_connection()
    cur=conn.cursor()
    cur.execute(query)
    conn.commit()
    details = cur.fetchall()
    cur.close()

    return

def insert_player_by_gamertag(tag):
    query = f"INSERT INTO players (game, tag, all_tags, prefixes, social, country, state, region, placings, characters, alias) VALUES ('ultimate', '{tag}', NULL, NULL, NULL, NULL, NULL, NULL, '[{{\"key\": \"your-smash-bros-event\", \"placing\": 999, \"seed\": 999, \"dq\": false}}]', NULL, NULL);"
    conn=create_connection()
    cur=conn.cursor()
    cur.execute(query)
    conn.commit()
    details = cur.fetchall()
    cur.close()

    return

def update_player_by_gamertag(tag, newtag):
    query = f"UPDATE players SET tag = '{newtag}' where tag= '{tag}';"
    conn=create_connection()
    cur=conn.cursor()
    cur.execute(query)
    conn.commit()
    details = cur.fetchall()
    cur.close()

    return

def get_cleaned_names_by_keys(keys):
    cur = create_connection().cursor()
    cleaned_names = {}
    for key in keys:
        query = f"SELECT cleaned_name \
                  FROM tournament_info \
                  WHERE tournament_info.key = '{key}'"
        cur.execute(query)
        details = cur.fetchall()
        cleaned_names[key] = details[0][0]
    cur.close()
    return cleaned_names

def get_set_game_count(p1, p2):
    cur = create_connection().cursor()
    query = f"SELECT tournament_key, winner_id, p1_id, p2_id, p1_score, p2_score, location_names \
            FROM sets WHERE (p1_id=(SELECT player_id FROM players WHERE tag='{p1}' GROUP BY tag) AND p2_id=(SELECT player_id FROM players WHERE tag='{p2}' GROUP BY tag)) \
            OR (p1_id=(SELECT player_id FROM players WHERE tag='{p2}' GROUP BY tag) AND p2_id=(SELECT player_id FROM players WHERE tag='{p1}' GROUP BY tag))"
    cur.execute(query)
    details = cur.fetchall()
    print(details)
    cur.close()
    return details
    
def export_pgr_players_to_json():
    query = f"SELECT DISTINCT * \
              FROM players \
              WHERE tag IN {PGR_Players} AND game='ultimate' GROUP BY tag"
    cur = create_connection().cursor()
    cur.execute(query)
    details = cur.fetchall()
    cur.close()
    return details

def get_playerid_by_tag(tag):
    query = f"SELECT player_id \
              FROM players \
              where tag = '{tag}' AND game='ultimate' GROUP BY tag"
    cur = create_connection().cursor()
    cur.execute(query)
    details = cur.fetchall()
    cur.close()
    return details

def get_players_by_placement(placement):
    query = f"SELECT * \
            FROM Player P NATURAL JOIN EventStanding E NATURAL JOIN TournamentEvent T \
            WHERE placement={placement} AND P.player_id = E.player_id AND T.tournament_id = E.tournament_id GROUP BY placement" 
    # query = f"SELECT gamer_tag FROM Player P JOIN EventStanding E JOIN TournamentEvent T WHERE placement={placement} AND P.player_id = E.player_id AND T.tournament_id = E.tournament_id GROUP BY placement"
    cur = conn.cursor()
    cur.execute(query)
    details = cur.fetchall()
    return details

def get_pgr50_2():
    query = f"select by_id from ranking_seasons \
              where season = 2 and ranking_name = 'PGRU'"
    cur = create_connection().cursor()
    cur.execute(query)
    details = cur.fetchall()
    cur.close()
    return json.loads(details[0][0])

def get_pgr50_1():
    query = f"select by_id \
            from ranking_seasons \
            where season = 1 and ranking_name = 'PGRU'"
    cur = create_connection().cursor()
    cur.execute(query)
    details = cur.fetchall()
    cur.close()
    return json.loads(details[0][0])

def get_sets_by_list_of_player_ids(player_list):
    player_tups = tuple(player_list)
    query = f"select tournament_key,winner_id,p1_id,p2_id,p1_score,p2_score,location_names \
            from sets \
            where p1_id in {player_tups} and p2_id in {player_tups} and best_of is not null and p1_score >= 0 and p2_score >= 0"
    cur = create_connection().cursor()
    cur.execute(query)
    details = cur.fetchall()
    cur.close()
    return details

def get_entrants_by_list_of_tournaments(tourney_list):
    tourney_tups = tuple(tourney_list)
    query = f"select tournament_info.key, entrants \
            from tournament_info \
            where tournament_info.key in {tourney_tups}"
    cur = create_connection().cursor()
    cur.execute(query)
    details = cur.fetchall()
    cur.close()
    return details

def get_gamertag_by_idlist(_idlist):
    _id_tups = tuple(_idlist)
    query = f"select player_id, tag \
            from players \
            where player_id in {_id_tups}"
    cur = create_connection().cursor()
    cur.execute(query)
    details = cur.fetchall()
    cur.close()
    return details
