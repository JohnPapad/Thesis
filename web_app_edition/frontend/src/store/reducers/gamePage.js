import * as actionTypes from '../actions/actionTypes';
import produce from "immer";

const initialState = {
    searching: true,
    gameRoomId: null,

    playBtnClicked: false,

    playersInfo : {
        X : null,
        O : null
    },

    timers : {
        X : 10,
        O : 10
    }
}


const setPlayBtnClicked = (state, action) => {
    return produce(state, draft => {
        draft.playBtnClicked = true;
    })
}

const setPlayersInfo = (state, action) => {
    return produce(state, draft => {
        draft.playersInfo.X = action.playerX;
        draft.playersInfo.O = action.playerO;
    })
}

const setGameRoomId = ( state, action ) => {
    return produce(state, draft => {
        draft.gameRoomId = action.gameRoomId;
    });
}

const setGameLobbyPhase = ( state, action ) => {
    return produce(state, draft => {
        draft.searching = false;
    });
}


const reducer = ( state = initialState, action ) => {
    switch ( action.type ) {
        case actionTypes.SET_PLAYERS_INFO: return setPlayersInfo( state, action );
        case actionTypes.SET_GAME_ROOM_ID: return setGameRoomId( state, action );
        case actionTypes.SET_GAME_LOBBY_PHASE: return setGameLobbyPhase( state, action );
        case actionTypes.SET_PLAY_BTN_CLICKED: return setPlayBtnClicked( state, action );

        default: return state;
    }
};

export default reducer;