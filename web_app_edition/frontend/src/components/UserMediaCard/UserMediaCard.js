import React from 'react';
import { connect } from 'react-redux';
import classes from '../UserCard/UserCard.module.scss';
import user_icon_path from '../../assets/images/user_icon.png';
import AI_icon_path from '../../assets/images/ai_icon.png';


const userMediaCard = (props) => {

    let img_path = user_icon_path;
    if (props.name === "AI bot")
    {
        img_path = AI_icon_path;
    }

    const boxShadowClass = props.playerTurn === props.playerMarker ? classes["playerBoxShadow" + props.playerMarker] : ""; 

    return (
        <div className={classes["playerCard" + props.playerMarker] + " " + boxShadowClass + " text-center pr-1 pl-2 pt-2 pb-2 w-100"} id={classes.user_card}>
            <div className="d-flex flex-row align-items-center justify-content-start" >
                <div id={classes.img_wrapper2}>
                    <img src={img_path} alt="User img" className={classes["imgBorder" + props.playerMarker] + " img-fluid rounded-circle mx-auto"}/>
                </div>

                <div>
                    <div className="pl-1" id={classes.username}>
                        <div className="d-inline"> {props.name} </div>
                        <div className="d-inline"> {props.surname} </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

const mapStateToProps = state => {
    return {
        playerTurn: state.board.playerTurn,
    }
}

export default connect( mapStateToProps )( userMediaCard ) ;