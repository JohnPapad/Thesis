
import React from 'react';
import { NavLink as RouterNavLink, withRouter }  from 'react-router-dom';
import { NavItem, Button } from 'reactstrap';
import classes from './NavigationItem.module.scss'

const navigationItem = ( props ) => {

    const isActive = props.location.pathname === props.link;
    
    return (
        <NavItem className="d-flex align-content-center p-1 mr-2">
            <RouterNavLink
                style={{textDecoration: "none"}}
                className="container fluid align-self-center p-0" 
                exact
                to={props.link}
            >
                <Button id={classes.nav_item} className={isActive ? classes.nav_item_active : ""} size="sm" block>
                    <span className={classes.text}>
                        {props.children}
                    </span>
                </Button>
            </RouterNavLink>  
        </NavItem>
    );
}

export default withRouter(navigationItem);