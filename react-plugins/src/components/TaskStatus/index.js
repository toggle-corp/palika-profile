import React from 'react';

import Spinner from '#rscz/Spinner';
import { _cs } from '@togglecorp/fujs';

import InfoGroup from '#components/InfoGroup';

import styles from './styles.scss';

const emptyObject = {};
const emptyList = [];

const TaskStatus = ({
    progress: {
        items = emptyList,
        itemList = emptyList,
    } = emptyObject,
}) => {
    if (itemList && itemList.length) {
        return (
            <div className={styles.container}>
                {itemList.map(item => (
                    <InfoGroup
                        label={item}
                        type="table"
                        value={
                            typeof (items[item]) === 'object'
                                ? `${items[item].complete}/${items[item].total}`
                                : items[item]
                        }
                    />
                ))}
            </div>
        );
    }
    return (
        <div className={_cs(styles.container, styles.spinnerContainer)}>
            <Spinner className={styles.spinner} />
        </div>
    );
};

export default TaskStatus;
