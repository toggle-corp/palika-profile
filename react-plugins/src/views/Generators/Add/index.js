import React from 'react';
import Wizard from '#rscv/Wizard';

import UploadPage from './UploadPage';
import ValidationPage from './ValidationPage';
import ExportPage from './ExportPage';
import FinalPage from './FinalPage';

import styles from './styles.scss';


const GeneratorAdd = () => (
    <Wizard
        className={styles.wizard}
    >
        <UploadPage />
        <ValidationPage />
        <ExportPage />
        <FinalPage />
    </Wizard>
);

export default GeneratorAdd;
