import React from 'react';
import FormattedDate from '#rscv/FormattedDate';
import iconNames from '#rsk/iconNames';
import FileLink, { GeneratorExportsDownload } from '#components/FileLink';

const RenderStatus = ({ status }) => {
    if (status) {
        let icon = iconNames.error;
        let title = 'Failure';

        if (status === 'success') {
            icon = iconNames.check;
            title = 'Success';
        } else if (status === 'pending') {
            icon = iconNames.loading;
            title = 'Pending';
        }

        return (
            <span className={icon} title={title} />
        );
    }
    return '';
};


const headers = [
    {
        key: 'createdAt',
        label: 'Created At',
        order: 1,
        modifier: generator => (
            <FormattedDate
                value={generator.createdAt}
                showLabel={false}
                mode="dd-MM-yyyy hh:mm"
                emptyComponent={null}
            />
        ),
    },
    {
        key: 'status',
        label: 'Status',
        order: 2,
        modifier: generator => (
            <RenderStatus
                status={generator.status}
            />
        ),
    },
    {
        key: 'file',
        label: 'File',
        order: 3,
        modifier: generator => (
            <FileLink
                url={generator.file}
            />
        ),
    },
    {
        key: 'export',
        label: 'Exports',
        order: 3,
        modifier: generator => (
            <GeneratorExportsDownload
                generator={generator}
            />
        ),
    },
];

export default headers;
