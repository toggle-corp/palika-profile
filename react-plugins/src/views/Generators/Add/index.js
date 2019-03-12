import React from 'react';
import Wizard from '#rscv/Wizard';

import UploadPage from './UploadPage';
import ValidationPage from './ValidationPage';
import ExportPage from './ExportPage';
import FinalPage from './FinalPage';


const GeneratorAdd = () => (
    <Wizard>
        <UploadPage />
        <ValidationPage />
        <ExportPage />
        <FinalPage />
    </Wizard>
);

export default GeneratorAdd;
