import React from 'react';
import BoardSpot from './BoardSpot/BoardSpot';
import MovingBoardSpot from './BoardSpot/MovingBoardSpot';
import classes from './BoardSpots.module.css';
import { connect } from 'react-redux';
import * as actions from '../../store/actions/index';
import { boardSpotsInfo } from '../../Utilities/boardUtility';

const MOVE_DUR = 2; // in seconds

class BoardSpots extends React.Component {

    shouldComponentUpdate(nextProps, nextState) {
        if ((this.props.playerMarker === null) && (nextProps.playerMarker !== null))
        {
            return false;
        }

        if ((this.props.movingManPhase === "manMovementCompleted") && (nextProps.movingManPhase === "manMovementCompleted"))
        {
            return false;
        }

        return true;
    }

    componentDidUpdate () {

        if (this.props.movingManPhase === "execManMovement")
        { // man movement has been executed
            let func = null;
            if (this.props.removeMan)
            { // reset source spot coords
                func = this.props.completeRemovingManMovement;
            }
            else
            { // mark destination spot with player's marker
                func = this.props.markDestBoardSpot;
            }
            setTimeout(func, MOVE_DUR * 1000);
        }
        else if ((this.props.movingManPhase === "storedSourceCoords") && (this.props.AImode) && (!this.props.myTurn))
        { // we are in AI mode - both source and destination coords have been set - ready to perform spot movement
            setTimeout(this.props.triggerManMovement, 500, this.props.destCoordId, this.props.destCoordX, this.props.destCoordY, null, true);
        }
        else if (this.props.movingManPhase === "manMovementCompleted")
        {
            if (this.props.AImode)
            {
                if (this.props.myTurn)
                {
                    this.props.changePlayerTurn();
                    this.props.WSsendData( this.createWSmsg({ action: "updateGameState", newBoardState: this.props.board }, "gameAI") );
                }
                else
                {
                    if (this.props.AImadeMill) // send ws msg to sever with new board state - AI has formed a mill
                    {
                        this.props.changeAImadeMill();   //change the flag value
                        this.props.WSsendData( this.createWSmsg({ action: "updateGameState", newBoardState: this.props.board }, "gameAI") );
                    }
                    else // it was AI's turn now it will be player's turn - no need to send ws msg to server
                    { // just to change player Turn
                        if (this.props.AIgameOver)
                        {
                            this.props.gameOver(this.getOpponentMarker());
                        }
                        else
                        {
                            this.props.changePlayerTurn();
                        }
                    }
                }
            }
            else
            {
                if (this.props.myTurn)
                { // inform server to update game state with new board 
                    this.props.WSsendData( this.createWSmsg({ action: "updateGameState", newBoardState: this.props.board }, "game") );
                }
                else 
                { // inform server that player is ready to receive new game state (all UI changes have been completed)
                    this.props.WSsendData( this.createWSmsg({ action: "sendNewGameState" }, "permission") );
                }
            }
        }
    }

    createWSmsg = (data, type = null) => {
        return {
            type: type ? type : "reflective",
            sender: this.props.playerMarker,
            data: data
        };
    }

    createCoordData = (coordId, coordX, coordY) => {
        return {
            coordId: coordId,
            coordX: coordX,
            coordY: coordY
        };
    }

    getOpponentMarker = () => {
        return this.props.playerMarker === 'X' ? "O" : 'X';
    }

    getRemovingManColor = () => {
        if (this.props.myTurn)
        {
            return this.getOpponentMarker();
        }
        else
        {
            return this.props.playerMarker;
        }
    }

    render() {

        const renderMovingSpot = this.props.movingManPhase === "execManMovement";
        let movingBoardSpotMarker = null;
        if (renderMovingSpot)
        {
            movingBoardSpotMarker = !this.props.removeMan ? this.props.playerTurn : this.getRemovingManColor();
        }

        return (
            <g id={classes.svg_g}>
                {
                    Object.keys(boardSpotsInfo).map((coordId, i) => (
                        <BoardSpot key={boardSpotsInfo[coordId].coordId} 
                            boardSpotInfo={boardSpotsInfo[coordId]} 
                            r={this.props.r} 
                            spotSelectedHandler={() => this.spotSelectedHandler(boardSpotsInfo[coordId].coordId, boardSpotsInfo[coordId].x, boardSpotsInfo[coordId].y)} 
                            selectedSpotFlag={this.getSelectedSpotFlag(boardSpotsInfo[coordId].coordId)} 
                            playerMarker={this.props.board[boardSpotsInfo[coordId].coordId]}
                        /> 
                    ))
                }

                {
                    renderMovingSpot ?
                    <MovingBoardSpot x={this.props.sourceCoordX} y={this.props.sourceCoordY} r={this.props.r} playerMarker={movingBoardSpotMarker} shadowColor="#009900" isHighlighted={false} 
                        moveDuration={MOVE_DUR}
                        transFrom="0 0" 
                        transTo={(this.props.destCoordX - this.props.sourceCoordX).toString() + " " + (this.props.destCoordY - this.props.sourceCoordY).toString()}
                    />
                    : null
                }
            </g>
        );
    }

