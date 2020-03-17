import React from 'react';
import { connect } from 'react-redux';
import classes from './NavBar.module.scss';
import { NavLink as RouterNavLink, withRouter }  from 'react-router-dom';
import logo_path from '../../../assets/images/nmm_board.png';
import NavigationItem from '../../../components/Navigation/NavigationItem';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSignInAlt, faSignOutAlt, faUserEdit } from '@fortawesome/free-solid-svg-icons';

import {
    Collapse,
    Navbar,
    NavbarToggler,
    NavbarBrand,
    Nav } from 'reactstrap';

const hardRedirectPaths = ["/gamelobby", "/game"];

class NavBar extends React.Component {

    constructor(props) {
        super(props);

        this.toggle = this.toggle.bind(this);
        this.state = {
            isOpen: false
        };
    }

    toggle() {
        this.setState({
            isOpen: !this.state.isOpen
        });
    }

    unAuthNavItems = () => {
		return(
			<>
				<NavigationItem link="/signin">
                    Sign In
                    <FontAwesomeIcon icon={faSignInAlt} className="ml-2"/>
                </NavigationItem>

                <NavigationItem link="/signup">
                    Sign Up
                    <FontAwesomeIcon icon={faUserEdit} className="ml-2"/>
                </NavigationItem>								
			</>
		);
    }

    authNavItems = () => {
		return(
			<>
                <NavigationItem link="/logout">
                    Log Out
                    <FontAwesomeIcon icon={faSignOutAlt} className="ml-2"/>
                </NavigationItem>								
			</>
		);
	}

    render() {
        return (
            <Navbar light expand="sm" id={classes.navbar} className="fixed-top pl-4 pb-2 pt-2" >
                {
                    hardRedirectPaths.includes(this.props.location.pathname) ?
                        <NavbarBrand href="/">
                            <img src={logo_path} id={classes.img} alt="Logo" className="img-fluid"/>
                        </NavbarBrand>
                    :
                        <RouterNavLink to="/" exact>
                            <img src={logo_path} id={classes.img} alt="Logo" className="img-fluid"/>
                        </RouterNavLink> 
                }
                <NavbarToggler onClick={this.toggle} />
                <Collapse isOpen={this.state.isOpen} navbar>
                    <Nav className="ml-auto" navbar>
                        {
                            ! this.props.isAuthed ?
                                this.unAuthNavItems()
                            :
                                this.authNavItems()                        
                        }
                    </Nav>
                </Collapse>
            </Navbar>
        );
    }
}

const mapStateToProps = state => {
    return {
        isAuthed : state.auth.token ? true : false,
    }
}

export default withRouter(connect(mapStateToProps)(NavBar));
