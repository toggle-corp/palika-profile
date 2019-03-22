import React from 'react';
import PropTypes from 'prop-types';

import { _cs } from '@togglecorp/fujs';

import styles from './styles.scss';

const propTypes = {
    className: PropTypes.string,
    label: PropTypes.string.isRequired,
    labelClassName: PropTypes.string,
    valueClassName: PropTypes.string,
    value: PropTypes.oneOfType([
        PropTypes.number,
        PropTypes.string,
    ]),
    type: PropTypes.string,
};

const defaultProps = {
    className: '',
    labelClassName: '',
    valueClassName: '',
    value: 'N/A',
    type: 'normal',
};

export default class InfoGroup extends React.PureComponent {
    static propTypes = propTypes;
    static defaultProps = defaultProps;

    render() {
        const {
            valueClassName,
            labelClassName,
            className,
            label,
            value,
            type,
        } = this.props;

        return (
            <div
                className={_cs(
                    type === '' && styles.infoGroup,
                    type === 'normal' && styles.normalInfoGroup,
                    type === 'table' && styles.tableInfoGroup,
                    className,
                )}
            >
                <div className={_cs(styles.infoLabel, labelClassName)}>
                    {label}
                </div>
                <div className={_cs(styles.infoValue, valueClassName)}>
                    {value}
                </div>
            </div>
        );
    }
}
