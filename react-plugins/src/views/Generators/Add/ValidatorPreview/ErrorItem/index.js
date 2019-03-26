import React from 'react';
import PropTypes from 'prop-types';
import { _cs } from '@togglecorp/fujs';
import InfoGroup from '#components/InfoGroup';

import ListView from '#rscv/List/ListView';

import styles from './styles.scss';


const propTypes = {
    className: PropTypes.string,
    index: PropTypes.number.isRequired,
    columns: PropTypes.array.isRequired, // eslint-disable-line react/forbid-prop-types
};

const defaultProps = {
    className: '',
};

const keySelector = d => d.column;

export default class ErrorItem extends React.PureComponent {
    static propTypes = propTypes;
    static defaultProps = defaultProps;

    constructor(props) {
        super(props);

        this.state = {
            expanded: false,
        };
    }

    handleErrorItemClick = () => {
        const { expanded } = this.state;
        this.setState({ expanded: !expanded });
    }

    rendererParams = (k, d) => ({
        label: d.column,
        value: d.message,
        type: 'table',
    });

    render() {
        const {
            index,
            columns,
            className,
        } = this.props;

        const { expanded } = this.state;

        return (
            <div
                className={_cs(styles.errorItem, className)}
                onClick={this.handleErrorItemClick}
                onKeyPress={() => {}}
                role="button"
                tabIndex={0}
            >
                <div className={styles.top}>
                    <div className={styles.left}>
                        <div className={styles.keyValuePair}>
                            <span className={styles.key}>Index:</span>
                            <span>{index}</span>
                        </div>
                        <div className={styles.keyValuePair}>
                            <span className={styles.key}>Number of columns with errors:</span>
                            <span>{columns.length}</span>
                        </div>
                    </div>
                </div>
                {expanded && (
                    <div className={styles.bottom}>
                        <h3>Errors</h3>
                        <ListView
                            data={columns}
                            className={styles.individualErrors}
                            rendererParams={this.rendererParams}
                            renderer={InfoGroup}
                            keySelector={keySelector}
                        />
                    </div>
                )}
            </div>
        );
    }
}
