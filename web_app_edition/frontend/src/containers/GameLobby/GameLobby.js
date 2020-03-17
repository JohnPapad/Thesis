import React from 'react';
import { connect } from 'react-redux';
import { withRouter, Redirect, Prompt } from 'react-router-dom';
import nmm_board_img_depth from '../../assets/images/nmm_board_depth.png';
import { Col, Row, Card } from 'reactstrap';
import  classes from './GameLobby.module.scss';
import PvAIlobby from './PvAIlobby/PvAIlobby';
import PvPlobby from './PvPlobby/PvPlobby';

class GameLobby extends React.Component {

    constructor(props) {
        super(props);
        this.onUnload = this.onUnload.bind(this); 
    }

    onUnload(event) { 
        event.returnValue = " ";
    }

    componentDidMount() {
       window.addEventListener("beforeunload", this.onUnload);
    }

    componentWillUnmount() {
        window.removeEventListener("beforeunload", this.onUnload);
    } 
   
    render() {

        if ((!this.props.location.data) || (!this.props.location.data.gameMode))
        {
            return (<Redirect to="/" />);
        }

        if ( (this.props.location.data.gameMode === "PvP") && (!this.props.isAuthed ) )
        {
            return (<Redirect to="/" />);
        }

        const AImode = this.props.location.data.gameMode === "PvAI";
        const NMMpanelStyle = {
            backgroundImage: `url(${nmm_board_img_depth})`,
        }

        return (
            <>
                <Prompt
                    message={location =>
                        location.pathname !== ("/game")
                        ? (AImode ? `Are you sure you want to exit PvAI Game Lobby ?` : `Are you sure you want to exit PvP Matchmaking ?`)
                        : true
                    }
                />

                <Row id={classes.content}>
                    <Col xs="12" sm="2" md="4"></Col>
                    <Col xs="12" sm="8" md="4" style={NMMpanelStyle} id={classes.nmm_panel} className="p-0"> 
                        <div className={classes.panel_bg_gradient}>
                            <Card className="h-100 border-0" style={{backgroundColor: "inherit", paddingTop: "8vh"}}> 
                                {
                                    AImode ? <PvAIlobby/>
                                    : <PvPlobby/>
                                }
                            </Card>
                        </div>
                    </Col>
                </Row>
            </>
        );

    }

}

const mapStateToProps = state => {
    return {
        isAuthed : state.auth.token ? true : false,
    }
}

export default withRouter( connect( mapStateToProps )( GameLobby ) );

