import React from 'react';
import { connect } from 'react-redux';
import { withRouter, Redirect, Prompt } from 'react-router-dom';
import axios from '../../Services/axiosConfig';
import produce from 'immer';
import Board from './Board/Board';
import  classes from './GamePage.module.scss';
import { Container, Col, Row, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';
import UserCard from '../../components/UserCard/UserCard';
import UserMediaCard from '../../components/UserMediaCard/UserMediaCard';
import withErrorHandler from '../../hoc/withErrorHandler/withErrorHandler';
import * as actions from '../../store/actions/index';
import { boardSpotsInfo } from '../../Utilities/boardUtility';
import MyBtn from '../../components/UI/MyBtn/MyBtn';

class GamePage extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            winner: null,
            disconnection: false
        };

        this.onUnload = this.onUnload.bind(this); 
    }

    onUnload(event) { 
        event.returnValue = " ";
    }

    ws = this.props.location.data ? new WebSocket(this.props.location.data.WS_URL) : null;

    shouldComponentUpdate(nextProps, nextState) {
        if ((this.props.playerMarker === null) && (nextProps.playerMarker !== null))
        {
            return false;
        }
        return true;
    }

    componentDidMount () { 
        window.addEventListener("beforeunload", this.onUnload);

        if ((!this.ws) || (!this.props.location.data))
        {
            return;
        }

        this.ws.onopen = () => { 
        } 
     
        this.ws.onmessage = e => { 
            // listen to data sent from the websocket server 
            const msg = JSON.parse(e.data); 
            if (this.props.location.data.AImode)
            {
                this.WSPvAIreceivedData(msg); 
            }
            else
            {
                this.WSPvPreceivedData(msg); 
            }
        } 
     
        this.ws.onclose = () => { 
        } 
    } 

    componentWillUnmount() {
        window.removeEventListener("beforeunload", this.onUnload);

        if (this.ws) 
        {
            this.ws.close();
        }
    }


    WSsendData = (msg) => {
        const msgJSON = JSON.stringify(msg);
        this.ws.send(msgJSON);
    }

    WSPvAIreceivedData = (msg) => {
        if (msg.type === "gameAI")
        {

            if ((msg.data.player) && (!msg.data.AIbot))
            { // player has formed a mill - update game state
                msg.data.player["changePlayerTurn"] = true
                this.props.updateGameState(msg.data.player);
                return;
            }

            if ((msg.data.AIbot) && (!msg.data.player))
            { //  AIbot will form a mill at next move
                // send flag that an AI mill will be made at the next move
                const newGameState = {
                    "changeAImadeMill": true,
                    "AIgameOver": msg.data.AIgameOver
                }

                const AIbot = msg.data.AIbot;
                if (AIbot.action === "storeSourceDestCoord")
                {
                    this.props.storeSourceDestCoords(AIbot.sourceCoordId, boardSpotsInfo[AIbot.sourceCoordId].x, boardSpotsInfo[AIbot.sourceCoordId].y, AIbot.destCoordId, boardSpotsInfo[AIbot.destCoordId].x, boardSpotsInfo[AIbot.destCoordId].y, newGameState, /*AImode=*/true);
                }
                else if (AIbot.action === "triggerManMovement")
                {
                    this.props.triggerManMovement(AIbot.coordId, boardSpotsInfo[AIbot.coordId].x, boardSpotsInfo[AIbot.coordId].y, newGameState, /*AImode=*/true);
                }
                return;
            }

            //first AIbot's turn and then player's turn
            //update game state
            let newGameState = {...msg.data.player};
            newGameState["AIgameOver"] = msg.data.AIgameOver;

            const AIbot = msg.data.AIbot;

            if (AIbot.action === "storeSourceDestCoord")
            {
                this.props.storeSourceDestCoords(AIbot.sourceCoordId, boardSpotsInfo[AIbot.sourceCoordId].x, boardSpotsInfo[AIbot.sourceCoordId].y, AIbot.destCoordId, boardSpotsInfo[AIbot.destCoordId].x, boardSpotsInfo[AIbot.destCoordId].y, newGameState, /*AImode=*/true);
            }
            else if (AIbot.action === "triggerManMovement")
            {
                this.props.triggerManMovement(AIbot.coordId, boardSpotsInfo[AIbot.coordId].x, boardSpotsInfo[AIbot.coordId].y, newGameState, /*AImode=*/true);
            }
            else if (AIbot.action === "triggerRemovingManMovement")
            {
                this.props.triggerRemovingManMovement(AIbot.coordId, boardSpotsInfo[AIbot.coordId].x, boardSpotsInfo[AIbot.coordId].y, newGameState, /*AImode=*/true);
            }
        }
        else if (msg.type === "gameOver")
        {
            this.gameOver( msg.data.winner);
        }
    }

    WSPvPreceivedData = (msg) => {

        if (msg.type === "reflective")
        {
            this.execReflectiveAction(msg.data.action, msg.data.coordData);
        }
        else if (msg.type === "game")
        {
            this.props.updateGameState(msg.data[this.props.playerMarker], msg.data.playerTurn);
        }
        else if ( msg.type === "gameOver")
        {
            this.gameOver( msg.data.winner);
        }
        else if ( msg.type === "disconnection")
        {
            this.disconnection();
        }
    }

    execReflectiveAction = (action, coordData) => {
        if (action === "storeSourceCoords")
        {
            this.props.storeSourceCoords(coordData.coordId, coordData.coordX, coordData.coordY);
        }
        else if (action === "triggerManMovement")
        {
            this.props.triggerManMovement(coordData.coordId, coordData.coordX, coordData.coordY);
        }
        else if (action === "triggerRemovingManMovement")
        {
            this.props.triggerRemovingManMovement(coordData.coordId, coordData.coordX, coordData.coordY);
        }
        else if (action === "deselectBoardSpot")
        {
            this.props.deselectBoardSpot();
        }
    }

    gameOver = (winner) => {
        this.setState(
			produce( draft => {
				draft.winner = winner;
			})
		);
    }

    disconnection = () => {
        this.setState(
			produce( draft => {
				draft.disconnection = true;
			})
		);
    }

    modalContinueHandler = () => {
        this.props.history.goBack();
    }

    render() {

        if ((!this.props.location.data) || (!this.ws))
        {
            return (<Redirect to="/" />);
        }

        return (
            <>
                <Prompt
                    message={location =>
                        location.pathname === "/" && (this.state.winner || this.state.disconnection)
                        ? true
                        : "Are you sure you want to quit NMM Game ?"
                    }
                />

                <Modal 
                    id={classes.modal}
					isOpen={(this.state.winner !== null) || this.state.disconnection} 
                    size="md"  
                    fade  			    
				>
					<ModalHeader id={classes.modal_header}> 
						<span className={classes.modal_content}>
                            GAME OVER
                        </span>
					</ModalHeader>

					<ModalBody id={classes.modal_body}>
						{
                            this.state.winner ? 
                                (this.state.winner === this.props.playerMarker ? 
                                    <div className={classes.modal_content}> YOU WON !! Congratulations </div>
                                    :<div className={classes.modal_content}> You lost.. Don't worry better luck next time </div>
                                )
                            :<div> Opponent disconnected </div>
                        }  
                        <div className="mt-2"> Press "Continue" in order to be redirected and play again.. </div>
					</ModalBody>

					<ModalFooter className="p-2" id={classes.modal_footer}>
                        <MyBtn size="MD" borderWidth="4px" clickedHandler={this.modalContinueHandler}>
                            <span  style={{textShadow: "1px 1px 1px black"}}>
                                Continue
                            </span>
                        </MyBtn>
					</ModalFooter>
				</Modal>

                <Row id={classes.content}>
                    <Col xs="3" className={classes.side_col + (' d-none d-sm-block align-self-center p-0 m-0')}>
                        <div className="d-flex justify-content-end">
                            <UserCard name={this.props.playerXusername} surname="" playerMarker='X' img_src=""/>
                        </div>
                    </Col>

                    <Col xs="12" sm="6" id={classes.main_content}>
                        
                        <Container className="d-block d-sm-none h-25 pb-3">
                            <Row className="h-100 align-items-center">
                                <Col className={"d-flex justify-content-center mr-auto p-2"} >
                                    <UserMediaCard name={this.props.playerXusername} surname="" playerMarker='X'/>
                                </Col>

                                <Col className={"d-flex justify-content-center mr-auto p-2"} >
                                    <UserMediaCard  name={this.props.playerOusername} surname="" playerMarker='O'/>
                                </Col>
                            </Row>
                        </Container>

                        <div id={classes.game_area}>
                            <Board
                                WSsendData={this.WSsendData}
                                AImode={this.props.location.data.AImode}
                                gameOver={this.gameOver}
                            />
                        </div>
                    </Col>

                    <Col xs="3" className={classes.side_col + (' d-none d-sm-block align-self-center p-0 m-0')}>
                        <div className="d-flex justify-content-start">
                            <UserCard  name={this.props.playerOusername} surname="" playerMarker='O' img_src=""/>
                        </div>
                    </Col>

                </Row>  
            </>
        );
    }

}


