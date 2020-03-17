import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import nmm_board_img_depth from '../../assets/images/nmm_board_depth.png';
import { Container, Col, Row, Card, CardBody, CardFooter, Media } from 'reactstrap';
import  classes from './LandingPage.module.scss';
import MyBtn from '../../components/UI/MyBtn/MyBtn';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faRobot, faGlobeAmericas } from '@fortawesome/free-solid-svg-icons';

class LandingPage extends React.Component {


    render() {
        const rightPanelStyle = {
            backgroundImage: `url(${nmm_board_img_depth})`,
        }

        return (
            <Row id={classes.content}>
                <Col xs="12" sm="7" id={classes.left_panel} className="d-flex p-0"> 
                    <div className={classes.panel_bg_gradient}>
                        <Card className="h-100 border-0" style={{backgroundColor: "inherit", paddingTop: "8%"}}>
                            <CardBody id={classes.title} className="pb-0 pt-0 pr-0">
                                Welcome to Nine Men's Morris online
                            </CardBody>

                            <CardFooter className="d-none d-sm-block">
                                <Row className="justify-content-around">
                                    <Col xs="6" className="d-flex justify-content-center p-1">
                                        <div>
                                            <Media>
                                                <Media left middle>
                                                    <FontAwesomeIcon icon={faGlobeAmericas} size="6x" className="pr-2"/>
                                                </Media>
                                                <Media body>
                                                    <Media heading>
                                                        You can play competitive versus players from all over the world. 
                                                        The matchmaking system will make sure that that you will be matched with an opponent as soon as possible.
                                                        {/* Win ELO and climb at the top of the leaderboard. THE DARE IS TO DO !! */}
                                                    </Media>
                                                </Media>
                                            </Media>
                                        </div>
                                    </Col>
                                    
                                    <Col xs="6" className="d-flex justify-content-center p-1">
                                        <div>
                                            <Media>
                                                <Media left middle>
                                                    <FontAwesomeIcon icon={faRobot} size="6x" className="pr-2"/>
                                                </Media>
                                                <Media body>
                                                    <Media heading>
                                                        Or you can challenge yourself by playing against the powerful AI. 
                                                        Train yourself against the toughest opponent and be ready for competitive matchups.
                                                    </Media>
                                                </Media>
                                            </Media>
                                        </div>
                                    </Col>     
                                </Row>
                            </CardFooter>
                        </Card>
                    </div>
                </Col>

                <Col xs="12" sm="5" style={rightPanelStyle} id={classes.right_panel} className="p-0"> 
                    <div className={classes.panel_bg_gradient + " d-flex align-items-end justify-content-center"}>
                        <Container fluid className="mb-3">
                            <Row className="justify-content-around">
                                <Col xs="12" sm="auto" className="d-flex justify-content-center p-1 mb-3">
                                    <div>
                                        <Link 
                                            to={{   
                                                pathname: this.props.isAuthed ? '/gamelobby' : "/signin", 
                                                data: { 
                                                    gameMode: "PvP"
                                                } 
                                            }} 
                                        >
                                            <MyBtn borderWidth="6px">
                                                <span  style={{textShadow: "2px 2px 2px black"}}>
                                                    PLAY vs Player
                                                </span>
                                            </MyBtn>
                                        </Link>
                                    </div>
                                </Col>
                                
                                <Col xs="12" sm="auto" className="d-flex justify-content-center p-1 mb-3">
                                    <div>
                                        <Link 
                                            to={{   
                                                pathname: '/gamelobby', 
                                                data: { 
                                                    gameMode: "PvAI"
                                                } 
                                            }} 
                                        >
                                            <MyBtn borderWidth="6px">
                                                <span  style={{textShadow: "2px 2px 2px black"}}>
                                                    PLAY vs AI
                                                </span>
                                            </MyBtn>
                                        </Link>
                                    </div>
                                </Col>       
                            </Row>
                        </Container>
                    </div>
                </Col>

            </Row>
        );
    }

}

const mapStateToProps = state => {
    return {
        isAuthed : state.auth.token ? true : false,
    }
}

export default connect( mapStateToProps )( LandingPage ) ;
