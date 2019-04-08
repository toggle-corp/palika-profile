import React from 'react';
import PropTypes from 'prop-types';
import { compose } from 'redux';
import { connect } from 'react-redux';

import Spinner from '#rscz/Spinner';
import Message from '#rscv/Message';
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
import styles from './styles.scss';

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
        return (
            <div className={styles.container}>
                <Spinner className={styles.spinner} />
                <div className={styles.messageContainer}>
                    <Message>
                        Validating Document
                    </Message>
                </div>
            </div>
        );
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
