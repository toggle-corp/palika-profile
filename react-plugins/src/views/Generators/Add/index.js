import React from 'react';
import Wizard from '#rscv/Wizard';
import update from '#rsu/immutable-update';

import FormPage from './FormPage';
import TriggerPage from './TriggerPage';
import ExportPage from './ExportPage';


class GeneratorAdd extends React.PureComponent {
    constructor(props) {
        super(props);

        this.state = {
            generator: {},

            exportState: undefined,
            exportStatus: undefined,

            validationState: undefined,
            validationStatus: undefined,
        };
    }

    onAddSuccess = (generator) => {
        this.setState({ generator });
    };

    updateGenerator = (settings) => {
        const { generator } = this.state;
        const newGenerator = update(generator, settings);
        this.setState({
            generator: newGenerator,
        });
    }

    setExportState = state => this.setState({ exportState: state });
    setExportStatus = state => this.setState({ exportStatus: state });

    setValidationState = state => this.setState({ validationState: state });
    setValidationStatus = state => this.setState({ validationStatus: state });

    render() {
        const {
            generator,

            exportState,
            exportStatus,

            validationState,
            validationStatus,
        } = this.state;

        return (
            <Wizard>
                <FormPage
                    generator={generator}
                    onSuccess={this.onAddSuccess}
                />
                <TriggerPage
                    generator={generator}
                    updateGenerator={this.updateGenerator}
                    setState={this.setValidationState}
                    setStatus={this.setValidationStatus}
                    exportState={validationState}
                    exportStatus={validationStatus}
                />
                <ExportPage
                    generator={generator}
                    updateGenerator={this.updateGenerator}
                    setState={this.setExportState}
                    setStatus={this.setExportStatus}
                    exportState={exportState}
                    exportStatus={exportStatus}
                />
            </Wizard>
        );
    }
}

export default GeneratorAdd;
