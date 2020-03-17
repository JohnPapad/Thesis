import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
// import * as serviceWorker from './serviceWorker';
import { BrowserRouter } from 'react-router-dom';


import 'bootstrap/dist/css/bootstrap.min.css';

import { Provider } from 'react-redux';
import { createStore, applyMiddleware, compose, combineReducers } from 'redux';
import thunk from 'redux-thunk';

import gamePageReducer from './store/reducers/gamePage';
import boardReducer from './store/reducers/board';
import authReducer from './store/reducers/auth';
import * as actions from './store/actions/actionTypes';

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const appReducer = combineReducers({
    auth: authReducer,
    gamePage: gamePageReducer,
    board: boardReducer
});


const rootReducer = (state, action) => {
    if (action.type === actions.RESET_BOARD_GAME_STATE) 
    {
        // state = undefined;
        const { auth } = state;
        state = { auth };
    }
  
    return appReducer(state, action)
};


const store = createStore(rootReducer, composeEnhancers(
    applyMiddleware(thunk)
));

const app = (
    <Provider store={store}>
        <BrowserRouter>
            <App />
        </BrowserRouter>
    </Provider>
);

ReactDOM.render(app, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
// serviceWorker.unregister();
