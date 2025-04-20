const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  openFile: () => ipcRenderer.invoke('dialog:openFile'),
  getAllModels: () => ipcRenderer.invoke('model:getAllModels'),
  generateModel: () => ipcRenderer.invoke('model:generate'),
  openModel: (path) => ipcRenderer.invoke('dialog:openModel', path),
  modifyAsset: (assetId, newModel) => ipcRenderer.invoke('model:modifyAsset', assetId, newModel),
  getDashboard: () => ipcRenderer.invoke('dashboard:get'),
  generateSysML: (modelIds) => ipcRenderer.invoke('model:generateSysML', modelIds),
  onSysMLGenerated: (callback) => ipcRenderer.on('model:generateSysML', (_event, modelId, model) => {
    console.log('Model generated:', modelId);
    callback(modelId, model);
  }),
})
