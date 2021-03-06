import { requestMethods } from '#request';

const requests = {
    generatorAdd: {
        method: requestMethods.POST,
        url: '/generators/',
        body: ({ params: { data } }) => data,
        extras: { isFormData: true },
        onSuccess: ({
            response,
            props: {
                setGenerator,
                onNext,
            },
        }) => {
            setGenerator({ generator: response });
            onNext();
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
};

export default requests;
