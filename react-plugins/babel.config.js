module.exports = function config(api) {
    api.cache(true);

    return {
        presets: [
            '@babel/preset-env',
            '@babel/preset-react',
        ],
        plugins: [
            ['@babel/plugin-proposal-decorators', { legacy: true }],
            ['@babel/plugin-proposal-class-properties', { loose: true }],
            '@babel/plugin-proposal-object-rest-spread',
            ['@babel/plugin-transform-runtime', { regenerator: true }],
            [
                'module-resolver',
                {
                    root: [
                        '.',
                    ],
                    alias: {
                        '#config': './src/config',
                        '#utils': './src/utils',
                        '#actionCreators': './src/store/actionCreators',
                        '#selectors': './src/store/selectors',
                        '#rscv': './src/vendor/react-store/components/View',
                        '#rsca': './src/vendor/react-store/components/Action',
                        '#rscg': './src/vendor/react-store/components/General',
                        '#rsci': './src/vendor/react-store/components/Input',
                        '#rscz': './src/vendor/react-store/components/Visualization',
                        '#rsu': './src/vendor/react-store/utils',
                        '#rsk': './src/vendor/react-store/constants',
                        '#components': './src/components',
                        '#request': './src/request',
                        '#storage': './src/storage',
                    },
                },
            ],
        ],
    };
};
