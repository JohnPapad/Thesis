import * as actionTypes from './actionTypes';
import * as actions from './index';

export const updatePvAILobbyState = (players_info, player_marker) => {
    return dispatch => {
        dispatch(setPlayersInfo(players_info["X"], players_info["O"]));
        dispatch(setPlayBtnClicked());
        dispatch(actions.setPlayerMarker(player_marker));
    };
}

export const updatePvPLobbyState = (player_X, player_O, game_room_id, player_marker) => {
    return dispatch => {
        dispatch(setPlayersInfo(player_X, player_O));
        dispatch(setGameRoomId(game_room_id));
        dispatch(setGameLobbyPhase());
        dispatch(actions.setPlayerMarker(player_marker));
    };
}

export const setPlayersInfo = (player_X, player_O) => {
    return {
        type: actionTypes.SET_PLAYERS_INFO,
        playerX: player_X,
        playerO: player_O,
    };
};

export const setPlayBtnClicked = () => {
    return {
        type: actionTypes.SET_PLAY_BTN_CLICKED
    }
};

export const setGameLobbyPhase = () => {
    return {
        type: actionTypes.SET_GAME_LOBBY_PHASE
    }
};

export const setGameRoomId = (game_room_id) => {
    return {
        type: actionTypes.SET_GAME_ROOM_ID,
        gameRoomId: game_room_id
    }
};

