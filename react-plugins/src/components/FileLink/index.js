import React from 'react';
import memoize from 'memoize-one';
import PropTypes from 'prop-types';

import { P } from '#request';

const FileLink = ({ url, label }) => {
    if (url) {
        const filename = label || url.split('/').pop();
        return (
            <a href={url}>
                {filename}
            </a>
        );
    }
    return '';
};

export const FileLinks = ({ urls, keySelector, labelSelector, urlSelector }) => {
    if (urls) {
        return urls.map(
            exp => (
                <div key={keySelector(exp)}>
                    <FileLink
                        url={urlSelector(exp)}
                        label={labelSelector(exp)}
                    />
                </div>
            ),
        );
    }
    return '';
};


const fileKeySelector = file => file.id;
const fileLabelSelector = file => file.title;
const fileUrlSelector = file => file.file;

export class GeneratorExportsDownload extends React.PureComponent {
    static propTypes = {
        // eslint-disable-next-line react/forbid-prop-types
        generator: PropTypes.object,
    };
    static defaultProps = {
        generator: {},
    };

    getDownloadAsZipUrl = memoize(id => (
        `/download-palika-documents?${P({ generatorId: id })}`
    ))

    render() {
        const {
            generator: {
                id,
                exports,
            },
        } = this.props;
        if (exports && exports.length) {
            return (
                <div>
                    <FileLinks
                        urls={exports}
                        keySelector={fileKeySelector}
                        labelSelector={fileLabelSelector}
                        urlSelector={fileUrlSelector}
                    />
                    <a
                        href={this.getDownloadAsZipUrl(id)}
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        Download as zip
                    </a>
                </div>
            );
        }
        return 'No export found..';
    }
}

export default FileLink;
