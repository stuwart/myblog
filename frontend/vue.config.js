module.exports = {  //跨域设置，将/api 的请求传送到8000端口
    devServer: {
        proxy: {
            '/api': {
                target: `http://127.0.0.1:8000/api`,
                changeOrigin: true,
                pathRewrite: {
                    '^/api': ''
                }
            }
        }
    }
};

