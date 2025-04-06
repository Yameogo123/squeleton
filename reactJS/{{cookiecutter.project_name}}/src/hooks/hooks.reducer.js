//import moment from "moment";

import moment from "moment";

const userState={
    user: {},
    token: "",
    loading: "",
    limit: ""
}



export function userReducer(state= userState, action) {
    let newState;

    switch (action.type) { 
        case "login":
            newState={...state, user: action.value.user, token: action.value.token, limit: moment().toISOString()}
            return newState || state;
        case "logout":
            newState= {...state, user:{}, token:"", limit: ""}
            return newState || state;
        case "loading":
            newState= {...state, loading: action.value}
            return newState || state;
        case "user-update":
            newState= {...state, user: action.value}
            return newState || state;
        default:
            return state;
    }
}

