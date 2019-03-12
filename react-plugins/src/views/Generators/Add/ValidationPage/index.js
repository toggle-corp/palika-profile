import React from 'react';
import PropTypes from 'prop-types';
import { compose } from 'redux';
import { connect } from 'react-redux';

import {
    generatorSelectorGP,
} from '#selectors';
import {
    setGeneratorActionGP,
    setGeneratorStateActionGP,
    setGeneratorStatusActionGP,
} from '#actionCreators';

import {
    RequestCoordinator,
    RequestClient,
} from '#request';


import requests from './requests';

const propTypes = {
    /* eslint-disable react/forbid-prop-types */
    requests: PropTypes.object.isRequired,
    generator: PropTypes.object.isRequired,
    /* eslint-enable react/forbid-prop-types */
    // onNext: PropTypes.func.isRequired,
};

const defaultProps = {};

class ValidationPage extends React.PureComponent {
    static propTypes = propTypes;
    static defaultProps = defaultProps;

    componentDidMount() {
        const {
            generator: { id },
            requests: {
                generatorTriggerValidator,
            },
        } = this.props;
        if (id) {
            generatorTriggerValidator.do({ id });
        }
    }

    render() {
        return 'Validating Document.....';
    }
}

const mapStateToProps = state => ({
    generator: generatorSelectorGP(state),
});

const mapDispatchToProps = dispatch => ({
    setGenerator: params => dispatch(setGeneratorActionGP(params)),
    setGeneratorState: params => dispatch(setGeneratorStateActionGP(params)),
    setGeneratorStatus: params => dispatch(setGeneratorStatusActionGP(params)),
});

export default compose(
    connect(mapStateToProps, mapDispatchToProps),
    RequestCoordinator,
    RequestClient(requests),
)(ValidationPage);
