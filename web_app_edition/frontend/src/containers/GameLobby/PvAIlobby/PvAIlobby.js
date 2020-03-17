import React from 'react';
import { connect } from 'react-redux';
import produce from 'immer';
import { Redirect } from 'react-router-dom';
import { Col, Row, CardBody, CardFooter, Form, FormGroup, Label, Input } from 'reactstrap';
import  classes from '../GameLobby.module.scss';
import MyBtn from '../../../components/UI/MyBtn/MyBtn';
import { WS_URL_PVAI } from '../../../Services/Websockets';
import * as actions from '../../../store/actions';


class PvAIlobby extends React.Component {

    state = {
        formControls: {
            radios: {
                hard: false,
                easy: false,
                normal: true
            },

            currRadio: "normal",
            playFirst: true
        }
    }

    inputChangedHandler = (e, elemName, isCheckbox) => {
        if (isCheckbox)
        {
            this.setState(
                produce( draft => {
                    draft.formControls.playFirst = !draft.formControls.playFirst;
                })
            )
            return;
        }

        if (elemName === this.state.formControls.currRadio)
        {
            return;
        }

        this.setState(
            produce( draft => {
                draft.formControls.radios[draft.formControls.currRadio] = !draft.formControls.radios[draft.formControls.currRadio];
                draft.formControls.radios[elemName] = !draft.formControls.radios[elemName];
                draft.formControls.currRadio = elemName;
            })
        );

    }

    getPlayerMarker = () => {
        if (this.state.formControls.playFirst)
        {
            return "X";
        }
        else
        {
            return "O";
        }
    }

    getPlayersInfo = () => {
        const ownPlayerInfo = {
            username: this.props.username,
            userId: this.props.userId
        };

        const AIbotPlayerInfo = {
            username: "AI bot"
        };

        if (this.getPlayerMarker() === 'X')
        {
            return {
                X: {...ownPlayerInfo},
                O: {...AIbotPlayerInfo}
            };
        }
        else
        {
            return {
                X: {...AIbotPlayerInfo},
                O: {...ownPlayerInfo}
            };
        }
    }

    render () {

        if (this.props.playBtnClicked)
        {
            return (
                <Redirect 
                    to={{   
                        pathname: '/game', 
                        data: { 
                            AImode: true,
                            WS_URL: WS_URL_PVAI + this.getPlayerMarker() + "/" + this.state.formControls.currRadio + "/"
                        } 
                    }} 
                />
            );
        }

        return (
            <>
                <CardBody className="pr-5 pl-5 pt-0">
                    <Form id={classes.form} className="pr-0 pl-3 pt-2 pb-2">
                        <Row form>
                            <Col xs={12} className={classes.form_title + " d-flex justify-content-start"}>
                                AI Difficulty
                            </Col>
                        </Row>

                        <Row form className="pb-2">
                            <Col xs={12} className="d-flex justify-content-around">
                                <FormGroup check inline>
                                    <Label check>
                                        <Input type="radio" checked={this.state.formControls.radios.easy} onChange={ (e) => this.inputChangedHandler(e, "easy")}/> Easy
                                    </Label>
                                </FormGroup>

                                <FormGroup check inline>
                                    <Label check>
                                        <Input type="radio" checked={this.state.formControls.radios.normal} onChange={ (e) => this.inputChangedHandler(e, "normal")}/> Normal
                                    </Label>
                                </FormGroup>

                                <FormGroup check inline>
                                    <Label check>
                                        <Input type="radio" checked={this.state.formControls.radios.hard} onChange={ (e) => this.inputChangedHandler(e, "hard")}/> Hard
                                    </Label>
                                </FormGroup>
                            </Col>
                        </Row>

                        <Row form>
                            <Col xs={12} className="d-flex justify-content-start">
                                <FormGroup check inline>
                                    <Label check className={classes.form_title}>
                                        <Input type="checkbox" checked={this.state.formControls.playFirst} onChange={ (e) => this.inputChangedHandler(e, "playFirst", true) } />
                                        Play First
                                    </Label>
                                </FormGroup>
                            </Col>
                        </Row>
                        
                    </Form>
                </CardBody>

                <CardFooter className="d-flex justify-content-center pb-4 pt-4">
                    <MyBtn borderWidth="6px" clickedHandler={() => this.props.updatePvAILobbyState( this.getPlayersInfo(), this.getPlayerMarker() )}>
                        <span  style={{textShadow: "3px 3px 2px black"}}>
                            PLAY NOW
                        </span>
                    </MyBtn>
                </CardFooter>
            </>
        );
    }

}

const mapStateToProps = state => {
    return {
        userId : state.auth.userId,
        username: state.auth.username ? state.auth.username : "Anonymous Player",
        playBtnClicked: state.gamePage.playBtnClicked,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        updatePvAILobbyState: (players_info, player_marker) => dispatch(actions.updatePvAILobbyState(players_info, player_marker)),
    }
} 


export default connect( mapStateToProps, mapDispatchToProps )( PvAIlobby ) ;