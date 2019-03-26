// Simple key-value storage to share data globally
import React from 'react';
import hoistNonReactStatics from 'hoist-non-react-statics';

const storage = {
    generatorAddPage: {
        generator: {
            id: 3,
        },
    },
};
const listeners = {};

export const addListener = (listenerKey, listener) => {
    listeners[listenerKey] = listener;
};

export const removeListener = (listenerKey) => {
    delete listeners[listenerKey];
};

export const setGlobalState = (key, value) => {
    storage[key] = value;

    Object.keys(listeners).forEach((lkey) => {
        listeners[lkey]();
    });
};

export const getGlobalState = key => storage[key];


const connectedId = 1;
export const connect = mapping => (WrappedComponent) => {
    class View extends React.PureComponent {
        constructor(props) {
            super(props);
            this.uniqueId = `connectedComponent${connectedId}`;
            this.state = {
                injectedProps: mapping(storage),
            };
            addListener(this.uniqueId, this.handleStateChange);
        }

        componentWillUnmount() {
            removeListener(this.uniqueId);
        }

        handleStateChange = () => {
            this.setState({
                injectedProps: mapping(storage),
            });
        }

        render() {
            const { injectedProps } = this.state;

            return (
                <WrappedComponent
                    {...this.props}
                    {...injectedProps}
                />
            );
        }
    }

    return hoistNonReactStatics(
        View,
        WrappedComponent,
    );
};
