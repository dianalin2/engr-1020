const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  openFile: () => ipcRenderer.invoke('dialog:openFile')
})

ipcRenderer.on('asynchronous-reply', (_event, arg) => {
    console.log(arg) // prints "pong" in the DevTools console
  })
ipcRenderer.send('asynchronous-message', 'ping')