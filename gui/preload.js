const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  openFile: () => ipcRenderer.invoke('dialog:openFile'),
  getAllModels: () => ipcRenderer.invoke('model:getAllModels'),
  generateModel: (path) => ipcRenderer.invoke('model:generate', path),
  openModel: (path) => ipcRenderer.invoke('dialog:openModel', path),
})

ipcRenderer.on('asynchronous-reply', (_event, arg) => {
  console.log(arg) // prints "pong" in the DevTools console
})
ipcRenderer.send('asynchronous-message', 'ping')
