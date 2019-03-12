import { requestMethods } from '#request';

const requests = {
    generatorGet: {
        method: requestMethods.GET,
        url: ({
            props: { generator: { id } },
            params: { getExportState },
        }) => (
            getExportState ? `/generators/${id}/data/` : `/generators/${id}/`
        ),
        onSuccess: ({
            response,
            props: { setGenerator },
        }) => setGenerator({ generator: response }),
        onFailure: () => console.warn('failure'),
        onFatal: () => console.warn('fatal'),
    },
};

export default requests;
