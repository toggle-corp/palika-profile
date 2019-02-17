import {
    createRequestCoordinator,
    createRequestClient,
    RestRequest,
} from '@togglecorp/react-rest-request';

import update from '#rsu/immutable-update';

// TODO: Use env variable to fill endpoint
const wsEndpoint = '/api/v1';

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

export const RequestCoordinator = createRequestCoordinator({
    transformUrl: (url) => {
        if (/^https?:\/\//i.test(url)) {
            return url;
        }

        return `${wsEndpoint}${url}`;
    },

    transformParams: (params) => {
        const csrfToken = getCookie('csrftoken');
        if (!csrfToken) {
            return params;
        }

        const settings = {
            headers: { $auto: {
                'X-CSRFToken': { $set: csrfToken },
            } },
        };

        return update(params, settings);
    },

    transformErrors: (response) => {
        const faramErrors = alterResponseErrorToFaramError(response.errors);
        return {
            response,
            faramErrors,
        };
    },
});

export const RequestClient = createRequestClient();
export const requestMethods = RestRequest.methods;
