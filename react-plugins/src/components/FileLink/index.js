import React from 'react';
import memoize from 'memoize-one';
import PropTypes from 'prop-types';
import { _cs } from '@togglecorp/fujs';

import { P } from '#request';
import styles from './styles.scss';

const FileLink = ({ url, label }) => {
    if (url) {
        const filename = label || url.split('/').pop();
        return (
            <a
                href={url}
                target="_blank"
                rel="noopener noreferrer"
                className={styles.link}
            >
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
                <div
                    key={keySelector(exp)}
                    className={styles.file}
                >
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
        className: PropTypes.string,
        filesContainerClassName: PropTypes.string,
    };
    static defaultProps = {
        className: '',
        filesContainerClassName: '',
        generator: {},
    };

    getDownloadAsZipUrl = memoize(id => (
        `/download-palika-documents?${P({ generatorId: id })}`
    ))

    render() {
        const {
            filesContainerClassName,
            className,
            generator: {
                id,
                exports,
            },
        } = this.props;
        if (exports && exports.length) {
            return (
                <div className={_cs(className, styles.container)}>
                    <a
                        className={styles.downloadZip}
                        href={this.getDownloadAsZipUrl(id)}
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        <span className={_cs(styles.icon, 'ion-ios-download-outline')} />
                        Download as zip
                    </a>
                    <div className={_cs(styles.filesContainer, filesContainerClassName)}>
                        <FileLinks
                            urls={exports}
                            keySelector={fileKeySelector}
                            labelSelector={fileLabelSelector}
                            urlSelector={fileUrlSelector}
                        />
                    </div>
                </div>
            );
        }
        return (
            <div className={className}>
                No exports found.
            </div>
        );
    }
}

export default FileLink;
