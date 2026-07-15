#!/usr/bin/env node

const { execSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');

try {
  execSync('swift build -c release', { stdio: 'inherit', cwd: __dirname });

  fs.rmSync(path.join(__dirname, 'ExpoModulesMacros-tool'), { force: true });

  fs.copyFileSync(
    path.join(__dirname, '.build/arm64-apple-macosx/release/ExpoModulesMacros-tool'),
    path.join(__dirname, 'ExpoModulesMacros-tool')
  );

  execSync('strip ExpoModulesMacros-tool', { stdio: 'inherit', cwd: __dirname });
} catch (error) {
  console.error('Build failed:', error.message);
  process.exit(1);
}
