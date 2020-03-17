import React from 'react';
import BoardSpots from '../../../components/BoardSpots/BoardSpots';
import WoodenImgPath from '../../../assets/images/wooden_background.jpg';
import classes from './Board.module.scss';

class Board extends React.Component {

    render() {
        return (
            <svg
                version="1.1"
                width="100%"
                height="100%" 
                viewBox="-410 -410 820 820"
            >
                <defs>
                    <pattern id="board_bg_img" patternUnits="userSpaceOnUse" x="-410" y="-410" width="100%" height="100%">
                        <image width="100%" height="100%" href={WoodenImgPath} />             
                    </pattern>
                </defs>

                <rect id={classes.board} x="-410" y="-410" width="820" height="820" fill="url(#board_bg_img)"/>
                <rect x="-350" y="-350" width="700" height="700" fill="none" stroke="#361c0a" strokeWidth="5"/>

                <text className={classes.board_coords}>
                    <tspan x="-390" y="-290">7</tspan>
                    <tspan x="-390" y="-190">6</tspan>
                    <tspan x="-390" y="-90">5</tspan>
                    <tspan x="-390" y="10">4</tspan>
                    <tspan x="-390" y="110">3</tspan>
                    <tspan x="-390" y="210">2</tspan>
                    <tspan x="-390" y="310">1</tspan>
                </text>

                <text className={classes.board_coords}>
                    <tspan x="-310" y="390">A</tspan>
                    <tspan x="-210" y="390">B</tspan>
                    <tspan x="-110" y="390">C</tspan>
                    <tspan x="-10" y="390">D</tspan>
                    <tspan x="100" y="390">E</tspan>
                    <tspan x="200" y="390">F</tspan>
                    <tspan x="300" y="390">G</tspan>
                </text>
                
                <g>
                    <rect x="-300" y="-300" width="600" height="600" />
                    <rect x="-200" y="-200" width="400" height="400" />
                    <rect x="-100" y="-100" width="200" height="200" />
                    <line x1="0" y1="-300" x2="0" y2="-100" />
                    <line x1="0" y1="300" x2="0" y2="100" />
                    <line x1="-300" y1="0" x2="-100" y2="0" />
                    <line x1="300" y1="0" x2="100" y2="0" />
                </g>

                <BoardSpots r="20"
                    WSsendData={this.props.WSsendData} 
                    AImode={this.props.AImode}
                    gameOver={this.props.gameOver}
                />
        </svg>
        );
    }
}

export default Board;
