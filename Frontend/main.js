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
  const menuTemplate = [ //https://www.electronjs.org/docs/latest/api/menu-item
    {
      label: 'Settings',
      submenu: [
        {
          label: 'Source Camara',
          click: () => { console.log('Cambiar o la camara o ingresar url RTSP'); }
        }
      ]
      /*
      La idea es poder configurar la direccion de la camara
      
      */
    },
    {
        label: 'View',
        submenu: [
          {
            label: 'Force Reload', // Forzar recarga de la ventana, útil para desarrollo por que no tengo que reiniciar la app
            role: 'forceReload'
          }
        ]
    }
  ];

  // Construir el menú a partir del template
  const menu = Menu.buildFromTemplate(menuTemplate);
  // Asignar el menú a la aplicación (o puedes usar mainWindow.setMenu(menu) para un menú específico)
  Menu.setApplicationMenu(menu);
}

app.whenReady().then(createWindow); //Cuando la app esté lista, crear la ventana

app.on('window-all-closed', () => { //Cerrar la app cuando todas las ventanas estén cerradas
  if (process.platform !== 'darwin') app.quit();
});