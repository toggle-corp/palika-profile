import React from 'react';
import Wizard from '#rscv/Wizard';

import FormPage from './FormPage';

// eslint-disable-next-line
class GeneratorAdd extends React.PureComponent {
    render() {
        return (
            <Wizard>
                <FormPage />
            </Wizard>
        );
    }
}

export default GeneratorAdd;
