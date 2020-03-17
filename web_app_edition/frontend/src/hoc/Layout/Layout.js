import React from 'react';
import NavBar from '../../containers/Navigation/NavBar/NavBar';


const layout = (props) => (
    <>
        <NavBar/>
        {props.children}
    </>
);

export default layout;