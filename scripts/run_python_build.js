const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const isWin = process.platform === 'win32';
const root = path.resolve(__dirname, '..');

let pythonExec = isWin ? 'python' : 'python3';
const venvWin = path.join(root, 'venv', 'Scripts', 'python.exe');
const venvUnix = path.join(root, 'venv', 'bin', 'python');

if (isWin && fs.existsSync(venvWin)) {
  pythonExec = venvWin;
} else if (!isWin && fs.existsSync(venvUnix)) {
  pythonExec = venvUnix;
}

const buildScript = path.join(root, 'scripts', 'build_backends.py');

console.log(`[Build Runner] Using Python interpreter: ${pythonExec}`);
const res = spawnSync(pythonExec, [buildScript], {
  cwd: root,
  stdio: 'inherit'
});

process.exit(res.status || 0);
