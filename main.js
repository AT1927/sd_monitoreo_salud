let token = '';

async function register() {
    const nombre = document.getElementById('nombre').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nombre, email, password })
    });

    const data = await response.json();
    alert(data.message);
}

async function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();
    if (data.access_token) {
        token = data.access_token;
        alert('Login exitoso');
        loadData();
    } else {
        alert(data.message);
    }
}

async function sendData() {
    const frecuencia_cardiaca = document.getElementById('frecuencia_cardiaca').value;
    const tension_arterial = document.getElementById('tension_arterial').value;
    const respiracion = document.getElementById('respiracion').value;

    const response = await fetch('/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ frecuencia_cardiaca, tension_arterial, respiracion })
    });

    const data = await response.json();
    alert(data.message);
    loadData();
}

async function loadData() {
    const response = await fetch('/data', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    const data = await response.json();
    const dataList = document.getElementById('data-list');
    dataList.innerHTML = data.map(item => `
                <div>
                    <p>Frecuencia Cardíaca: ${item.frecuencia_cardiaca}</p>
                    <p>Tensión Arterial: ${item.tension_arterial}</p>
                    <p>Respiración: ${item.respiracion}</p>
                    <p>Timestamp: ${item.timestamp}</p>
                </div>
            `).join('');
}