const mapStateToProps = state => {
    return {
        playerXusername : state.gamePage.playersInfo["X"] ? state.gamePage.playersInfo["X"].username : null,
        playerOusername : state.gamePage.playersInfo["O"] ? state.gamePage.playersInfo["O"].username : null,

        playerMarker : state.board.playerMarker

    };
}

const mapDispatchToProps = dispatch => {
    return {        
        setPlayerMarker: (player_marker) => dispatch(actions.setPlayerMarker(player_marker)),

        storeSourceCoords: (coord, coord_x, coord_y) => dispatch(actions.storeSourceCoords(Number(coord), coord_x, coord_y)),
        storeSourceDestCoords: (source_coord_id, source_coord_x, source_coord_y, dest_coord_id, dest_coord_x, dest_coord_y, new_game_state, AI_mode) => dispatch(actions.storeSourceDestCoords(Number(source_coord_id), source_coord_x, source_coord_y, Number(dest_coord_id), dest_coord_x, dest_coord_y, new_game_state, AI_mode)),
        triggerManMovement: (coord, coord_x, coord_y, new_game_state, AI_mode) => dispatch(actions.triggerManMovement(Number(coord), coord_x, coord_y, new_game_state, AI_mode)),
        triggerRemovingManMovement: (coord, coord_x, coord_y, new_game_state, AI_mode) => dispatch(actions.triggerRemovingManMovement(Number(coord), coord_x, coord_y, new_game_state, AI_mode)),
        deselectBoardSpot: () => dispatch(actions.deselectBoardSpot()),

        updateGameState: (game_state_info, new_player_turn) => dispatch(actions.updateGameState(game_state_info, new_player_turn))
    }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(withErrorHandler( GamePage, axios )));

