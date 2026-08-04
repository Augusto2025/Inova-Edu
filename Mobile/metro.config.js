const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');

module.exports = (async () => {
  const projectRoot = __dirname;
  const config = await getDefaultConfig(projectRoot);

  // Restrict watch folders to the Mobile project only (avoid parent node_modules)
  config.watchFolders = [path.resolve(projectRoot)];

  // Make sure resolver looks for node_modules inside Mobile only
  config.resolver = config.resolver || {};
  config.resolver.nodeModulesPaths = [path.resolve(projectRoot, 'node_modules')];

  return config;
})();
