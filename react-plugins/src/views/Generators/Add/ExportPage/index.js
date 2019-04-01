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
import SegmentInput from '#rsci/SegmentInput';
import ScrollTabs from '#rscv/ScrollTabs';
import MultiViewContainer from '#rscv/MultiViewContainer';
import Message from '#rscv/Message';
import iconNames from '#rsk/iconNames';

import {
    generatorSelectorGP,
    generatorErrorListSelectorGP,
    generatorProvinceListSelectorGP,

    generatorDistrictListSelectorGP,
    generatorPalikaCodeListSelectorGP,

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
    exportState: PropTypes.object.isRequired,
    /* eslint-enable react/forbid-prop-types */
    setExportFaram: PropTypes.func.isRequired,
    setGeneratorStatus: PropTypes.func.isRequired,
    setGeneratorState: PropTypes.func.isRequired,
    onNext: PropTypes.func.isRequired,
};

const defaultProps = {};

const emptyObject = {};

const tabs = {
    progress: 'Export Progress',
    validation: 'Validation',
};
const NEPALI = 'nep';
const ENGLISH = 'eng';

const languageOptions = [
    {
        title: 'Nepali',
        key: NEPALI,
    },
    {
        title: 'English',
        key: ENGLISH,
    },
];

const KeySelector = ele => ele.id;
const labelSelector = (ele = emptyObject) => ele.title;
const palikaKeySelector = palika => palika.code;
const palikaLabelSelector = labelSelector;

const languageOptionsLabelSelector = l => l.title;
const languageOptionsKeySelector = l => l.key;

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
            language: [requiredCondition],
        },
    }

    constructor(props) {
        super(props);

        this.state = {
            faramValues: {
                language: ENGLISH,
            },
            faramErrors: {},
            activeTab: 'validation',
            // pristine: true,
        };

        this.views = {
            progress: {
                component: () => {
                    const {
                        requests: {
                            generatorTriggerExport,
                            generatorTriggerExportPoll,
                        },
                        exportState,
                    } = this.props;

                    const exportPending = (
                        generatorTriggerExportPoll.pending || generatorTriggerExport.pending
                    );

                    return (
                        <div className={styles.exportStatus}>
                            {exportPending ? (
                                <TaskStatus
                                    {...exportState}
                                />
                            ) : (
                                <div className={styles.messageContainer}>
                                    <Message>
                                        Export has not been started
                                    </Message>
                                </div>
                            )}
                        </div>
                    );
                },
                wrapContainer: true,
            },
            validation: {
                component: () => {
                    const { errors } = this.props;

                    return (
                        <ValidatorPreview errors={errors} />
                    );
                },
                wrapContainer: true,
            },
        };
    }

    componentDidMount() {
        // NOTE: This is for debugging only
        const {
            generator: { id },
            requests: { generatorGet },
        } = this.props;
        if (id) {
            generatorGet.do({ pullMeta: true });
        }
    }

    getFilteredDistrictList = memoize((districts, selectedProvince) => {
        if (selectedProvince && selectedProvince.length) {
            return districts.filter(
                district => (
                    selectedProvince.findIndex(
                        provinceId => provinceId === district.province,
                    ) !== -1
                ),
            );
        }
        return districts;
    })

    getFilteredPalikaCodeList = memoize((palikaCodes, selectedProvince, selectedDistrict) => {
        if (selectedDistrict && selectedDistrict.length) {
            return palikaCodes.filter(
                palika => (
                    selectedDistrict.findIndex(
                        districtId => districtId === palika.district,
                    ) !== -1
                ),
            );
        } if (selectedProvince && selectedProvince.length) {
            return palikaCodes.filter(
                palika => (
                    selectedProvince.findIndex(
                        provinceId => provinceId === palika.province,
                    ) !== -1
                ),
            );
        }
        return palikaCodes;
    })

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
        this.setState({
            faramValues,
            faramErrors,
            // pristine: false,
        });
    };

    handleFaramFailure = (faramErrors) => {
        this.setState({ faramErrors });
    };

    handleFaramSuccess = (_, { selectedPalikaCodes }) => {
        const {
            requests: {
                generatorTriggerExport,
            },
        } = this.props;
        this.setState({ activeTab: 'progress' });
        generatorTriggerExport.do({ selectedPalikaCodes });
    };

    handleTabClick = (activeTab) => {
        this.setState({ activeTab });
    }

    render() {
        const {
            requests: {
                generatorTriggerExport,
                generatorTriggerExportPoll,
            },
            provinces,
            districts,
            palikaCodes,

            exportState,
        } = this.props;

        const {
            activeTab,

            faramValues,
            faramErrors,
            // pristine,
        } = this.state;

        const {
            selectedProvince,
            selectedDistrict,
            selectedPalikaCodes,
        } = faramValues;

        const filteredDistricts = this.getFilteredDistrictList(districts, selectedProvince);
        const filteredPalikaCodeList = this.getFilteredPalikaCodeList(
            palikaCodes, selectedProvince, selectedDistrict,
        );

        const validatedFaramValues = {
            ...faramValues,
            selectedDistrict: this.getValidatedDistrictId(selectedDistrict, filteredDistricts),
            selectedPalikaCodes: this.getValidatedPalikaCodes(
                selectedPalikaCodes, filteredPalikaCodeList,
            ),
        };
        const exportPending = (
            generatorTriggerExportPoll.pending || generatorTriggerExport.pending
        );

        return (
            <div className={styles.export}>
                <div className={styles.top}>
                    <h1>Select Palikas</h1>
                    <Faram
                        className={styles.form}
                        onValidationSuccess={this.handleFaramSuccess}
                        onValidationFailure={this.handleFaramFailure}
                        onChange={this.handleFaramChange}
                        schema={TriggerPage.schema}
                        value={validatedFaramValues}
                        error={faramErrors}
                        disabled={exportPending}
                    >
                        <div className={styles.selectContainer}>
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
                                options={filteredDistricts}
                                showHintAndError={false}
                                placeholder="Select District"
                            />
                            <MultiSelectInput
                                faramElementName="selectedPalikaCodes"
                                keySelector={palikaKeySelector}
                                labelSelector={palikaLabelSelector}
                                options={filteredPalikaCodeList}
                                showHintAndError={false}
                                placeholder="Select Palikas"
                            />
                            <SegmentInput
                                options={languageOptions}
                                keySelector={languageOptionsKeySelector}
                                labelSelector={languageOptionsLabelSelector}
                                faramElementName="language"
                                label="Language"
                            />
                        </div>
                        <PrimaryButton
                            className={styles.button}
                            pending={exportPending}
                            type="submit"
                            iconName={iconNames.textDoc}
                        >
                            Export
                        </PrimaryButton>
                    </Faram>
                </div>
                <div className={styles.bottomContainer}>
                    <ScrollTabs
                        className={styles.tabs}
                        tabs={tabs}
                        active={activeTab}
                        onClick={this.handleTabClick}
                    />
                    <MultiViewContainer
                        views={this.views}
                        active={activeTab}
                        containerClassName={styles.view}
                    />
                </div>
            </div>
        );
    }
}

const mapStateToProps = state => ({
    generator: generatorSelectorGP(state),
    errors: generatorErrorListSelectorGP(state),
    provinces: generatorProvinceListSelectorGP(state),

    districts: generatorDistrictListSelectorGP(state),
    palikaCodes: generatorPalikaCodeListSelectorGP(state),
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
