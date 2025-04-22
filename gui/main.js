const { app, BrowserWindow, shell, dialog, ipcMain } = require('electron')
const path = require('node:path')
const { spawn } = require('child_process');
const fs = require('fs');

require('dotenv').config({ path: path.join(__dirname, '../.env') });

const PYTHON_PATH = process.env.PYTHON_PATH ?? 'py';

app.whenReady().then(() => {
  const win = new BrowserWindow({
    width: 800,
    height: 600,

    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  })

  win.loadFile('index.html')

  async function handleGenerateModel(event,) {
    const child = spawn(PYTHON_PATH, ['../collate_open_sysml.py'],);

    return new Promise((resolve, reject) => {
      child.stdout.on('data', (data) => {
        data = data.toString().trim();
        // resolve with model name
        resolve(data);
      });

      child.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
        reject(data.toString());
      });
    });
  }

  async function handleGenerateSysML(event, modelIds = []) {
    const child = spawn(PYTHON_PATH, ['../generate_push_sysml.py', JSON.stringify(modelIds)],);

    let data = '';

    return new Promise((resolve, reject) => {
      child.stdout.on('close', () => {
        resolve();
      });

      child.stdout.on('data', (currData) => {
        currData = currData.toString().trim();
        if (currData.startsWith('Loading')) {
          console.log('Loading model...');
          return;
        }

        data += currData;

        try {
          data = JSON.parse(data);
          if (!data)
            return;
        } catch (e) {
          console.error('Error parsing JSON:', data);
          return;
        }

        win.webContents.send('model:generateSysML', data['id'], data['model']);

        data = '';
      });

      child.stderr.on('data', (data) => {
        data = data.toString().trim();
        if (data.startsWith('Loading') || data.startsWith('Device set to') || data.startsWith('Setting'))
          return;

        reject(data);
      });
    });
  }

  async function handleOpenModel(event, modelName) {
    fs.mkdirSync(path.join(__dirname, '../models', modelName), { recursive: true });
    const data = fs.readFileSync(`../models/${modelName}/models.sysml`, 'utf8');

    shell.openExternal("http://localhost:8080");

    return data;
  }

  async function handleGetDashboard(event) {
    const child = spawn(PYTHON_PATH, ['../get_dashboard.py'], { shell: true });

    return new Promise((resolve, reject) => {
      const allData = [];

      child.stdout.on('data', (data) => {
        data = data.toString().trim();
        if (data)
          allData.push(data);
      });

      child.stdout.on('close', () => {
        const result = allData.join('');
        resolve(JSON.parse(result));
      });


      child.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
        reject(data.toString());
      });
    });
  }

  async function handleModifyAsset(event, assetId, newModel) {
    const child = spawn(PYTHON_PATH, ['../modify_asset.py', assetId, newModel]);

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

  async function getAllModels() {
    const files = fs.readdirSync('../models');
    return files;
  }

  async function handleFileOpen(event) {
    const { canceled, filePaths } = await dialog.showOpenDialog({})
    if (!canceled) {
      console.log(filePaths[0])
      const child = spawn(PYTHON_PATH, ['../push_file_to_db.py', filePaths[0]],);
      child.stdout.pipe(process.stdout)
      child.stderr.pipe(process.stderr)

      child.on('close', (code) => {
        console.log(`Child process exited with code ${code}`);
        win.webContents.send('file:open', filePaths[0]);
      });
    }
  }


  ipcMain.handle('dialog:openFile', handleFileOpen)
  ipcMain.handle('model:getAllModels', getAllModels)
  ipcMain.handle('model:generate', handleGenerateModel)
  ipcMain.handle('dialog:openModel', handleOpenModel)
  ipcMain.handle('dashboard:get', handleGetDashboard)
  ipcMain.handle('model:modifyAsset', handleModifyAsset)
  ipcMain.handle('model:generateSysML', handleGenerateSysML)

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})
