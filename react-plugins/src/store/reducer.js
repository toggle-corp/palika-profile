import { combineReducers } from 'redux';

import pageReducer from './atom/page/reducer';

const rootReducer = combineReducers(
    {
        page: pageReducer,
    },
);

export default rootReducer;
