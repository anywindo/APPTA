const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const dirsToClean = [
  path.join(root, 'dist'),
  path.join(root, 'build')
];

for (const dir of dirsToClean) {
  if (fs.existsSync(dir)) {
    try {
      fs.rmSync(dir, { recursive: true, force: true, maxRetries: 3, retryDelay: 200 });
      console.log(`[Clean] Successfully cleaned ${path.basename(dir)} directory.`);
    } catch (err) {
      console.warn(`[Clean] Warning cleaning ${path.basename(dir)}:`, err.message);
    }
  }
}
