const {defineConfig} = require('@vue/cli-service')
//module.exports = {assetsDir: 'static',
// 静态文件的输出目录publicPath: './',outputDir: '../dist',
// dist 文件夹的输出目录devServer: {
// 该配置项解决请求 flask 后端接口时造成的跨域问题proxy: {'/api': {target: 'http://127.0.0.1:5000/api/',changeOrigin: true,
// true 表示实现跨域pathRewrite: {'^/api': '/'
// 这里理解成用‘/api’代替target里面的地址}}}}
module.exports = defineConfig({
    transpileDependencies: true,
    publicPath: './',
    outputDir: '../testkeeper/templates',
    assetsDir: 'static',
    devServer: {
        proxy: {
            '/':
                {
                    target: 'http://127.0.0.1:5000/',
                    changeOrigin: true,
                    pathRewrite:
                        {
                            '^/': '/'
                        }
                }
        }
    }

})
