import React from 'react';
import PropTypes from 'prop-types';
import memoize from 'memoize-one';
import { mapToList } from '@togglecorp/fujs';

import ListView from '#rscv/List/ListView';

import ErrorItem from './ErrorItem';
import styles from './styles.scss';


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

    getGroupedErrors = memoize((errors) => {
        const groupedErrors = {};
        errors.forEach((e) => {
            if (groupedErrors[e.index]) {
                groupedErrors[e.index].columns = [
                    e,
                    ...groupedErrors[e.index].columns,
                ];
            } else {
                groupedErrors[e.index] = {
                    index: e.index,
                    columns: [e],
                };
            }
        });
        const groupedErrorsList = mapToList(
            groupedErrors,
            (d, k) => ({
                index: k,
                ...d,
            }),
        );
        return groupedErrorsList;
    });

    rendererParams = (_, error) => ({
        ...error,
    });

    render() {
        const { errors } = this.props;
        const groupedErrors = this.getGroupedErrors(errors);

        return (
            <ListView
                data={groupedErrors}
                keySelector={keySelector}
                rendererParams={this.rendererParams}
                renderer={ErrorItem}
            />
        );
    }
}

export default ValidatorPreview;
