const webpack = require('webpack');

module.exports = function override(config, env) {
  // Add fallback for Node.js core modules
  config.resolve.fallback = {
    url: require.resolve('url'),
    assert: require.resolve('assert'),
    buffer: require.resolve('buffer'),
    stream: require.resolve('stream-browserify'),
    crypto: require.resolve('crypto-browserify'),
  };

  // Add polyfills
  config.plugins.push(
    new webpack.ProvidePlugin({
      process: 'process/browser',
      Buffer: ['buffer', 'Buffer'],
    })
  );

  return config;
};