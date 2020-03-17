import React from 'react';
import classes from './BoardSpot.module.css';


class BoardSpot extends React.PureComponent {

    render() {

        let radius = this.props.r ;
        if (this.props.selectedSpotFlag)
        {
            // scaleAtrr = "scale(1.1 1.1)" ;
            radius = ( Number(radius) * 1.2 ).toString() ;
        }

        const selectedClasses = [] ; 
     
        let shadowColor = "#009900" ; 
        let dropShadowAtrr = "" ; 
        
        if (this.props.spotType === 0) 
        { 
            selectedClasses.push(classes.spot_not_allowed) ; 
        } 
        else if (this.props.spotType === 1) 
        { 
            selectedClasses.push(classes.spot_allowed) ; 
        } 
        else 
        { 
            selectedClasses.push(classes.spot_allowed) ; 
        } 
    
        if (this.props.playerMarker === 'X') 
        { 
            selectedClasses.push(classes.player_X_marker) ; 
        } 
        else if (this.props.playerMarker === 'O') 
        { 
            selectedClasses.push(classes.player_O_marker) ; 
        } 
    
        return ( 
            <> 
                <defs> 
                    <filter id="ds1" x="-100%" y="-100%" width="300%" height="300%"> 
                        <feComponentTransfer in="SourceAlpha"> 
                            <feFuncA type="table" tableValues="1 0" /> 
                        </feComponentTransfer> 
                        <feGaussianBlur stdDeviation="75"/> 
                        <feOffset    result="offsetblur"/> 
                        <feFlood floodColor={shadowColor} result="color"/> 
                        <feComposite in2="offsetblur" operator="in"/> 
                        <feComposite in2="SourceAlpha" operator="in" /> 
                        <feMerge> 
                            <feMergeNode in="SourceGraphic" /> 
                            <feMergeNode /> 
                        </feMerge> 
                    </filter> 
                </defs> 
    
                <circle filter={dropShadowAtrr} className={selectedClasses.join(' ')} cx={this.props.boardSpotInfo.x} cy={this.props.boardSpotInfo.y} r={radius} onClick={this.props.spotSelectedHandler} /> 
            </> 
        );
    }
}

export default BoardSpot ;
