import React from 'react';


const FileLink = ({ url }) => {
    if (url) {
        const filename = url.split('/').pop();
        return (
            <a href={url}>
                {filename}
            </a>
        );
    }
    return '';
};

export default FileLink;
