import React from 'react';
import { connect } from 'react-redux';
import { Redirect } from 'react-router-dom';
import { CardBody, CardFooter,} from 'reactstrap';
import  classes from '../GameLobby.module.scss';
import { WS_URL_PVP, WS_URL_LOBBY } from '../../../Services/Websockets';
import { Spinner } from 'reactstrap';
import * as actions from '../../../store/actions';


class PvPlobby extends React.Component {

    ws = new WebSocket(WS_URL_LOBBY + this.props.userId + "/" + this.props.username + "/");

    componentDidMount () { 
        this.ws.onopen = () => { 
        } 
     
        this.ws.onmessage = e => { 
            // listen to data sent from the websocket server 
            const msg = JSON.parse(e.data); 
            this.WSreceivedData(msg); 
        } 
     
        this.ws.onclose = () => { 
        }          
    } 

    componentWillUnmount() {
        this.ws.close();
    }

    //------------------------------

    WSreceivedData = (msg) => {
        const ownPlayerInfo = {
            userId : this.props.userId,
            username: this.props.username,
        }

        let playerX = null;
        let playerO = null;
        if (msg.marker === 'X')
        {
            playerX = {...ownPlayerInfo};
            playerO = {...msg.opponent}
        }
        else
        {
            playerX = {...msg.opponent}
            playerO = {...ownPlayerInfo};
        }

        this.props.updatePvPLobbyState(playerX, playerO, msg.room, msg.marker);
    }

    renderSearchingMsg = () => {
        return (
            <span id={classes.searching_footer}>
                Searching for opponent ...
            </span>
        );
    }

    render () {
        
        if (!this.props.searching)
        {
            const WS_URL = WS_URL_PVP + this.props.gameRoomId + '/';
            return (
                <Redirect 
                    to={{   
                        pathname: '/game', 
                        data: { 
                            AImode: false,
                            WS_URL: WS_URL
                        } 
                    }} 
                />
            );
        }

        return (
            <>
                <CardBody className="d-flex justify-content-center pr-3 pl-3 pt-4">
                    {
                        this.props.searching ?
                            < Spinner id={classes.spinner} />
                        : null
                    }

                </CardBody>

                <CardFooter className="d-flex justify-content-center pb-4 pt-4">
                    {
                        this.props.searching ?
                            this.renderSearchingMsg()
                        : null
                    }

                </CardFooter>
            </>
        );
    }

}

const mapStateToProps = state => {
    return {
        userId : state.auth.userId,
        username: state.auth.username,
        searching: state.gamePage.searching,
        gameRoomId: state.gamePage.gameRoomId
    }
}

const mapDispatchToProps = dispatch => {
    return {
        updatePvPLobbyState: (player_X, player_O, game_room_id, player_marker) => dispatch(actions.updatePvPLobbyState(player_X, player_O, game_room_id, player_marker)),
    }
} 

export default connect( mapStateToProps, mapDispatchToProps )( PvPlobby ) ;