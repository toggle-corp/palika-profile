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
            generator: {
            },
            selectedPalikaCodes: undefined,

            exportState: undefined,
            exportStatus: undefined,
        };
    }

    updateGenerator = (settings) => {
        const { generator } = this.state;
        const newGenerator = update(generator, settings);
        this.setState({
            generator: newGenerator,
        });
    }

    setPalikaCodes = ({
        selectedPalikaCodes,
        callback,
    }) => {
        this.setState({ selectedPalikaCodes }, callback);
    }

    setExportState = state => this.setState({ exportState: state });
    setExportStatus = state => this.setState({ exportStatus: state });

    setValidationState = state => this.setState({ validationState: state });
    setValidationStatus = state => this.setState({ validationStatus: state });

    render() {
        const {
            generator,
            selectedPalikaCodes,

            exportState,
            exportStatus,
        } = this.state;

        return (
            <Wizard>
                <FormPage />
                <TriggerPage
                    setPalikaCodes={this.setPalikaCodes}
                />
                <ExportPage
                    generator={generator}
                    selectedPalikaCodes={selectedPalikaCodes}
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
