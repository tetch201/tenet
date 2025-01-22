const localtunnel = require('localtunnel');
const readline = require('readline');
const { spawn } = require('child_process');

function printBanner() {
    const banner = `
_____                 _____ 
__  /___________________  /_
_  __/  _ \\_  __ \\  _ \\  __/
/ /_ /  __// / / /  __/ /_  
\\__/ \\___//_/ /_/\\___/\\__/ \n`;
    console.log(banner);
}

printBanner();

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const startServer = async (port) => {
    try {
        let tunnel = await localtunnel({ port: port });
        let wsTunnel = tunnel.url.replace('https://', 'ws://');
        console.log(`Туннель запущен на ${wsTunnel}`);

        // const serverProcess = await spawn('server.exe', [port], { stdio: 'inherit' });
        const serverProcess = await spawn('python', ['server.py', port], { stdio: 'inherit' });

        serverProcess.on('close', (code) => {
            console.log(`Сервер завершил работу с кодом ${code}`);
            tunnel.close();
        });

        tunnel.on('close', () => {
            console.log('Туннель закрыт.');
            serverProcess.kill();
        });

        tunnel.on('error', (err) => {
            console.error('Ошибка туннеля: ', err);
            serverProcess.kill();
        });

        // spawn('client.exe', [wsTunnel], {stdio: 'inherit'});
        spawn('python', ['client.py', wsTunnel], {stdio: 'inherit'});
    } catch (err) {
        console.error('Ошибка при создании туннеля: ', err);
    }
};

const connectToServer = () => {
    // const clientProcess = spawn('client.exe', { stdio: 'inherit' });
    const clientProcess = spawn('python', ['client.py'], { stdio: 'inherit' });

    clientProcess.on('close', (code) => {
        console.log(`Клиент завершил работу с кодом ${code}`);
    });
};

const mainMenu = () => {
    console.log('Выберите действие:');
    console.log('1. Создать сервер');
    console.log('2. Подключиться к серверу');

    rl.question('Введите номер действия: ', (choice) => {
        if (choice === '1') {
            rl.question('Введите порт для создания туннеля: ', (port) => {
                startServer(port);
                rl.close();
            });
        } else if (choice === '2') {
            connectToServer();
            rl.close();
        } else {
            console.log('Неверный выбор. Пожалуйста, попробуйте снова.');
            mainMenu();
        }
    });
};

mainMenu();