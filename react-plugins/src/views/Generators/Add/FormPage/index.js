import React from 'react';
import PropTypes from 'prop-types';
import { compose } from 'redux';
import { connect } from 'react-redux';

import Faram, {
    requiredCondition,
} from '@togglecorp/faram';
import FileInput from '#rsci/RawFileInput';
import PrimaryButton from '#rsca/Button/PrimaryButton';

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
    onNext: PropTypes.func.isRequired,
};

const defaultProps = {};

class FormPage extends React.PureComponent {
    static propTypes = propTypes;
    static defaultProps = defaultProps;
    static schema = {
        fields: {
            file: [requiredCondition],
        },
    }

    constructor(props) {
        super(props);

        this.state = {
            faramValues: {},
            faramErrors: {},
            pristine: true,
        };
    }

    componentDidMount() {
        // NOTE: This is for debugging only
        const {
            generator: { id },
            onNext,
        } = this.props;
        if (id) {
            onNext();
        }
    }

    handleFaramChange = (faramValues, faramErrors) => {
        this.setState({
            faramValues,
            faramErrors,
            pristine: false,
        });
    };

    handleFaramFailure = (faramErrors) => {
        this.setState({ faramErrors });
    };

    handleFaramSuccess = (_, values) => {
        const {
            requests: {
                generatorAdd,
            },
        } = this.props;
        const formData = new FormData();

        formData.append('file', values.file);
        generatorAdd.do({
            data: formData,
            setState: params => this.setState(params),
        });
    };

    render() {
        const {
            requests: {
                generatorAdd: { pending },
                generatorTriggerValidatorPoll,
                generatorTriggerValidator,
                generatorGet,
            },
        } = this.props;

        const {
            faramValues,
            faramErrors,
            pristine,
        } = this.state;

        const metaExtractionPending = (
            generatorTriggerValidatorPoll.pending || generatorTriggerValidator.pending
            || generatorGet.pending
        );

        if (metaExtractionPending) {
            return 'Validating Document';
        }

        return (
            <Faram
                className={styles.form}
                onValidationSuccess={this.handleFaramSuccess}
                onValidationFailure={this.handleFaramFailure}
                onChange={this.handleFaramChange}
                schema={FormPage.schema}
                value={faramValues}
                error={faramErrors}
            >
                <FileInput
                    disabled={pending}
                    faramElementName="file"
                    error={faramErrors.file}
                    accept=".xlsx"
                >
                    {'Click to Select File'}
                </FileInput>
                <div className={styles.bottomContainer}>
                    <PrimaryButton
                        className={styles.button}
                        type="submit"
                        pending={pending}
                        disabled={pristine}
                    >
                            Submit
                    </PrimaryButton>
                </div>
            </Faram>
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
)(FormPage);
