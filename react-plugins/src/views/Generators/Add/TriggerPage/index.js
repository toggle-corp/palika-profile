import React from 'react';
import PropTypes from 'prop-types';

import PrimaryButton from '#rsca/Button/PrimaryButton';

import TaskStatus from '#components/TaskStatus';

import {
    RequestCoordinator,
    RequestClient,
} from '#request';


import ValidatorPreview from '../ValidatorPreview';

import requests from './requests';
import styles from './styles.scss';

const propTypes = {
    /* eslint-disable react/forbid-prop-types */
    requests: PropTypes.object.isRequired,
    generator: PropTypes.object.isRequired,
    validationState: PropTypes.object,
    validationStatus: PropTypes.string,
    /* eslint-enable react/forbid-prop-types */
    // updateGenerator: PropTypes.func.isRequired,
    // setState: PropTypes.func.isRequired,
    // setStatus: PropTypes.func.isRequired,
    onNext: PropTypes.func.isRequired,
};

const defaultProps = {
    validationState: undefined,
    validationStatus: undefined,
};
const emptyObject = {};

@RequestCoordinator
@RequestClient(requests)
class TriggerPage extends React.PureComponent {
    static propTypes = propTypes;
    static defaultProps = defaultProps;

    triggerExport = () => {
        const { onNext } = this.props;
        onNext();
    }

    triggerValidator = () => {
        const {
            requests: {
                generatorTriggerValidator,
            },
        } = this.props;
        generatorTriggerValidator.do();
    }

    render() {
        const {
            requests: {
                generatorTriggerValidator,
                generatorTriggerValidatorPoll,
            },
        } = this.props;

        const {
            generator: { errors } = emptyObject,
            validationState,
            validationStatus,
        } = this.props;

        const pending = (
            generatorTriggerValidator.pending || generatorTriggerValidatorPoll.pending
        );

        if (validationState) {
            return (
                <TaskStatus
                    progress={validationState}
                />
            );
        }

        return (
            <div>
                <div className={styles.bottomContainer}>
                    <PrimaryButton
                        className={styles.button}
                        pending={pending}
                        onClick={this.triggerExport}
                    >
                        Trigger Export
                    </PrimaryButton>
                    <PrimaryButton
                        className={styles.button}
                        pending={pending}
                        onClick={this.triggerValidator}
                    >
                        Trigger Validator
                    </PrimaryButton>
                </div>
                <ValidatorPreview
                    progress={validationStatus}
                    errors={errors}
                />
            </div>
        );
    }
}

export default TriggerPage;
