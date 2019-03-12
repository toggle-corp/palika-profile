import { requestMethods } from '#request';

const requests = {
    generatorAdd: {
        method: requestMethods.POST,
        url: '/generators/',
        body: ({ params: { data } }) => data,
        extras: { isFormData: true },
        onSuccess: ({
            response, props: {
                setGenerator,
                requests: { generatorTriggerValidator },
            },
        }) => {
            setGenerator({ generator: response });
            generatorTriggerValidator.do({ id: response.id });
        },
        onFailure: ({ params: { setState }, error: { faramErrors } }) => setState({ faramErrors }),
        onFatal: ({ params: { setState } }) => (
            setState({
                faramErrors: {
                    $internal: 'Something bad happened. Try again or contact admin',
                },
            })
        ),
    },

    generatorGet: {
        method: requestMethods.GET,
        url: ({
            props: {
                generator: { id },
            },
        }) => `/generators/${id}/meta/`,
        onSuccess: ({
            response,
            props: { setGenerator, onNext },
        }) => {
            setGenerator({ generator: response });
            onNext();
        },
        onFailure: () => console.warn('failure'),
        onFatal: () => console.warn('fatal'),
    },

    generatorTriggerValidator: {
        method: requestMethods.GET,
        url: ({
            params: { id },
        }) => `/generators/${id}/trigger-validation`,
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
        options: ({ props: { setGeneratorState } }) => ({
            pollTime: 1000,
            shouldPoll: ({ state }) => {
                const breakPoll = (
                    state === 'success' || state === 'failure'
                );
                if (!breakPoll) {
                    setGeneratorState({ validationState: state });
                    return true;
                }
                return false;
            },
        }),
        onSuccess: ({
            response: { state },
            props: {
                requests: { generatorGet },
                generator: { id },
            },
            props: { setGeneratorStatus },
        }) => {
            setGeneratorStatus({ validationStatus: state });
            generatorGet.do({ generatorId: id });
        },
        onFailure: () => console.warn('failure'),
        onFatal: () => console.warn('fatal'),
    },
};

export default requests;
