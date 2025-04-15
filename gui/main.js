
const { app, BrowserWindow, shell, dialog, ipcMain } = require('electron')
const path = require('node:path')
const { spawn } = require('child_process');
const fs = require('fs');

async function handleGenerateModel(event, path) {
  const child = spawn('py', ['../collate_open_sysml.py', path],);

  return new Promise((resolve, reject) => {
    child.stdout.on('data', (data) => {
      resolve(data.toString());
    });

    child.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
      reject(data.toString());
    });
  });
}

async function handleOpenModel(event, modelName) {
  const data = fs.readFileSync(`../models/${modelName}/models.sysml`, 'utf8');

  shell.openExternal("http://localhost:8080");

  return data;
}

async function getAllModels() {
  const files = fs.readdirSync('../models');
  return files;
}

async function handleFileOpen() {
  const { canceled, filePaths } = await dialog.showOpenDialog({})
  if (!canceled) {
    console.log(filePaths[0])
    const child = spawn('py', ['../push_file_to_db.py', filePaths[0]],);
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
  ipcMain.handle('model:getAllModels', getAllModels)
  ipcMain.handle('model:generate', handleGenerateModel)
  ipcMain.handle('dialog:openModel', handleOpenModel)
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