    callFunctionWithSpotCoords = (action, args) => {
        if (!this.props.AImode)
        { // PvP mode
            this.props.WSsendData( this.createWSmsg({ action: action, coordData: this.createCoordData(...args) }) );
        }
        else // PvAI mode
        { // action indicates function name in this case
            this["props"][action](...args); 
        }
    }
    
    getSelectedSpotFlag = (spot_coord)  => {
        return (  (this.props.sourceCoordId  === spot_coord) && (this.props.movingManPhase === "storedSourceCoords") && (this.props.movingPhase) ) ;
    }

    spotSelectedHandler = (spot_coord, spot_coord_x_str, spot_coord_y_str) => {
        const spot_coord_x = Number(spot_coord_x_str);
        const spot_coord_y = Number(spot_coord_y_str);

        if (!this.props.myTurn)
        {
            return;
        }
        else
        {
            if (!this.props.moveFinished)
            {
                return;
            }
        }


        if (this.props.movingManPhase === "execManMovement") 
        { // man movement is ongoing. player must wait to be completed
            return;
        }

        if (this.getSelectedSpotFlag(spot_coord) === true)
        { // player has chosen as destination spot the source spot, so the chosen spot will be deselected
            this.callFunctionWithSpotCoords("deselectBoardSpot", []);
            return;
        }

        if (this.props.allowedSpots.includes(spot_coord))
        {
            if (this.props.removeMan)
            { // player chooses a rival man to be removed from the board
                this.callFunctionWithSpotCoords("triggerRemovingManMovement", [spot_coord, spot_coord_x, spot_coord_y]);
                return;
            }

            if (this.props.movingPhase)
            { // moving phase: players can move their men on the board

                if ( (this.props.movingManPhase === "manMovementCompleted") || (this.props.movingManPhase === "manDeselected") ) //|| (this.props.movingManPhase === null))
                { // man chooses the coords of one of his men on board, who will be moved on the next step
                    this.callFunctionWithSpotCoords("storeSourceCoords", [spot_coord, spot_coord_x, spot_coord_y]);
                }
                else if (this.props.movingManPhase === "storedSourceCoords")
                { // player has already chosen source man's coords and now chooses destination board spot's coords to move his selected man
                    this.callFunctionWithSpotCoords("triggerManMovement", [spot_coord, spot_coord_x, spot_coord_y]);                
                }
            }
            else 
            { // placement phase: players can only place one of their men at a time on the board
                // first this will be executed
                // player chooses a board spot to place one of his men
                this.callFunctionWithSpotCoords("triggerManMovement", [spot_coord, spot_coord_x, spot_coord_y]);
            }

        }
    }
}

const mapStateToProps = state => {
    return {
        movingPhase : !state.board.placementPhase,
        
        board : state.board.board,
        allowedSpots : getAllowedSpots(state.board, state.board.playerTurn === state.board.playerMarker),

        AImadeMill : state.board.AImadeMill,
        AIgameOver: state.board.AIgameOver,

        moveFinished: state.board.moveFinished,
        removeMan : state.board.removeMan,

        movingManPhase : state.board.movingManPhase,
        myTurn : state.board.playerTurn === state.board.playerMarker,
        playerTurn : state.board.playerTurn,
        playerMarker : state.board.playerMarker,
        
        sourceCoordId  : state.board.sourceCoordId ,
        sourceCoordX : state.board.sourceCoordX,
        sourceCoordY : state.board.sourceCoordY,
        
        destCoordId : state.board.destCoordId,
        destCoordX : state.board.destCoordX,
        destCoordY : state.board.destCoordY
    };
}

const mapDispatchToProps = dispatch => {
    return {
        storeSourceCoords: (coord, coord_x, coord_y) => dispatch(actions.storeSourceCoords(Number(coord), coord_x, coord_y)),
        triggerManMovement: (coord, coord_x, coord_y) => dispatch(actions.triggerManMovement(Number(coord), coord_x, coord_y)),
        triggerRemovingManMovement: (coord, coord_x, coord_y) => dispatch(actions.triggerRemovingManMovement(Number(coord), coord_x, coord_y)),
        completeRemovingManMovement: () => dispatch(actions.completeRemovingManMovement()),
        markDestBoardSpot: () => dispatch(actions.markDestBoardSpot()),
        deselectBoardSpot: () => dispatch(actions.deselectBoardSpot()),
        updateGameState: (game_state_info, new_player_turn) => dispatch(actions.updateGameState(game_state_info, new_player_turn)),
        changePlayerTurn: () => dispatch(actions.changePlayerTurn()),
        changeAImadeMill: () => dispatch(actions.changeAImadeMill())
    }
}

const getAllowedSpots = (boardState, myTurn) => {
    if (!myTurn)
    {
        return null;
    }
    
    if (boardState.removeMan || boardState.placementPhase)
    { 
        return boardState.allowedSpots;
    }
    
    // movingPhase and no man should be removed 
    if (boardState.movingManPhase === "storedSourceCoords")
    { 
        return boardState.allowedSpots[(boardState.sourceCoordId).toString()];
    }

    // no source spot has been selected - return a list of all (own) men that could be moved
    return (Object.keys(boardState.allowedSpots)).map(Number);
}

export default connect(mapStateToProps, mapDispatchToProps)( BoardSpots ); 
