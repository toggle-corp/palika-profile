import { requestMethods } from '#request';

const requests = {
    generatorGet: {
        method: requestMethods.GET,
        url: ({
            params: { pullMeta },
            props: {
                generator: { id },
            },
        }) => (
            pullMeta ? `/generators/${id}/meta/` : `/generators/${id}/`
        ),
        onSuccess: ({
            response,
            props: { setGenerator, onNext },
            params: { callOnNext },
        }) => {
            setGenerator({ generator: response });
            if (callOnNext) {
                onNext();
            }
        },
        onFailure: () => console.warn('failure'),
        onFatal: () => console.warn('fatal'),
    },

    generatorTriggerExport: {
        method: requestMethods.POST,
        url: ({ props: { generator: { id } } }) => `/generators/${id}/trigger-export/`,
        body: ({ params: { selectedPalikaCodes } }) => ({ selectedPalikaCodes }),
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
        options: ({ props: { setGeneratorState } }) => ({
            pollTime: 1000,
            shouldPoll: ({ state }) => {
                const breakPoll = (
                    state === 'success' || state === 'failure'
                );
                if (!breakPoll) {
                    setGeneratorState({ exportState: state });
                    return true;
                }
                return false;
            },
        }),
        onSuccess: ({
            response: { state },
            props: {
                generator: { id },
                requests: { generatorGet },
                setGeneratorStatus,
            },
        }) => {
            setGeneratorStatus({ exportStatus: state });
            generatorGet.do({
                generatorId: id,
                callOnNext: true,
            });
        },
        onFailure: () => console.warn('failure'),
        onFatal: () => console.warn('fatal'),
    },
};

export default requests;
