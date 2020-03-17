
from game_nmm.nmm import defaults as defs

import redis 
import json 
import time
import random

def initialize_board_info(room_name):
    r = redis.Redis(host='localhost', port=6379, db=0)

    game_info_key  = "game_" + room_name

    if not r.exists(game_info_key):

        info={
                'board':defs.empty_board,
                'all_men_placed':defs.all_men_placed,
                'men_placed':defs.men_placed,
                'men_remaining':defs.men_remaining,
                'made_mills_indexes':defs.made_mills_indexes,
                'counter':defs.counter,
                'changeGamePhase':defs.changeGamePhase,
                'ref_coord':defs.ref_coord
            }
        json_info=json.dumps(info)
        r.set(game_info_key, json_info)


def update_board_info(room_name,board,all_men_placed,men_placed,men_remaining,made_mills_indexes,counter=0,changeGamePhase=False ,ref_coord=8):
    r = redis.Redis(host='localhost', port=6379, db=0)
    game_info_key  = "game_"  +room_name

    made_mills_indexes['X']=list(made_mills_indexes['X'])
    made_mills_indexes['O']=list(made_mills_indexes['O'])
    info={
            'board':board,
            'all_men_placed':all_men_placed,
            'men_placed':men_placed,
            'men_remaining':men_remaining,
            'made_mills_indexes':made_mills_indexes,
            'counter':counter,
            'changeGamePhase':changeGamePhase,
            'ref_coord':ref_coord
        }

    json_info=json.dumps(info)
    r.set(game_info_key, json_info)

def get_board_info(room_name):
    r = redis.Redis(host='localhost', port=6379, db=0)
    game_info_key  = "game_"  +room_name

    info=r.get(game_info_key)
    info_json = json.loads(info.decode('utf-8'))

    board=info_json["board"]
    all_men_placed= info_json["all_men_placed"]
    men_placed=info_json["men_placed"]
    men_remaining=info_json["men_remaining"]
    made_mills_indexes=info_json["made_mills_indexes"]
    counter=info_json["counter"]
    changeGamePhase=info_json["changeGamePhase"]
    ref_coord=info_json["ref_coord"]

    return board,all_men_placed,men_placed,men_remaining,made_mills_indexes,counter,changeGamePhase,ref_coord

def check_game_websocket(room_name,channel_name):
    r = redis.Redis(host='localhost', port=6379, db=0)
    user1_game_key = "user1_" +room_name
    user2_game_key = "user2_" +room_name

    if r.exists(user2_game_key):
        return -1
    if r.exists(user1_game_key):
        r.set(user2_game_key, channel_name)
    else:
        r.set(user1_game_key, channel_name)
    return 1

def check_gameai_websocket(room_name,channel_name):
    r = redis.Redis(host='localhost', port=6379, db=0)
    user1_game_key = "user1_" +room_name

    if r.exists(user1_game_key):
        return -1
  
    r.set(user1_game_key, channel_name)
    return 1

def delete_websocket(room_name):
    r = redis.Redis(host='localhost', port=6379, db=0)

    user1_game_key = "user1_" +room_name
    user2_game_key = "user2_" +room_name
    r_room_name    = "asgi::group:"+room_name
    game_info_key  = "game_"  +room_name

    r.delete(user1_game_key)
    r.delete(user2_game_key)    
    r.delete(r_room_name)
    r.delete(game_info_key)

def wait_for_permission(room_name):
    r = redis.Redis(host='localhost', port=6379, db=0)
    perm="permission_"+room_name
    while True:
        if r.exists(perm):
            break
        else: 
            time.sleep(0.01)
    r.delete(perm)

def give_permission(room_name):
    r = redis.Redis(host='localhost', port=6379, db=0)
    perm="permission_"+room_name
    r.set(perm,1)

def add_to_lobby(ch_name,id,username):
    r = redis.Redis(host='localhost', port=6379, db=0)
    info={
            "channel_name":ch_name,
            "id":id,
            "username":username
        }
    r.lpush("lobby",json.dumps(info)) 
    return

def remove_from_lobby(ch_name,id,username):
    r = redis.Redis(host='localhost', port=6379, db=0)
    info={
            "channel_name":ch_name,
            "id":id,
            "username":username
        }
    r.lrem("lobby",1,json.dumps(info)) 
    return

def lobby_exists():
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r.exists("lobby")

def pop_random():
    r = redis.Redis(host='localhost', port=6379, db=0)
    d=r.lrange("lobby",0,r.llen("lobby"))[random.randint(0,r.llen("lobby")-1)].decode("utf-8")
    r.lrem("lobby",1,d)

    return json.loads(d)

def lobby_len():
    r = redis.Redis(host='localhost', port=6379, db=0)

    return r.llen("lobby")