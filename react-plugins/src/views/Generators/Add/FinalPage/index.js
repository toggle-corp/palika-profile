import React from 'react';
import PropTypes from 'prop-types';
import { compose } from 'redux';
import { connect } from 'react-redux';

import PrimaryButton from '#rsca/Button/PrimaryButton';

import { GeneratorExportsDownload } from '#components/FileLink';
import TaskStatus from '#components/TaskStatus';

import {
    RequestCoordinator,
    RequestClient,
} from '#request';

import {
    setGeneratorActionGP,
} from '#actionCreators';
import {
    generatorSelectorGP,
    exportStatusSelectorGP,
} from '#selectors';
import requests from './requests';
import styles from './styles.scss';

const propTypes = {
    /* eslint-disable react/forbid-prop-types */
    requests: PropTypes.object.isRequired,
    generator: PropTypes.object.isRequired,
    /* eslint-enable react/forbid-prop-types */
    exportStatus: PropTypes.string,
    onPrev: PropTypes.func.isRequired,
};

const defaultProps = {
    exportStatus: undefined,
};
const emptyObject = {};

class ExportPage extends React.PureComponent {
    static propTypes = propTypes;
    static defaultProps = defaultProps;

    componentDidMount() {
        const {
            requests: {
                generatorGet,
            },
            generator,
            exportStatus,
        } = this.props;
        if (exportStatus === 'failed') {
            generatorGet.do({ getExportState: true });
        } else if (!generator.exports) {
            // NOTE: This is for debugging only
            generatorGet.do();
        }
    }

    render() {
        const {
            generator,
            exportStatus,
            onPrev,
        } = this.props;

        const { data = emptyObject } = generator;

        if (!exportStatus === 'failed') {
            return (
                <div>
                    <h1>Failed to generate PDFs</h1>
                    <h3>Server Error:</h3>
                    <code>
                        {data.errors}
                    </code>
                    <h3>Final Status:</h3>
                    <TaskStatus
                        progress={data.progress}
                    />
                </div>
            );
        }

        return (
            <div className={styles.container}>
                <div>
                    <PrimaryButton
                        onClick={onPrev}
                        className={styles.button}
                    >
                        Back
                    </PrimaryButton>
                </div>
                <div className={styles.content}>
                    <div className={styles.downImage}>
                        Download files
                    </div>
                    <GeneratorExportsDownload
                        className={styles.downloads}
                        generator={generator}
                    />
                </div>
            </div>
        );
    }
}


const mapStateToProps = state => ({
    generator: generatorSelectorGP(state),
    exportStatus: exportStatusSelectorGP(state),
});

const mapDispatchToProps = dispatch => ({
    setGenerator: params => dispatch(setGeneratorActionGP(params)),
});

export default compose(
    connect(mapStateToProps, mapDispatchToProps),
    RequestCoordinator,
    RequestClient(requests),
)(ExportPage);
