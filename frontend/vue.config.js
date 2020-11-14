// reference: https://cli.vuejs.org/config/#vue-config-js

module.exports = {

  // https://webpack.js.org/configuration/dev-server/
  devServer: {

    /* If your frontend app and the backend API server are not
     * running on the same host, you will need to proxy API requests
     * to the API server during development. */

    // Server: 'http://10.128.202.42:8000'
    // LocalServer: 'http://localhost:8000'
    proxy: {
      '^/api/': {
        target: 'http://localhost:8000'
      },
      '^/api-auth/': {
        target: 'http://localhost:8000'
      },
      '^/admin/': {
        target: 'http://localhost:8000'
      },
      '^/static/rest_framework/': {
        target: 'http://localhost:8000'
      }
    }
  },

  // configureWebpack: {
  //   module: {
  //     rules: [
  //       {
  //         test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
  //         use: [{
  //           loader: 'url-loader',
  //           query: {
  //             limit: 10000,
  //             name: 'imgs/[name]--[folder].[ext]'
  //           }
  //         }]
  //       },
  //       {
  //         test: /\.(mp4|webm|ogg|mp3|wav|flac|aac)(\?.*)?$/,
  //         loader: 'url-loader',
  //         options: {
  //           limit: 10000,
  //           name: 'media/[name]--[folder].[ext]'
  //         }
  //       },
  //       {
  //         test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
  //         use: {
  //           loader: 'url-loader',
  //           query: {
  //             limit: 10000,
  //             name: 'fonts/[name]--[folder].[ext]'
  //           }
  //         }
  //       }
  //     ]
  //   }
  // },

  chainWebpack: config => {
    config
      .plugin('html')
      .tap(options => {
        if (options[0].minify) {
          options[0].minify.minifyCSS = true
        }
        return options
      })

    config.module
      .rule('images')
      .test(/\.(png|jpe?g|gif|webp|svg)(\?.*)?$/)
      .use('url-loader')
      .tap(options => {
        options.limit = 10000
        return options
      })

    const svgRule = config.module.rule('svg')
    svgRule.uses.clear()
    // svgRule.
    //   use('url-loader')
    // config.module
    //   .rule('svg')
    //   .use('url-loader')
    //   .loader('url-loader')

    // config.module
    //   .rule('gzip')
    //   .test(/\.gz$/)
    //   .use('gzip-loader')
    //   .loader('gzip-loader')
    //   .end()

    // config.module
    //   .rule('txt')
    //   .test(/\.txt$/)
    //   .use('@/loaders/txtLoader')
    //   .loader('@/loaders/txtLoader')
    //   .end()
  },

  productionSourceMap: false,

  /* A directory (relative to outputDir) to nest generated static
   * assets (js, css, img, fonts) under. */
  assetsDir: 'static'
}
