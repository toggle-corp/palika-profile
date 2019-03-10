import { requestMethods } from '#request';

const requests = {
    generatorGet: {
        method: requestMethods.GET,
        url: ({
            props: {
                generator: { id },
            },
        }) => `/generators/${id}/errors/`,
        onSuccess: ({
            response,
            props: {
                updateGenerator,
            },
        }) => (
            updateGenerator({
                $auto: {
                    errors: { $set: response.errors },
                },
            })
        ),
        onFailure: () => console.warn('failure'),
        onFatal: () => console.warn('fatal'),
    },

    generatorTriggerValidator: {
        method: requestMethods.GET,
        url: ({
            props: { generator: { id } },
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
        options: ({ props: { setState } }) => ({
            pollTime: 1000,
            shouldPoll: ({ state }) => {
                const breakPoll = (
                    state === 'success' || state === 'failure'
                );
                if (!breakPoll) {
                    setState(state);
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
            props: { setStatus },
        }) => {
            setStatus(state);
            generatorGet.do({ generatorId: id });
        },
        onFailure: () => console.warn('failure'),
        onFatal: () => console.warn('fatal'),
    },
};

export default requests;
