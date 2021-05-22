# game_nmm/consumers.py

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from random import randrange,choices

from game_nmm import consumer_helper as ch
from game_nmm import consumer_threads as ct
from game_nmm import redis_management as rm


import json
import redis
import threading
import time
import string
import random

# every consumer has three function in common (connect, disconnect, receive) 
# the others are custom functions and are called because of events
# this functions are called because the json has type with the name of the function

class Game_NMMConsumer(WebsocketConsumer):


    def connect(self): 
        self.room_name=self.scope['url_route']['kwargs']['room_name']

        if not self.room_name.startswith('nmm_room_'):
            self.room_name="-1"
            self.close
        
        ch=rm.check_game_websocket(self.room_name,self.channel_name)
      
        if ch==-1:
            self.close()
        else:
            rm.initialize_board_info(self.room_name)

            async_to_sync(self.channel_layer.group_add)(
                self.room_name,
                self.channel_name
            )
            self.accept()
 
    def disconnect(self, close_code):
        if close_code==1006:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_name,
                self.channel_name
            )
        elif close_code==1001:

            send_info={
                'type': "closeall",
                'data': ""
            }

            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                send_info
            )            
            rm.delete_websocket(self.room_name)

        elif close_code==1000:
            self.close()

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data_type = text_data_json["type"]
        print(text_data)
        send_info={
            'type': data_type,
            'data': ch.receive_helper(data_type,text_data_json,self.room_name)
        }

        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            send_info
        )

    def closeall(self, event):
      
        rdata={
            "type" : "disconnection",
            "sender": "server"
        }
        self.send(text_data=json.dumps(rdata))
        self.close()


    def chat(self, event):
        data = event['data']
        self.send(text_data=json.dumps(data))

    def permission(self, event):
        pass

    def reflective(self, event):
   
        data = event['data']
        self.send(text_data=json.dumps(data))

    def game(self, event):
        data = event['data']
        self.send(text_data=json.dumps(data))
        # t1 = Timer(self)
        # t1.start()



class GameAI_NMMConsumer(WebsocketConsumer):

    def connect(self): 

        room_hash = ''.join(choices(string.ascii_letters + string.digits, k=randrange(16,24)))
        self.room_name='ai_nmm_room'+"_"+room_hash
        self.difficulty=self.scope['url_route']['kwargs']['difficulty']
        self.my_marker=self.scope['url_route']['kwargs']['player_marker']
        ch=rm.check_gameai_websocket(self.room_name,self.channel_name)
      
        if ch==-1:
            self.close()
        elif ch==-2:
            self.close()
        else:
            rm.initialize_board_info(self.room_name)

            async_to_sync(self.channel_layer.group_add)(
                self.room_name,
                self.channel_name
                )
            self.accept()
            if self.my_marker=='O':
                self.receive( json.dumps(
                    {
                        'type':"AI_move"}) )

    def disconnect(self, close_code):

        if close_code==1006:
            
            async_to_sync(self.channel_layer.group_discard)(
                self.room_name,
                self.channel_name
            )
        elif close_code==1001:

            send_info={
                'type': "closeall",
                'data': ""
            }

            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                send_info
            )            
            rm.delete_websocket(self.room_name)

        elif close_code==1000:
            self.close()

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text_data_json['my_marker']=self.my_marker
        text_data_json['difficulty']=self.difficulty
        data_type = text_data_json["type"]

            
        send_info={
            'type': data_type,
            'data': ch.receive_helper(data_type,text_data_json,self.room_name)
        }

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            send_info
        )

    def gameAI(self, event):
        data = event['data']
        self.send(text_data=json.dumps(data))

    def AI_move(self, event):
        data = event['data']
        self.send(text_data=json.dumps(data))

class LobbyConsumer(WebsocketConsumer):
    #if there is no lobby it is created when a user wants to join
    def connect(self): 
        self.uid=self.scope['url_route']['kwargs']['id']
        self.username=self.scope['url_route']['kwargs']['username']
        self.room_name="lobby"
        if not rm.lobby_exists():
            lm= ct.Lobby_Match(self)
            lm.start()

        rm.add_to_lobby(self.channel_name,self.uid,self.username) 
            
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
          )
        self.accept()

    def disconnect(self, close_code):
        rm.remove_from_lobby(self.channel_name,self.uid,self.username)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

        self.close()

    # Receive message from WebSocket
    def receive(self, text_data):
        pass
    
    def match(self, event):
        data=event["data"]
        pl_list= data["pl_list"]
        if self.channel_name == pl_list[0]:
            self.send(text_data=json.dumps(data["pl1"]))
        elif self.channel_name == pl_list[1]:
            self.send(text_data=json.dumps(data["pl2"]))
        else:
            return 
