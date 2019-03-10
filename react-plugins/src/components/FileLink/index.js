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

export const FileLinks = ({ urls, keySelector, urlSelector }) => {
    if (urls) {
        return urls.map(
            exp => (
                <div key={keySelector(exp)}>
                    <FileLink
                        url={urlSelector(exp)}
                    />
                </div>
            ),
        );
    }
    return '';
};


export default FileLink;
