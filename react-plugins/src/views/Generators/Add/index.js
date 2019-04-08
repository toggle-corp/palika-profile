import React from 'react';
import Wizard from '#rscv/Wizard';

import UploadPage from './UploadPage';
import ValidationPage from './ValidationPage';
import ExportPage from './ExportPage';
import FinalPage from './FinalPage';

import styles from './styles.scss';

const GeneratorAdd = () => (
    <div className={styles.wizardContainer}>
        <div className={styles.header}>
            <a
                className={styles.downloadButton}
                href="/static/palika/sample_template.xlsx"
                target="_blank"
                rel="noopener noreferrer"
            >
                <span className="ion-ios-download-outline" />
                Sample sheet
            </a>
            {/*
            <a
                className={styles.downloadButton}
                href="https://imgur.com/gallery/XXWzc0z"
            >
                <span className="ion-ios-download-outline" />
                Shape files
            </a>
            */}
        </div>
        <Wizard
            className={styles.wizard}
        >
            <UploadPage />
            <ValidationPage />
            <ExportPage />
            <FinalPage />
        </Wizard>
    </div>
);

export default GeneratorAdd;
