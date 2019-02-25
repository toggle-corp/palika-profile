import React from 'react';
import PropTypes from 'prop-types';

import Table from '#rscv/Table';

import {
    RequestCoordinator,
    RequestClient,
} from '#request';

import requests from './requests';
import headers from './headers';
import styles from './styles.scss';

const propTypes = {
    // eslint-disable-next-line react/forbid-prop-types
    requests: PropTypes.object.isRequired,
};

const defaultProps = {};
const emptyObject = {};
const emptyArray = [];
const keySelector = generator => generator.id;

@RequestCoordinator
@RequestClient(requests)
class Generator extends React.PureComponent {
    static propTypes = propTypes;
    static defaultProps = defaultProps;

    render() {
        const {
            requests: {
                generatorsGet: {
                    response: {
                        results: generators = emptyArray,
                    } = emptyObject,
                },
            },
        } = this.props;

        return (
            <div>
                <Table
                    className={styles.table}
                    data={generators}
                    headers={headers}
                    keySelector={keySelector}
                />
            </div>
        );
    }
}

export default Generator;
