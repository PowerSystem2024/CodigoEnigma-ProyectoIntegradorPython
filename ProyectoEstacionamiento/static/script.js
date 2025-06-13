document.addEventListener('DOMContentLoaded', function() {
    listarPatentes();
    actualizarTimer();
    setInterval(actualizarTimer, 1000);
});

function actualizarTimer() {
    const ahora = new Date();
    const hora = ahora.toLocaleTimeString();
    document.getElementById('timer').textContent = `Hora actual: ${hora}`;
}

document.getElementById('agregarBtn').addEventListener('click', function() {
    const patente = document.getElementById('patenteInput').value.trim();
    const ahora = new Date();

    if (patente === '') {
        alert('Por favor ingrese una patente válida.');
        return;
    }

    fetch('http://127.0.0.1:5000/agregar', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            patente: patente,
            horaIngreso: ahora.toISOString()
        })
    })
    .then(response => response.json())
    .then(data => {
        listarPatentes();
        document.getElementById('patenteInput').value = '';
    });
});

document.getElementById('verificarServidorBtn').addEventListener('click', function() {
    fetch('http://127.0.0.1:5000/listar')
    .then(response => {
        if (response.ok) {
            document.getElementById('estadoServidor').textContent = 'Estado: ONLINE';
        } else {
            document.getElementById('estadoServidor').textContent = 'Estado: OFFLINE';
        }
    })
    .catch(() => {
        document.getElementById('estadoServidor').textContent = 'Estado: OFFLINE';
    });
});

function listarPatentes() {
    fetch('http://127.0.0.1:5000/listar')
    .then(response => response.json())
    .then(data => {
        const tablaBody = document.querySelector('#tablaPatentes tbody');
        tablaBody.innerHTML = '';
        data.forEach((registro, index) => {
            const fila = document.createElement('tr');
            fila.innerHTML = `
                <td>${index + 1}</td>
                <td>${registro.patente}</td>
                <td>${new Date(registro.horaIngreso).toLocaleTimeString()}</td>
            `;
            tablaBody.appendChild(fila);
        });
    });
}
