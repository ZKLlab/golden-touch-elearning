module.exports = {
  pages: {
    admin: {
      entry: 'src/pages/admin/main.js',
      template: 'public/admin.html',
      filename: 'admin.html'
    }
  },

  devServer: {
    proxy: {
      '/api':
        {
          target: 'http://localhost:5000',
          changeOrigin: true
        }
    }
  },

  publicPath: undefined,
  outputDir: undefined,
  assetsDir: undefined,
  runtimeCompiler: undefined,
  productionSourceMap: undefined,
  parallel: undefined,
  css: undefined
}