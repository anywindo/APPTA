const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  setActiveApp: (appType) => ipcRenderer.invoke('set-active-app', appType),
  switchApp: (appType) => ipcRenderer.invoke('set-active-app', appType),
  restartBackend: (appType) => ipcRenderer.invoke('restart-backend', appType),
  openExternal: (url) => ipcRenderer.invoke('open-external', url),
  getState: () => ipcRenderer.invoke('get-state'),
  onBackendStatus: (callback) => {
    const handler = (event, data) => callback(data);
    ipcRenderer.on('backend-status', handler);
    return () => ipcRenderer.removeListener('backend-status', handler);
  },
  onBackendLog: (callback) => {
    const handler = (event, data) => callback(data);
    ipcRenderer.on('backend-log', handler);
    return () => ipcRenderer.removeListener('backend-log', handler);
  },
  onInitialState: (callback) => {
    const handler = (event, data) => callback(data);
    ipcRenderer.on('initial-state', handler);
    return () => ipcRenderer.removeListener('initial-state', handler);
  },
  onSwitchTab: (callback) => {
    const handler = (event, data) => callback(data);
    ipcRenderer.on('switch-tab', handler);
    return () => ipcRenderer.removeListener('switch-tab', handler);
  }
});
