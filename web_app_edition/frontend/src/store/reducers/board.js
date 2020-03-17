import * as actionTypes from '../actions/actionTypes';
import { createEmptyBoard } from '../utility';
import { getAllBoardCoords } from '../utility';
import { EMPTY_MARKER } from '../utility';
import produce from "immer";

const sourceCoordsDefaults = {
    X: {
        sourceCoordX : -550,
        sourceCoordY : 0,
    },

    O: {
        sourceCoordX : 550,
        sourceCoordY : 0,
    }
}

const initialState = {
    board : [...createEmptyBoard()],

    highlightedSpots : [],
    notAllowedSpots : [],
    allowedSpots : [...getAllBoardCoords()],

    moveFinished: true,

    removeMan : false,
    movingManPhase :  null,

    sourceCoordId : null,
    sourceCoordX : sourceCoordsDefaults["X"].sourceCoordX,
    sourceCoordY : sourceCoordsDefaults["X"].sourceCoordY,

    destCoordId : null,
    destCoordX : null,
    destCoordY : null,

    placementPhase : true,
    playerTurn: "X",
    playerMarker: null,

    forfeit : false,
    winner : null,

    AImadeMill: false, // only used in AI mode 
    AIgameOver: false, // only used in AI mode
};


const getNextPlayerTurn = (playerTurn) => {
    return playerTurn === 'X' ? "O" : 'X';
}

const changeGamePhase = (draft) => {
    draft.placementPhase = false;
}

const changeRemoveManFlag = (draft) => {
    draft.removeMan = !draft.removeMan;
}

const changePlayerTurn = (draft) => {
    draft.moveFinished = true;
    draft.playerTurn = getNextPlayerTurn(draft.playerTurn);
}

const setPlayerMarker = (draft, playerMarker) => {
    draft.playerMarker = playerMarker;
}

const setAllowedSpots = (draft, allowedSpots) => {
    draft.allowedSpots = allowedSpots;
}

const setMovingManPhase = (draft, phase) => {
    draft.movingManPhase = phase;
};

const setBoardSpot = (draft, coordId, MARKER) => {
    draft.board[coordId] = MARKER;
};

const setSourceCoords = (draft, sourceCoordId, sourceCoordX, sourceCoordY) => {
    draft.sourceCoordId = sourceCoordId;
    draft.sourceCoordX = sourceCoordX;
    draft.sourceCoordY = sourceCoordY;
};

const setDestCoords = (draft, destCoordId, destCoordX, destCoordY) => {
    draft.destCoordId = destCoordId;
    draft.destCoordX = destCoordX;
    draft.destCoordY = destCoordY;
};

const resetSourceCoords = ( draft, playerMarker ) => {
    draft.sourceCoordId = null;
    draft.sourceCoordX = sourceCoordsDefaults[playerMarker].sourceCoordX;
    draft.sourceCoordY = sourceCoordsDefaults[playerMarker].sourceCoordY;
};

const changeAImadeMill = (draft) => {
    draft.AImadeMill = !draft.AImadeMill;
}

const setAIgameOver = (draft) => {
    draft.AIgameOver = true;
}

//---------------------------------------------------------

const triggerManMovementAction = (draft, action) => {
    setDestCoords(draft, action.destCoordId, action.destCoordX, action.destCoordY);
    setMovingManPhase(draft, "execManMovement");
    if (!draft.placementPhase) 
    { 
        setBoardSpot(draft, draft.sourceCoordId, EMPTY_MARKER);
    }

    if ((action.AImode) && (action.newGameState))
    {
        updateGameStateAction(draft, action.newGameState, true);
    }
}

const triggerRemovingManMovementAction = (draft, action) => {
    setSourceCoords(draft, action.sourceCoordId, action.sourceCoordX, action.sourceCoordY);
    setDestCoords(draft, null, 0, 600);
    setMovingManPhase(draft, "execManMovement");
    setBoardSpot(draft, action.sourceCoordId, EMPTY_MARKER); 
    
    if ((action.AImode) && (action.newGameState))
    {
        updateGameStateAction(draft, action.newGameState, true);
    }
}

const updateGameStateAction = (draft, gameStateInfo, AImode) => {
    draft.moveFinished = true;
    
    if ((AImode) && (gameStateInfo.changeAImadeMill))
    {
        changeAImadeMill(draft);
    }

    if ((AImode) && (gameStateInfo.AIgameOver))
    {
        setAIgameOver(draft);
    }

    if (gameStateInfo.changeGamePhase)
    {
        changeGamePhase(draft);
    }

    if (gameStateInfo.changePlayerTurn)
    {
        if (draft.placementPhase)
        {
            resetSourceCoords(draft, getNextPlayerTurn(draft.playerTurn));
        }
        changePlayerTurn(draft);
    }

    if (gameStateInfo.allowedSpots)
    {
        setAllowedSpots(draft, gameStateInfo.allowedSpots);
    }

    if (gameStateInfo.removeMan)
    {
        changeRemoveManFlag(draft);
    }
}


const reducer = ( state = initialState, action ) => 
    produce(state, draft => {

        switch ( action.type ) {
            case actionTypes.STORE_SOURCE_DEST_COORDS: //only used in AI mode

                setSourceCoords(draft, action.sourceCoordId, action.sourceCoordX, action.sourceCoordY);
                setDestCoords(draft, action.destCoordId, action.destCoordX, action.destCoordY);
                setMovingManPhase(draft, "storedSourceCoords");

                if ((action.AImode) && (action.newGameState))
                {
                    updateGameStateAction(draft, action.newGameState, true);
                }
                return;

            // all other cases can be used in both AI and PVP modes ------------

            case actionTypes.STORE_SOURCE_COORDS: 
                setSourceCoords(draft, action.sourceCoordId, action.sourceCoordX, action.sourceCoordY);
                setMovingManPhase(draft, "storedSourceCoords");
                return;

            case actionTypes.TRIGGER_MAN_MOVEMENT: 
                triggerManMovementAction(draft, action);
                return;

            case actionTypes.TRIGGER_REMOVING_MAN_MOVEMENT: 
                triggerRemovingManMovementAction(draft, action);
                return;

            case actionTypes.COMPLETE_REMOVING_MAN_MOVEMENT: 
                draft.moveFinished = false;
                setMovingManPhase(draft, "manMovementCompleted");
                changeRemoveManFlag(draft);
                return;

            case actionTypes.MARK_DEST_BOARD_SPOT: 
                draft.moveFinished = false;
                setMovingManPhase(draft, "manMovementCompleted");
                setBoardSpot(draft, draft.destCoordId, draft.playerTurn);
                return;

            case actionTypes.DESELECT_BOARD_SPOT: 
                resetSourceCoords(draft, draft.playerTurn);
                setMovingManPhase(draft, "manDeselected");
                return;

            case actionTypes.UPDATE_GAME_STATE:
                updateGameStateAction(draft, action.gameStateInfo);
                return;

            case actionTypes.CHANGE_PLAYER_TURN:
                if (draft.placementPhase)
                {
                    resetSourceCoords(draft, getNextPlayerTurn(draft.playerTurn));
                }
                changePlayerTurn(draft);
                return;

            case actionTypes.CHANGE_AI_MADE_MILL:
                changeAImadeMill(draft);
                return;

            case actionTypes.SET_PLAYER_MARKER:
                setPlayerMarker( draft, action.playerMarker );
                return;
            
            default: 
                return state; 
        }
    });


export default reducer;