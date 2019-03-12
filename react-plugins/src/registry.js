import React from 'react';
import { Provider } from 'react-redux';

import store from './store';

import Generators from './views/Generators';
import GeneratorAdd from './views/Generators/Add';

// HOC to attach attach store for every App
const attachStore = App => ({ ...props }) => (
    <Provider store={store}>
        <App {...props} />
    </Provider>
);

export default {
    Generators: attachStore(Generators),
    GeneratorAdd: attachStore(GeneratorAdd),
};
