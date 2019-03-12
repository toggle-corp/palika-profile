import React from 'react';
import PropTypes from 'prop-types';
import memoize from 'memoize-one';
import { compose } from 'redux';
import { connect } from 'react-redux';

import Faram, {
    requiredCondition,
} from '@togglecorp/faram';
import PrimaryButton from '#rsca/Button/PrimaryButton';
import MultiSelectInput from '#rsci/MultiSelectInput';

import {
    generatorSelectorGP,
    generatorErrorListSelectorGP,
    generatorProvinceListSelectorGP,

    exportDistrictListSelectorGP,
    exportPalikaListSelectorGP,
    exportFaramSelectorGP,
    exportStateSelectorGP,
} from '#selectors';
import {
    setGeneratorActionGP,
    setExportFaramActionGP,
    setGeneratorStatusActionGP,
    setGeneratorStateActionGP,
} from '#actionCreators';

import {
    RequestCoordinator,
    RequestClient,
} from '#request';


import TaskStatus from '#components/TaskStatus';
import ValidatorPreview from '../ValidatorPreview';

import requests from './requests';
import styles from './styles.scss';

const propTypes = {
    /* eslint-disable react/forbid-prop-types */
    requests: PropTypes.object.isRequired,
    generator: PropTypes.object.isRequired,
    errors: PropTypes.array.isRequired,
    provinces: PropTypes.array.isRequired,
    districts: PropTypes.array.isRequired,
    palikaCodes: PropTypes.array.isRequired,
    exportFaram: PropTypes.object.isRequired,
    exportState: PropTypes.object.isRequired,
    /* eslint-enable react/forbid-prop-types */
    setExportFaram: PropTypes.func.isRequired,
    setGeneratorStatus: PropTypes.func.isRequired,
    setGeneratorState: PropTypes.func.isRequired,
    onNext: PropTypes.func.isRequired,
};

const defaultProps = {};

const emptyObject = {};

const KeySelector = ele => ele.id;
const labelSelector = (ele = emptyObject) => ele.title;
const palikaKeySelector = palika => palika.code;
const palikaLabelSelector = labelSelector;

@RequestCoordinator
@RequestClient(requests)
class TriggerPage extends React.PureComponent {
    static propTypes = propTypes;
    static defaultProps = defaultProps;
    static schema = {
        fields: {
            selectedProvince: [],
            selectedDistrict: [],
            selectedPalikaCodes: [requiredCondition],
        },
    }

    componentDidMount() {
        // NOTE: This is for debugging only
        const {
            generator: {
                id,
                skipTriggerPage,
            } = emptyObject,
            requests: { generatorGet },
            onNext,
        } = this.props;
        if (skipTriggerPage) {
            onNext();
        } else if (id) {
            generatorGet.do({ pullMeta: true });
        }
    }

    getValidatedDistrictId = memoize(
        (selectedDistricts, districts) => {
            if (selectedDistricts && selectedDistricts.length) {
                return selectedDistricts.filter(
                    districtId => districts.findIndex(
                        district => district.id === districtId,
                    ) !== -1,
                );
            }
            return [];
        },
    )

    getValidatedPalikaCodes = memoize(
        (selectedPalikaCodes, palikaCodes) => {
            if (selectedPalikaCodes && selectedPalikaCodes.length) {
                return selectedPalikaCodes.filter(
                    palikaCode => palikaCodes.findIndex(
                        pc => pc.code === palikaCode,
                    ) !== -1,
                );
            }
            return [];
        },
    )

    handleFaramChange = (faramValues, faramErrors) => {
        const {
            setExportFaram,
        } = this.props;
        setExportFaram({
            faramValues,
            faramErrors,
            // pristine: false,
        });
    };

    handleFaramFailure = (faramErrors) => {
        const { setExportFaram } = this.props;
        setExportFaram({ faramErrors });
    };

    handleFaramSuccess = (_, { selectedPalikaCodes }) => {
        const {
            requests: {
                generatorTriggerExport,
            },
        } = this.props;
        generatorTriggerExport.do({ selectedPalikaCodes });
    };

    render() {
        const {
            requests: {
                generatorTriggerExport,
                generatorTriggerExportPoll,
            },
            errors,
            provinces,
            districts,
            palikaCodes,

            exportFaram,
            exportState,
        } = this.props;

        const {
            faramValues,
            faramErrors,
            // pristine,
        } = exportFaram;

        const {
            selectedDistrict,
            selectedPalikaCodes,
        } = faramValues;

        const validatedFaramValues = {
            ...faramValues,
            selectedDistrict: this.getValidatedDistrictId(selectedDistrict, districts),
            selectedPalikaCodes: this.getValidatedPalikaCodes(selectedPalikaCodes, palikaCodes),
        };
        const pending = false;
        const exportPending = (
            generatorTriggerExportPoll.pending || generatorTriggerExport.pending
        );

        return (
            <div>
                <div className={styles.bottomContainer}>
                    <Faram
                        className={styles.form}
                        onValidationSuccess={this.handleFaramSuccess}
                        onValidationFailure={this.handleFaramFailure}
                        onChange={this.handleFaramChange}
                        schema={TriggerPage.schema}
                        value={validatedFaramValues}
                        error={faramErrors}
                    >
                        <MultiSelectInput
                            faramElementName="selectedProvince"
                            keySelector={KeySelector}
                            labelSelector={labelSelector}
                            options={provinces}
                            showHintAndError={false}
                            placeholder="Select Province"
                        />
                        <MultiSelectInput
                            faramElementName="selectedDistrict"
                            keySelector={KeySelector}
                            labelSelector={labelSelector}
                            options={districts}
                            showHintAndError={false}
                            placeholder="Select District"
                        />
                        <MultiSelectInput
                            faramElementName="selectedPalikaCodes"
                            keySelector={palikaKeySelector}
                            labelSelector={palikaLabelSelector}
                            options={palikaCodes}
                            showHintAndError={false}
                            placeholder="Select Palikas"
                        />
                        <PrimaryButton
                            className={styles.button}
                            pending={pending}
                            type="submit"
                        >
                            Export
                        </PrimaryButton>
                    </Faram>
                </div>
                {
                    exportPending && (
                        <TaskStatus
                            {...exportState}
                        />
                    )
                }
                <ValidatorPreview
                    errors={errors}
                />
            </div>
        );
    }
}

const mapStateToProps = state => ({
    generator: generatorSelectorGP(state),
    errors: generatorErrorListSelectorGP(state),
    provinces: generatorProvinceListSelectorGP(state),

    districts: exportDistrictListSelectorGP(state),
    palikaCodes: exportPalikaListSelectorGP(state),
    exportFaram: exportFaramSelectorGP(state),
    exportState: exportStateSelectorGP(state),
});

const mapDispatchToProps = dispatch => ({
    setGenerator: params => dispatch(setGeneratorActionGP(params)),
    setExportFaram: params => dispatch(setExportFaramActionGP(params)),
    setGeneratorStatus: params => dispatch(setGeneratorStatusActionGP(params)),
    setGeneratorState: params => dispatch(setGeneratorStateActionGP(params)),
});

export default compose(
    connect(mapStateToProps, mapDispatchToProps),
    RequestCoordinator,
    RequestClient(requests),
)(TriggerPage);
