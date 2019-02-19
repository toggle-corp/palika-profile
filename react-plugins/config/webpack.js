const path = require('path');

const appBase = process.cwd();
const appSrc = path.resolve(appBase, 'src/');

module.exports = {
    entry: './src/index.js',
    output: {
        path: path.resolve(appBase, process.env.RP_KITAB_BUILD_DIR || '../kitab/static/js/'),
        filename: 'react-plugins.js',
        library: 'reactPlugins',
        libraryTarget: 'umd',
    },
    // FIXME: Right now react-rest-request is not working with production mode
    mode: 'development',
    resolve: {
        alias: {
            'base-scss': path.resolve(appBase, 'src/stylesheets/'),
            'rs-scss': path.resolve(appBase, 'src/vendor/react-store/stylesheets/'),
        },
        symlinks: false,
    },

    devtool: 'source-map',

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
