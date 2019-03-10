import React from 'react';
import PropTypes from 'prop-types';

import PrimaryButton from '#rsca/Button/PrimaryButton';
import iconNames from '#rsk/iconNames';

import { FileLinks } from '#components/FileLink';
import TaskStatus from '#components/TaskStatus';

import {
    RequestCoordinator,
    RequestClient,
} from '#request';

import requests from './requests';
// import styles from './styles.scss';

const propTypes = {
    /* eslint-disable react/forbid-prop-types */
    requests: PropTypes.object.isRequired,
    generator: PropTypes.object.isRequired,
    exportState: PropTypes.object,
    exportStatus: PropTypes.string,
    /* eslint-enable react/forbid-prop-types */
    updateGenerator: PropTypes.func.isRequired,
    setState: PropTypes.func.isRequired,
    setStatus: PropTypes.func.isRequired,
    onPrev: PropTypes.func.isRequired,
};

const defaultProps = {
    exportState: {},
    exportStatus: undefined,
};
const emptyObject = {};
const emptyList = [];

const fileKeySelector = file => file.id;
const fileUrlSelector = file => file.file;

@RequestCoordinator
@RequestClient(requests)
class ExportPage extends React.PureComponent {
    static propTypes = propTypes;
    static defaultProps = defaultProps;

    componentDidMount() {
        const {
            requests: {
                generatorTriggerExport,
            },
            exportStatus,
        } = this.props;
        if (!exportStatus) {
            generatorTriggerExport.do();
        }
    }

    render() {
        const {
            generator: {
                exports = emptyList,
            } = emptyObject,
            exportState,
            exportStatus,
            onPrev,
        } = this.props;

        if (exportStatus) {
            if (exportStatus === 'success') {
                return (
                    <div>
                        <PrimaryButton
                            className={iconNames.backward}
                            onClick={onPrev}
                        >
                                Go Back
                        </PrimaryButton>
                        <FileLinks
                            urls={exports}
                            keySelector={fileKeySelector}
                            urlSelector={fileUrlSelector}
                        />
                    </div>
                );
            }
            return 'Failed';
        }

        return (
            <div>
                <TaskStatus
                    {...exportState}
                />
            </div>
        );
    }
}

export default ExportPage;
