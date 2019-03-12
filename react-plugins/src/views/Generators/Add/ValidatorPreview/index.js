import React from 'react';
import PropTypes from 'prop-types';

import Sortable from '#rscv/Taebul/Sortable';
import ColumnWidth from '#rscv/Taebul/ColumnWidth';
import NormalTaebul from '#rscv/Taebul';

import columns from './columns';
import styles from './styles.scss';

const Taebul = Sortable(ColumnWidth(NormalTaebul));

const propTypes = {
    // eslint-disable-next-line react/forbid-prop-types
    errors: PropTypes.array,
};

const defaultProps = {
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
        const { errors } = this.props;

        const {
            taebulOptions,
        } = this.state;

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
}

export default ValidatorPreview;
