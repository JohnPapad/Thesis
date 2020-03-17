export const EMPTY_MARKER = "#";

export const updateObject = (oldObject, updatedProperties) => {
    return {
        ...oldObject,
        ...updatedProperties
    };
};

export const createEmptyBoard = () => {
    let board = [];
    for (let i=0; i<24; i++) {
      board.push(EMPTY_MARKER);
    }
    return board;
}

export const getAllBoardCoords = () => {
    let coords = [];
    for (let i=0; i<24; i++) {
      coords.push(i);
    }
    return coords;
}

