import React from 'react';
import ReactDOM from 'react-dom';

import components from './registry';
import * as storage from './storage';


export const render = (component, selector, props = {}) => {
    const Component = components[component];
    if (!Component) {
        console.error(`Invalid component: ${component}`);
        return;
    }

    let element = selector;
    if (typeof element === 'string') {
        element = document.querySelector(selector);

        if (!element) {
            console.error(`Invalid element selector: ${selector}`);
            return;
        }
    }

    if (!(element instanceof HTMLElement)) {
        console.error(`Invalid element: ${element}`);
        return;
    }

    ReactDOM.render(<Component {...props} />, element);
};

export const state = {
    set: storage.setGlobalState,
    get: storage.getGlobalState,
    addListener: storage.addListener,
    removeListener: storage.removeListener,
};
