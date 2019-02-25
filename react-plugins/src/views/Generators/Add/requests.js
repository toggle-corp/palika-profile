import { requestMethods } from '#request';

const requests = {
    generatorAdd: {
        method: requestMethods.POST,
        url: '/generators/',
        body: ({ params: { data } }) => data,
        extras: { isFormData: true },
        onSuccess: ({
            response, params: { setState },
        }) => {
            setState({ generator: response });
        },
        onFailure: ({
            params: { setState },
            error: { faramErrors },
        }) => setState({ faramErrors }),
        onFatal: ({
            params: { setState },
        }) => setState({ processStatus: 'Fatal' }),
    },

    generatorGet: {
        method: requestMethods.GET,
        url: ({
            params: {
                generatorId,
                hasValidationErrors,
            },
        }) => (
            hasValidationErrors
                ? `/generators/${generatorId}/errors/`
                : `/generators/${generatorId}/`
        ),
        onSuccess: ({
            response,
            params: {
                updateGenerator,
                hasValidationErrors,
            },
        }) => (
            hasValidationErrors
                ? updateGenerator({
                    $auto: {
                        errors: { $set: response.errors },
                    },
                })
                : updateGenerator({ $set: response })
        ),
        onFailure: () => console.warn('failure'),
        onFatal: () => console.warn('fatal'),
    },

    generatorTriggerExport: {
        method: requestMethods.GET,
        url: ({
            params: { generatorId },
        }) => (
            `/generators/${generatorId}/trigger-export`
        ),
        onSuccess: ({
            response: { taskId },
            props: {
                requests: { generatorTriggerExportPoll },
            },
        }) => generatorTriggerExportPoll.do({ taskId }),
        onFailure: () => console.warn('failure'),
        onFatal: () => console.warn('fatal'),
    },

    generatorTriggerExportPoll: {
        method: requestMethods.GET,
        url: ({
            params: { taskId },
        }) => `/tasks/${taskId}/`,
        options: ({ params: { setState } }) => ({
            pollTime: 1000,
            shouldPoll: ({ state }) => {
                const breakPoll = (
                    state === 'success' || state === 'failure'
                );
                if (!breakPoll) {
                    setState({ exportState: state });
                    return true;
                }
                return false;
            },
        }),
        onSuccess: ({
            response: { state },
            props: { requests: { generatorGet } },
            params: { setState, getGeneratorId },
        }) => {
            setState({ exportStatus: state });
            generatorGet.do({ generatorId: getGeneratorId() });
        },
        onFailure: () => console.warn('failure'),
        onFatal: () => console.warn('fatal'),
    },

    generatorTriggerValidator: {
        method: requestMethods.GET,
        url: ({
            params: { generatorId },
        }) => (
            `/generators/${generatorId}/trigger-validation`
        ),
        onSuccess: ({
            response: { taskId },
            props: {
                requests: { generatorTriggerValidatorPoll },
            },
        }) => generatorTriggerValidatorPoll.do({ taskId }),
        onFailure: () => console.warn('failure'),
        onFatal: () => console.warn('fatal'),
    },

    generatorTriggerValidatorPoll: {
        method: requestMethods.GET,
        url: ({
            params: { taskId },
        }) => `/tasks/${taskId}/`,
        options: ({ params: { setState } }) => ({
            pollTime: 1000,
            shouldPoll: ({ state }) => {
                const breakPoll = (
                    state === 'success' || state === 'failure'
                );
                if (!breakPoll) {
                    setState({ validationState: state });
                    return true;
                }
                return false;
            },
        }),
        onSuccess: ({
            response: { state },
            props: { requests: { generatorGet } },
            params: { setState, getGeneratorId },
        }) => {
            setState({ validationStatus: state });
            generatorGet.do({
                generatorId: getGeneratorId(),
                hasValidationErrors: true,
            });
        },
        onFailure: () => console.warn('failure'),
        onFatal: () => console.warn('fatal'),
    },
};

export default requests;
