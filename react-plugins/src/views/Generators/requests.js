import { requestMethods } from '#request';

const requests = {
    generatorsGet: {
        method: requestMethods.GET,
        onMount: true,
        url: '/generators/',
    },
};

export default requests;
