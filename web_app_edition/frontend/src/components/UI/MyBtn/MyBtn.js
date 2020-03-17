import React from 'react';
import classes from './MyBtn.module.scss';
import { Button } from 'reactstrap';

const submitBtn = ( props ) => {

    const size = !props.size ? "sizeLG" : "size" + props.size;

    return (
        <Button style={{"borderWidth": props.borderWidth }} className={classes[size] + " font-weight-bold " + props.classes} id={classes.submit_btn}
            onClick={props.clickedHandler ? props.clickedHandler : () => { return }}
        >
            {props.children}
        </Button> 
    );

}


export default submitBtn;