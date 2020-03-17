import React from 'react'; 
import classes from './BoardSpot.module.css'; 
 
 
class MovingBoardSpot extends React.PureComponent {
    
    constructor(props) {
        super(props);
        this.myRef = React.createRef();
    }

    render() {

        const selectedClasses = [] ; 
        let shadowColor = this.props.shadowColor ; 
        let dropShadowAtrr = "" ; 
        
        if (this.props.isHighlighted)
        { 
            selectedClasses.push(classes.spot_highlighted) ; 
            dropShadowAtrr = "url(#ds1)" ; 
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
    
                <circle filter={dropShadowAtrr} className={selectedClasses.join(' ')} cx={this.props.x} cy={this.props.y} r={this.props.r} > 
                    <animateTransform ref={this.myRef}
                        attributeName="transform"
                        type="translate"
                        from={this.props.transFrom}
                        to={this.props.transTo}
                        begin="indefinite"
                        dur={this.props.moveDuration.toString() + "s"}
                        fill="freeze"
                        repeatCount="1"
                    />
                </circle>
            </> 
        ); 
    }

    componentDidMount () {
        this.myRef.current.beginElement();
    }

} 
 
export default MovingBoardSpot;