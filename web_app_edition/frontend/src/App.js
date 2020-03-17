import React, { Component } from 'react';
import { connect } from 'react-redux';
import './App.css';
import Layout from './hoc/Layout/Layout';
import GamePage from './containers/GamePage/GamePage' ;
import { Route, Redirect, Switch, withRouter } from 'react-router-dom';
import { Container } from 'reactstrap';
import SignIn from './containers/SignIn/SignIn';
import SignUp from './containers/SignUp/SignUp';
import LogOut from './containers/LogOut/LogOut';
import LandingPage from './containers/LandingPage/LandingPage';
import GameLobby from './containers/GameLobby/GameLobby';
import * as actions from './store/actions';


class App extends Component {

    componentDidMount () {    
        window.addEventListener("popstate", () => {
            if (this.props.location.pathname === "/")
            {
                this.props.resetBoardGameState();
            }
            
        });
    }

    unAuthRoutes = () => {
        return(
			<Switch>

                <Route 
					path={["/"]} 
					exact
                    render={() => ( < LandingPage /> )}
				/>

                <Route 
					path={["/gamelobby"]} 
					exact
                    render={() => ( < GameLobby /> )}
				/>

                <Route 
					path={["/game"]} 
					exact
                    render={() => ( <GamePage /> )}
				/>

				<Route 
					path={["/signin"]} 
					exact
                    render={() => ( < SignIn /> )}
				/>

                <Route 
					path={["/signup"]} 
					exact
                    render={() => ( < SignUp /> )}
				/>

                <Redirect to="/" />
            </Switch>
        );
    }

    authRoutes = () => {
        return(
			<Switch>

                <Route 
					path={["/"]} 
					exact
                    render={() => ( < LandingPage /> )}
				/>

				<Route 
					path={["/logout"]} 
					exact
                    render={() => ( < LogOut /> )}
				/>

                <Route 
					path={["/gamelobby"]} 
					exact
                    render={() => ( < GameLobby /> )}
				/>


                <Route 
					path={["/game"]} 
					exact
                    render={() => ( <GamePage /> )}
				/>
                
                <Redirect to="/" />
            </Switch>
        );
    }


    render() {
        return (
            <Container fluid className="App">
                <Layout>
                    {
                        this.props.isAuthed ? 
                            this.authRoutes()
                            : 
                            this.unAuthRoutes()
                    }
                </Layout>
            </Container>
        );
    }
    
}

const mapStateToProps = state => {
    return {
        isAuthed : state.auth.token ? true : false,
    }
}

const mapDispatchToProps = dispatch => {
    return {        
        resetBoardGameState: () => dispatch(actions.resetBoardGameState()),
    }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(App));

