
import threading
import time
import json
import string
from game_nmm import redis_management as rm
from asgiref.sync import async_to_sync
from random import choices , randrange

class Game_Timer (threading.Thread): #game timer thread sends a signal when the time is over
    def __init__(self,room_name):
        super(Game_Timer , self).__init__(name="Game_Timer thread")
        self.room_name=room_name
        self.default_time=15

    def run(self):
        rn=self.room_name

        time.sleep(5)
        rn.send(text_data=json.dumps({
            'message': "your time is up"

        })) 

class Lobby_Match (threading.Thread): #lobby match thread searches for random players and adds them to a game
    def __init__(self,cs):
        self.cons=cs
        super(Lobby_Match , self).__init__(name="Lobby_Match thread")

    def run(self):
        while True:
            time.sleep(4)
            if not rm.lobby_len()<2:
                self.match(rm.pop_random(),rm.pop_random())
            else:
                time.sleep(2)

    def match(self,pl1_info,pl2_info):
        room_hash = ''.join(choices(string.ascii_letters + string.digits, k=randrange(16,24)))
        room_name='nmm_room'+"_"+room_hash
        send_info={
            'type': "match",
            'data': {
                "pl_list":[pl1_info["channel_name"],pl2_info["channel_name"]],
                "pl1":{
                    "marker":"X",
                    "room":room_name,
                    "opponent":{
                        "userId": pl2_info["id"],
                        "username": pl2_info["username"]
                    }
                },
                "pl2":{
                    "marker":"O",
                    "room":room_name,
                    "opponent":{
                        "userId": pl1_info["id"],
                        "username": pl1_info["username"]
                    }
                }
            }
        }

        async_to_sync(self.cons.channel_layer.group_send)(
                self.cons.room_name,
                send_info
        )
