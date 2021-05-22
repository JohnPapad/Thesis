from game_nmm.nmm import PvP as pvp
from game_nmm.nmm import PvAI as pvai
from game_nmm.nmm import general as gn
from game_nmm import redis_management as rm

def receive_helper(data_type,text_data_json,room_name): 
    #just a "cool" way to call functions globals has the names of all the functions inside his file
    #we find the function and we call is using strings
    func=data_type+"_helper"
    if func in globals():
        return eval(func+'(text_data_json,room_name)')
    else: 
        return no_helper()


def chat_helper(data,room_name):
    return {
        'type' : 'chat',
        'message' : data["message"],
        'sender' :data["sender"]
    }

def permission_helper(data,room_name):
    rm.give_permission(room_name)
    return {"ok":1}


def reflective_helper(data,room_name):
    tdata=data['data']
    action=tdata['action']
    actions=["triggerManMovement","storeSourceCoords",
    "deselectBoardSpot","triggerRemovingManMovement"]
    if action in actions:
        return data
    else:
        return {
            'error': True,
            'reason':'Action not found'
        }

def game_helper(data,room_name):

    tdata=data["data"]
    action=tdata['action']

    if action=="updateGameState":
        sender=data['sender']
        board=tdata['newBoardState']
        gameState,receiver,allowedSpots,allowedSpotsmoves,changeGamePhase=pvp.Game(room_name,sender,board)

        rm.wait_for_permission(room_name)
        return gn.make_PVP_json(gameState,receiver,allowedSpots,allowedSpotsmoves,changeGamePhase)

    return {
        'error': True,
        'reason':'Action not found'
    }


def AI_move_helper(data,room_name):
    my_marker=data["my_marker"]
    difficulty=data["difficulty"]
    gameState,receiver,allowedSpots,allowedSpotsmoves,changeGamePhase,ai_action,coord2,coord=pvai.make_first_move(room_name,my_marker,difficulty)
    return gn.make_PVAI_json(gameState,receiver,allowedSpots,allowedSpotsmoves,changeGamePhase,ai_action,coord2,coord)


def gameAI_helper(data,room_name):

    tdata=data["data"]
    my_marker=data['my_marker']
    difficulty=data["difficulty"]
    action=tdata['action']

    if action=="updateGameState":
        board=tdata['newBoardState']

        gameState,receiver,allowedSpots,allowedSpotsmoves,changeGamePhase,ai_action,coord2,coord=pvai.Game(room_name,board,my_marker,difficulty)

        return gn.make_PVAI_json(gameState,receiver,allowedSpots,allowedSpotsmoves,changeGamePhase,ai_action,coord2,coord)

        
    return {
            'error':True,
            'reason':'Not implemented yet'
            }

def no_helper():
    return {
        'error':True,
        'reason':'Type not found'
        }