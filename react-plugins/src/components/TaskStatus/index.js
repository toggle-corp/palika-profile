import React from 'react';

const emptyObject = {};
const emptyList = [];

const TaskStatus = ({
    progress: {
        items = emptyList,
        itemList = emptyList,
    } = emptyObject,
}) => (
    itemList.map(
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
    )
);

export default TaskStatus;
