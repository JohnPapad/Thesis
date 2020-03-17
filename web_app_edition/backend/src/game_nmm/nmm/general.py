
def find_move(old_board,new_board):
    difs=[]

    if old_board==new_board:
        return "no_move" ,difs
    for i in range(0,24):
        if not old_board[i]==new_board[i]:
            if new_board[i]=='#':
                difs.insert(0,i)
                type_m='remove'
            else :
                difs.append(i)
                type_m='add'
    if len(difs)==1:
        return type_m ,difs
    elif len(difs)==2:
        return "move" ,difs
    else:
        return "wrong" , []


def make_PVP_json(gameState,receiver,allowedSpots,allowedSpotsmoves,changeGamePhase):

    data={'sender':'server'}

    if gameState=="gameOver":
        data['type']=gameState
        newElo={
                'X':800,
                'O':900
            }
        qdata={
            'winner':receiver,
            'newElo':newElo
        }
        data["data"]=qdata
        return data

    data['type']='game'

    qdata={'playerTurn':receiver}
    if gameState in ["movingMan" , "placingMan"]:
        qdata['X']={
            'changePlayerTurn':True}
        qdata['O']={
            'changePlayerTurn':True}
    else:
        qdata['X']={
            'removeMan':True}
        qdata['O']={
            'removeMan':True}

    if gameState in ["removingMan" , "placingMan"]:
        qdata[receiver]['allowedSpots']=allowedSpots
    else:
        allowedSpotsdict={}
        for i in range(0,len(allowedSpots)):
            allowedSpotsdict[int(allowedSpots[i])]=allowedSpotsmoves[i]
        qdata[receiver]['allowedSpots']=allowedSpotsdict

    if changeGamePhase==True:
        qdata['X']['changeGamePhase']=changeGamePhase
        qdata['O']['changeGamePhase']=changeGamePhase
    data['data']=qdata

    return data


def make_PVAI_json(gameState,receiver,allowedSpots,allowedSpotsmoves,changeGamePhase,ai_action,coord2,coord):

    data={'sender':'server'}

    if gameState=="MYgameOver":
        data['type']="gameOver"
        qdata={
            'winner':receiver,
        }
        data["data"]=qdata
        return data

    player={}
    AIbot={}

    data['type']='gameAI'

    if not gameState=="AIgameOver":
        if gameState in ["removingMan" , "placingMan"]:
            player={'allowedSpots':allowedSpots}
        elif gameState=="movingMan":
            allowedSpotsdict={}
            for i in range(0,len(allowedSpots)):
                allowedSpotsdict[int(allowedSpots[i])]=allowedSpotsmoves[i]
            player={'allowedSpots':allowedSpotsdict}

        if gameState=="removingMan" or ai_action=="triggerRemovingManMovement":
            player['removeMan']=True

        if changeGamePhase==True:
            player['changeGamePhase']=changeGamePhase
        
    if ai_action in ["triggerRemovingManMovement","triggerManMovement"]:  
        AIbot={'action':ai_action}
        AIbot['coordId']=coord
    elif ai_action=="storeSourceDestCoord":
        AIbot={'action':ai_action}
        AIbot['destCoordId']=coord
        AIbot['sourceCoordId']=coord2

    if not gameState=="AIgameOver":
        if player!={}:
            PlaAI={'player':player}
            if AIbot!={}:
                PlaAI['AIbot']=AIbot
        else :
            PlaAI={'AIbot':AIbot}
    else:
        if ai_action=="triggerRemovingManMovement":
            player={'removeMan':True}
        PlaAI={'player':player}
        PlaAI['AIbot']=AIbot
        PlaAI['AIgameOver']=True

    data['data']=PlaAI
    if coord2==-2:
        data['data']['firstMove']=True
    return data