import React from 'react';
import PropTypes from 'prop-types';

import Sortable from '#rscv/Taebul/Sortable';
import ColumnWidth from '#rscv/Taebul/ColumnWidth';
import NormalTaebul from '#rscv/Taebul';
import TaskStatus from '#components/TaskStatus';

import columns from './columns';
import styles from './styles.scss';

const Taebul = Sortable(ColumnWidth(NormalTaebul));

const propTypes = {
    /* eslint-disable react/forbid-prop-types */
    errors: PropTypes.array,
    progress: PropTypes.object,
    /* eslint-enable react/forbid-prop-types */
};

const defaultProps = {
    progress: {},
    errors: undefined,
};

const keySelector = datum => `${datum.index}-${datum.column}`;

class ValidatorPreview extends React.PureComponent {
    static propTypes = propTypes;
    static defaultProps = defaultProps;

    constructor(props) {
        super(props);

        this.state = {
            taebulOptions: {
                defaultColumnWidth: 250,
                minColumnWidth: 250,
            },
        };
    }

    handleSettingsChange = (options) => {
        this.setState({ taebulOptions: options });
    }

    render() {
        const {
            progress,
            errors,
        } = this.props;

        const {
            taebulOptions,
        } = this.state;

        if (errors) {
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
        return (
            <TaskStatus
                progress={progress}
            />
        );
    }
}

export default ValidatorPreview;
