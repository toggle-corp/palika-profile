import update from '#rsu/immutable-update';

import {
    createRequestCoordinator,
    createRequestClient,
    methods,
    prepareUrlParams,
} from '@togglecorp/react-rest-request';

export * from '@togglecorp/react-rest-request';

const wsEndpoint = process.env.RP_WS_ENDPOINT || '/api/v1';

const getCookie = (name) => {
    if (!document.cookie) {
        return null;
    }

    const xsrfCookies = document.cookie.split(';')
        .map(c => c.trim())
        .filter(c => c.startsWith(`${name}=`));

    if (xsrfCookies.length === 0) {
        return null;
    }

    return decodeURIComponent(xsrfCookies[0].split('=')[1]);
};

export const alterResponseErrorToFaramError = (errors) => {
    const {
        nonFieldErrors = [],
        ...formFieldErrors
    } = errors;

    return Object.keys(formFieldErrors).reduce(
        (acc, key) => {
            const error = formFieldErrors[key];
            acc[key] = Array.isArray(error) ? error.join(' ') : error;
            return acc;
        },
        {
            $internal: nonFieldErrors,
        },
    );
};


export const createConnectedRequestCoordinator = () => createRequestCoordinator({
    transformParams: (params) => {
        const csrfToken = getCookie('csrftoken');

        const {
            extras: {
                isFormData = false,
            } = {},
        } = params;

        if (isFormData) {
            return {
                method: params.method,
                body: params.body,
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            };
        }
        const newParams = {
            method: params.method,
            body: JSON.stringify(params.body),
            headers: {
                'X-CSRFToken': csrfToken,
                Accept: 'application/json',
                'Content-Type': 'application/json; charset=utf-8',
            },
        };
        return newParams;
    },

    transformProps: props => props,

    transformUrl: (url) => {
        if (/^https?:\/\//i.test(url)) {
            return url;
        }

        return `${wsEndpoint}${url}`;
    },

    transformErrors: (response) => {
        const faramErrors = alterResponseErrorToFaramError(response.errors);
        return {
            response,
            faramErrors,
        };
    },
});

export const RequestClient = createRequestClient;
export const RequestCoordinator = createConnectedRequestCoordinator();
export const requestMethods = methods;
export const P = prepareUrlParams;
