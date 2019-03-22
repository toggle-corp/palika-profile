import React from 'react';

import Spinner from '#rscz/Spinner';

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
                    <div
                        key={item}
                        className={styles.item}
                    >
                        <span>{`${item}:  `}</span>
                        <span>
                            {
                                typeof (items[item]) === 'object'
                                    ? `${items[item].complete}/${items[item].total}`
                                    : items[item]
                            }
                        </span>
                    </div>
                ))}
            </div>
        );
    }
    return (
        <div className={styles.container}>
            <Spinner />
        </div>
    );
};

export default TaskStatus;
