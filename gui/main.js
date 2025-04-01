
const { app, BrowserWindow, shell, dialog, ipcMain } = require('electron')
const path = require('node:path')
const { spawn } = require('child_process');

async function handleFileOpen () {
  const { canceled, filePaths } = await dialog.showOpenDialog({})
  if (!canceled) {
    console.log(filePaths[0])
    const child = spawn('py', ['../db.py', filePaths[0]],);
    child.stdout.pipe(process.stdout)
    child.stderr.pipe(process.stderr)

    return filePaths[0]
  }
}

const createWindow = () => {
  const win = new BrowserWindow({
    width: 800,
    height: 600,

    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  })

  win.loadFile('index.html')
}

app.whenReady().then(() => {
  ipcMain.handle('dialog:openFile', handleFileOpen)
  createWindow()
  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

ipcMain.on('asynchronous-message', (event, arg) => {
  console.log(arg) // prints "ping" in the Node console
  // works like `send`, but returning a message back
  // to the renderer that sent the original message
  event.reply('asynchronous-reply', 'pong')
})

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})