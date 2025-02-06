const { app, BrowserWindow, Menu } = require('electron');


function createWindow () {
  //Ventana principal
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true
    }
  });
  //Cargar HTML principal
  mainWindow.loadFile('index.html');

  // Crear un template para el menú
  const menuTemplate = [
    {
      label: 'Settings',
      submenu: [
        {
          label: 'Source Camara',
          click: () => { console.log('Cambiar o la camara o ingresar url RTSP'); }
        }
      ]
    },
    {
        label: 'View',
        submenu: [
          {
            label: 'Force Reload',
            role: 'forceReload'
          }
        ]
    }
  ];
  Menu.setApplicationMenu

  // Construir el menú a partir del template
  const menu = Menu.buildFromTemplate(menuTemplate);
  // Asignar el menú a la aplicación (o puedes usar mainWindow.setMenu(menu) para un menú específico)
  Menu.setApplicationMenu(menu);
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
