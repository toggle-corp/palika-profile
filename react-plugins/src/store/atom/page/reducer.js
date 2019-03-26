import produce from 'immer';

import createReducerWithMap from '#utils/createReducerWithMap';

import initialState from './initialState';

// TYPE

const PREFIX = 'PAGE/GENERATOR_PAGE';

const SET_GENERATOR = `${PREFIX}/SET_GENERATOR`;
const SET_GENERATOR_STATE = `${PREFIX}/SET_GENERATOR_STATE`;
const SET_GENERATOR_STATUS = `${PREFIX}/SET_GENERATOR_STATUS`;
const SET_GENERATOR_SELECTED_PALIKACODES = `${PREFIX}/SET_GENERATOR_SELECTED_PALIKACODES`;
const SET_EXPORT_FARAM = `${PREFIX}/SET_EXPORT_FARAM`;

// ACTION CREATORS
export const setGeneratorActionGP = ({ generator }) => ({
    type: SET_GENERATOR,
    generator,
});

export const setGeneratorStateActionGP = ({ validationState, exportState }) => ({
    type: SET_GENERATOR_STATE,
    validationState,
    exportState,
});

export const setGeneratorStatusActionGP = ({ validationStatus, exportStatus }) => ({
    type: SET_GENERATOR_STATUS,
    validationStatus,
    exportStatus,
});

export const setGeneratorSelectedPalikaCodesActionGP = ({ selectedPalikaCodes }) => ({
    type: SET_GENERATOR_SELECTED_PALIKACODES,
    selectedPalikaCodes,
});

export const setExportFaramActionGP = ({ faramValues, faramErrors }) => ({
    type: SET_EXPORT_FARAM,
    faramValues,
    faramErrors,
});


// dashboard action creator

const setGenerator = (state, action) => {
    const { generator } = action;
    const newState = produce(state, (deferedState) => {
        // eslint-disable-next-line no-param-reassign
        deferedState.generatorAdd.generator = {
            ...state.generatorAdd.generator,
            ...generator,
        };
    });
    return newState;
};

const setGeneratorState = (state, action) => {
    const {
        exportState,
        validationState,
    } = action;
    const newState = produce(state, (deferedState) => {
        if (exportState) {
            // eslint-disable-next-line no-param-reassign
            deferedState.generatorAdd.exportState = exportState;
        }
        if (validationState) {
            // eslint-disable-next-line no-param-reassign
            deferedState.generatorAdd.validationState = validationState;
        }
    });
    return newState;
};

const setGeneratorStatus = (state, action) => {
    const {
        exportStatus,
        validationStatus,
    } = action;
    const newState = produce(state, (deferedState) => {
        if (exportStatus) {
            // eslint-disable-next-line no-param-reassign
            deferedState.generatorAdd.exportStatus = exportStatus;
        }
        if (validationStatus) {
            // eslint-disable-next-line no-param-reassign
            deferedState.generatorAdd.validationStatus = validationStatus;
        }
    });
    return newState;
};

const setGeneratorSelectedPalikaCodes = (state, action) => {
    const { selectedPalikaCodes } = action;
    const newState = produce(state, (deferedState) => {
        // eslint-disable-next-line no-param-reassign
        deferedState.generatorAdd.selectedPalikaCodes = selectedPalikaCodes;
    });
    return newState;
};

const setExportFaram = (state, action) => {
    const {
        faramValues,
        faramErrors,
    } = action;
    const newState = produce(state, (deferedState) => {
        const {
            recentFaramValues,
            recentFaramErrors,
        } = deferedState.generatorAdd.generatorExport || {};
        // eslint-disable-next-line no-param-reassign
        deferedState.generatorAdd.generatorExport = {
            faramValues: faramValues || recentFaramValues,
            faramErrors: faramErrors || recentFaramErrors,
        };
    });
    return newState;
};

const reducers = {
    [SET_GENERATOR]: setGenerator,
    [SET_GENERATOR_STATE]: setGeneratorState,
    [SET_GENERATOR_STATUS]: setGeneratorStatus,
    [SET_GENERATOR_SELECTED_PALIKACODES]: setGeneratorSelectedPalikaCodes,
    [SET_EXPORT_FARAM]: setExportFaram,
};

const reducer = createReducerWithMap(reducers, initialState);
export default reducer;
