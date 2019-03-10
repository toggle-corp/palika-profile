import { requestMethods } from '#request';

const requests = {
    generatorGet: {
        method: requestMethods.GET,
        url: ({ props: { generator: { id } } }) => `/generators/${id}/`,
        onSuccess: ({
            response,
            props: { updateGenerator },
        }) => updateGenerator({ $set: response }),
        onFailure: () => console.warn('failure'),
        onFatal: () => console.warn('fatal'),
    },

    generatorTriggerExport: {
        method: requestMethods.GET,
        url: ({ props: { generator: { id } } }) => `/generators/${id}/trigger-export`,
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
            props: { generator: { id }, requests: { generatorGet }, setStatus },
        }) => {
            setStatus(state);
            generatorGet.do({ generatorId: id });
        },
        onFailure: () => console.warn('failure'),
        onFatal: () => console.warn('fatal'),
    },
};

export default requests;
