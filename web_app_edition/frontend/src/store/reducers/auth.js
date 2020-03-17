import * as actionTypes from '../actions/actionTypes';
import produce from 'immer';

const initialState = {
    token: localStorage.getItem('token'),
    userId: localStorage.getItem('userId'),
    username: localStorage.getItem('username'),
    error: null,
    loading: false,
    authRedirectPath: '/'
};

const authStart = (draft, action) => {
    draft.error = null;
    draft.loading = true;
};

const authSuccess = (draft, action) => {
    draft.token = action.idToken;
    draft.userId = action.userId;
    draft.username = action.username;
};

const authFail = (draft, action) => {
    draft.error = action.error;
    draft.loading = false;
};

const authLogout = (draft, action) => {
    draft.token = null;
    draft.userId = null;
};

const setAuthRedirectPath = (draft, action) => {
    draft.authRedirectPath = action.path;
}

    
const reducer = ( state = initialState, action ) => 
    produce(state, draft => {
        switch ( action.type ) {
            case actionTypes.AUTH_START: 
                authStart(draft, action);
                return;
            case actionTypes.AUTH_SUCCESS: 
                authSuccess(draft, action);
                return;
            case actionTypes.AUTH_FAIL: 
                authFail(draft, action);
                return;
            case actionTypes.AUTH_LOGOUT: 
                authLogout(draft, action);
                return;
            case actionTypes.SET_AUTH_REDIRECT_PATH: 
                setAuthRedirectPath(draft, action);
                return;
            default:
                return state;
        }
    });

export default reducer;