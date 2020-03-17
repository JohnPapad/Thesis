import * as actionTypes from './actionTypes';

export const storeSourceCoords = (spot_coord, spot_coord_x, spot_coord_y) => {
    return {
        type: actionTypes.STORE_SOURCE_COORDS,
        sourceCoordId: spot_coord,
        sourceCoordX: spot_coord_x,
        sourceCoordY: spot_coord_y
    };
};

export const storeSourceDestCoords = (source_coord_id, source_coord_x, source_coord_y, dest_coord_id, dest_coord_x, dest_coord_y, new_game_state, AI_mode) => {
    return {
        type: actionTypes.STORE_SOURCE_DEST_COORDS,
        sourceCoordId: source_coord_id,
        sourceCoordX: source_coord_x,
        sourceCoordY: source_coord_y,
        destCoordId: dest_coord_id,
        destCoordX: dest_coord_x,
        destCoordY: dest_coord_y,
        newGameState: new_game_state,
        AImode: AI_mode
    };
};

export const triggerManMovement = (dest_coord, dest_coord_x, dest_coord_y, new_game_state, AI_mode) => {
    return {
        type: actionTypes.TRIGGER_MAN_MOVEMENT,
        destCoordId: dest_coord,
        destCoordX: dest_coord_x,
        destCoordY: dest_coord_y,
        newGameState: new_game_state,
        AImode: AI_mode
    };
};

export const triggerRemovingManMovement = (source_coord, source_coord_x, source_coord_y, new_game_state, AI_mode) => {
    return {
        type: actionTypes.TRIGGER_REMOVING_MAN_MOVEMENT,
        sourceCoordId: source_coord,
        sourceCoordX: source_coord_x,
        sourceCoordY: source_coord_y,
        newGameState: new_game_state,
        AImode: AI_mode
    };
};

export const completeRemovingManMovement = () => {
    return {
        type: actionTypes.COMPLETE_REMOVING_MAN_MOVEMENT
    }
};

export const markDestBoardSpot = () => {
    return {
        type: actionTypes.MARK_DEST_BOARD_SPOT
    }
};

export const deselectBoardSpot  = () => {
    return {
        type: actionTypes.DESELECT_BOARD_SPOT
    }
};

export const updateGameState = (game_state_info, new_player_turn) => {
    return {
        type: actionTypes.UPDATE_GAME_STATE,
        gameStateInfo: game_state_info,
        newPlayerTurn: new_player_turn
    }
};

export const changePlayerTurn  = () => {
    return {
        type: actionTypes.CHANGE_PLAYER_TURN
    }
};

export const changeAImadeMill  = () => {
    return {
        type: actionTypes.CHANGE_AI_MADE_MILL
    }
};

export const setPlayerMarker = (player_marker) => {
    return {
        type: actionTypes.SET_PLAYER_MARKER,
        playerMarker: player_marker
    }
};