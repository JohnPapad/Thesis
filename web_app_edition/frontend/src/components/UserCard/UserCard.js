import React from 'react';
import classes from './UserCard.module.scss';
import user_icon_path from '../../assets/images/user_icon.png';
import AI_icon_path from '../../assets/images/ai_icon.png';
import { connect } from 'react-redux';


const userCard = (props) => {
    let img_path = user_icon_path;
    if (props.name === "AI bot")
    {
        img_path = AI_icon_path;
    }

    const boxShadowClass = props.playerTurn === props.playerMarker ? classes["playerBoxShadow" + props.playerMarker] : ""; 

    return (
        <div className={classes["playerCard" + props.playerMarker] + " " + boxShadowClass + " text-center pb-2 pt-3"} id={classes.user_card} >
            <div className="mx-auto mb-3" id={classes.img_wrapper}>
                <img src={img_path} alt="User img" className={classes["imgBorder" + props.playerMarker] + " img-fluid rounded-circle mx-auto"}/>
            </div>

            <div className="pb-2 mb-2" id={classes.username}>
                <div className="d-inline"> {props.name} </div>
                <div className="d-inline"> {props.surname} </div>
            </div>
        </div>
    );
}


const mapStateToProps = state => {
    return {
        playerTurn: state.board.playerTurn,
    }
}


// export default userCard;
export default connect( mapStateToProps )( userCard ) ;