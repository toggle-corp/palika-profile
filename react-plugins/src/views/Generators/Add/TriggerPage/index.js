import React from 'react';
import PropTypes from 'prop-types';

import Faram, {
    requiredCondition,
} from '@togglecorp/faram';
import FileInput from '#rsci/RawFileInput';
import PrimaryButton from '#rsca/Button/PrimaryButton';
import Sortable from '#rscv/Taebul/Sortable';
import ColumnWidth from '#rscv/Taebul/ColumnWidth';
import NormalTaebul from '#rscv/Taebul';
import update from '#rsu/immutable-update';

import FileLink from '#components/FileLink';

import {
    RequestCoordinator,
    RequestClient,
} from '#request';


import columns from './columns';
import requests from './requests';
import styles from './styles.scss';

const Taebul = Sortable(ColumnWidth(NormalTaebul));

const propTypes = {
    // eslint-disable-next-line react/forbid-prop-types
    requests: PropTypes.object.isRequired,
    setDefaultRequestParams: PropTypes.func.isRequired,
};

const defaultProps = {};
const keySelector = datum => `${datum.index}-${datum.column}`;
const emptyObject = {};
const emptyList = [];

@RequestCoordinator
@RequestClient(requests)
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

            generator: undefined,

            exportState: undefined,
            exportStatus: undefined,

            validationState: undefined,
            validationStatus: undefined,

            taebulOptions: {
                defaultColumnWidth: 250,
                minColumnWidth: 250,
            },
        };

        props.setDefaultRequestParams({
            setState: newState => this.setState(newState),
            getGeneratorId: this.getGeneratorId,
            updateGenerator: this.updateGenerator,
        });
    }

    getGeneratorId = () => {
        const {
            generator: {
                id,
            } = {},
        } = this.state;
        return id || 8;
    }

    updateGenerator = (settings) => {
        const { generator } = this.state;
        this.setState({
            generator: update(generator, settings),
        });
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
        generatorAdd.do({ data: formData });
    };

    handleSettingsChange = (options) => {
        this.setState({ taebulOptions: options });
    }

    renderForm = ({
        faramValues,
        faramErrors,
        pending,
        pristine,
    }) => (
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
    )

    renderExportStatus = ({
        state: { progress: { items, itemList } },
    }) => (
        itemList.map(
            item => (
                <div key={item}>
                    <span>{`${item}:  `}</span>
                    <span>
                        {
                            typeof (items[item]) === 'object'
                                ? `${items[item].complete}/${items[item].total}`
                                : items[item]
                        }
                    </span>
                </div>
            ),
        )
    )

    renderValidationStatus = ({
        state: { progress: { items, itemList } },
    }) => (
        itemList.map(
            item => (
                <div key={item}>
                    <span>{`${item}:  `}</span>
                    <span>
                        {
                            typeof (items[item]) === 'object'
                                ? `${items[item].complete}/${items[item].total}`
                                : items[item]
                        }
                    </span>
                </div>
            ),
        )
    )

    triggerExport = () => {
        const {
            requests: {
                generatorTriggerExport,
            },
        } = this.props;
        generatorTriggerExport.do({
            generatorId: this.getGeneratorId(),
        });
    }

    triggerValidator = () => {
        const {
            requests: {
                generatorTriggerValidator,
            },
        } = this.props;
        generatorTriggerValidator.do({
            generatorId: this.getGeneratorId(),
        });
    }

    render() {
        const {
            requests: {
                generatorAdd,
                generatorTriggerExport,
                generatorTriggerExportPoll,
                generatorTriggerValidator,
                generatorTriggerValidatorPoll,
            },
        } = this.props;

        const {
            faramValues,
            faramErrors,
            pristine,

            generator: {
                exports = emptyList,
                errors = emptyList,
            } = emptyObject,
            exportState,
            exportStatus,

            validationState,
            validationStatus,

            taebulOptions,
        } = this.state;

        const pending = (
            generatorAdd.pending
            || generatorTriggerExport.pending || generatorTriggerExportPoll.pending
            || generatorTriggerValidator.pending || generatorTriggerValidatorPoll.pending
        );

        const Form = this.renderForm;
        const ExportStatus = this.renderExportStatus;
        const ValidationStatus = this.renderValidationStatus;

        console.warn('validationState: ', validationState);
        console.warn('validationStatus: ', validationStatus);

        if (exportStatus) {
            if (exportStatus === 'success') {
                return exports.map(
                    exp => (
                        <div key={exp.id}>
                            <FileLink
                                url={exp.file}
                            />
                        </div>
                    ),
                );
            }
            return exportStatus;
        }

        if (validationStatus) {
            if (validationStatus === 'success') {
                return (
                    <Taebul
                        className={styles.table}
                        data={errors}
                        settings={taebulOptions}
                        keySelector={keySelector}
                        columns={columns}
                        onChange={this.handleSettingsChange}
                    />
                );
            }
            return exportStatus;
        }

        if (exportState) {
            return (
                <ExportStatus
                    state={exportState}
                />
            );
        }

        if (validationState) {
            return (
                <ValidationStatus
                    state={validationState}
                />
            );
        }

        if (this.getGeneratorId()) {
            return (
                <div>
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
            );
        }

        return (
            <Form
                faramValues={faramValues}
                faramErrors={faramErrors}
                pending={pending}
                pristine={pristine}
            />
        );
    }
}

export default FormPage;
