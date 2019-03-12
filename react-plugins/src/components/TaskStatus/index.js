import React from 'react';

const emptyObject = {};
const emptyList = [];

const TaskStatus = ({
    progress: {
        items = emptyList,
        itemList = emptyList,
    } = emptyObject,
}) => {
    if (itemList && itemList.length) {
        return itemList.map(
            item => (
                <div key={item}>
                    <span>{`${item}:  `}</span>
                    <span>
                        {
                            typeof (items[item]) === 'object'
                                ? `${items[item].complete}/${items[item].total}`
                                : items[item]
                        }
                    </span>
                </div>
            ),
        );
    }
    return '..';
};

export default TaskStatus;
