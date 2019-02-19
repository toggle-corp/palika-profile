const path = require('path');

const appBase = process.cwd();
const appSrc = path.resolve(appBase, 'src/');

module.exports = {
    entry: './src/index.js',
    output: {
        path: path.resolve(appBase, '../kitab/static/js/'),
        filename: 'react-plugins.js',
        library: 'reactPlugins',
        libraryTarget: 'umd',
    },
    mode: 'development',
    devServer: {
        host: '0.0.0.0',
        port: 3008,
        overlay: true,
        watchOptions: {
            ignored: /node_modules/,
        },
        // Don't show warnings in browser console
        clientLogLevel: 'none',
    },
    resolve: {
        alias: {
            'base-scss': path.resolve(appBase, 'src/stylesheets/'),
            'rs-scss': path.resolve(appBase, 'src/vendor/react-store/stylesheets/'),
        },
        symlinks: false,
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                include: appSrc,
                use: {
                    loader: 'babel-loader',
                },
            },
            {
                test: /\.scss$/,
                include: appSrc,
                use: [
                    'style-loader',
                    {
                        loader: require.resolve('css-loader'),
                        options: {
                            importLoaders: 1,
                            modules: true,
                            camelCase: true,
                            localIdentName: '[name]_[local]_[hash:base64]',
                            sourceMap: true,
                        },
                    },
                    {
                        loader: require.resolve('sass-loader'),
                        options: {
                            sourceMap: true,
                        },
                    },
                ],
            },
        ],
    },
};
