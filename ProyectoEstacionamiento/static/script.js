let patenteSeleccionada = null;
let horaIngresoSeleccionada = null;

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

document.getElementById('actualizarBtn').addEventListener('click', function() {
    const patenteNueva = document.getElementById('patenteInput').value.trim();

    if (!patenteSeleccionada) {
        alert('Seleccione un registro para actualizar.');
        return;
    }

    fetch('http://127.0.0.1:5000/actualizar', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            patenteOriginal: patenteSeleccionada,
            patenteNueva: patenteNueva
        })
    })
    .then(response => response.json())
    .then(data => {
        listarPatentes();
        resetSeleccion();
    });
});

document.getElementById('eliminarBtn').addEventListener('click', function() {
    if (!patenteSeleccionada) {
        alert('Seleccione un registro para eliminar.');
        return;
    }

    fetch('http://127.0.0.1:5000/eliminar', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            patente: patenteSeleccionada
        })
    })
    .then(response => response.json())
    .then(data => {
        listarPatentes();
        resetSeleccion();
    });
});

document.getElementById('cobroBtn').addEventListener('click', function() {
    if (!patenteSeleccionada || !horaIngresoSeleccionada) {
        alert('Seleccione un registro para cobrar.');
        return;
    }

    const precioPorHora = parseFloat(document.getElementById('precioHoraInput').value);
    const ahora = new Date();
    const horaIngreso = new Date(horaIngresoSeleccionada);

    const diffMs = ahora - horaIngreso;
    const diffHoras = Math.ceil(diffMs / (1000 * 60 * 60));

    const total = diffHoras * precioPorHora;

    alert(`Cobro total para patente "${patenteSeleccionada}": $${total} (${diffHoras} hora(s))`);
});

// Verificación automática del estado del servidor
function verificarEstadoServidor() {
    fetch('http://127.0.0.1:5000/listar')
    .then(response => {
        if (response.ok) {
            document.getElementById('estadoServidor').textContent = 'Online';
            document.getElementById('puntoEstado').className = 'online';
        } else {
            document.getElementById('estadoServidor').textContent = 'Offline';
            document.getElementById('puntoEstado').className = 'offline';
        }
    })
    .catch(() => {
        document.getElementById('estadoServidor').textContent = 'Offline';
        document.getElementById('puntoEstado').className = 'offline';
    });
}

// Iniciar verificación cada 3 segundos
setInterval(verificarEstadoServidor, 3000);

// Ejecutar verificación al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    listarPatentes();
    actualizarTimer();
    setInterval(actualizarTimer, 1000);
    verificarEstadoServidor();
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

            fila.addEventListener('click', function() {
                // Quitar selección anterior
                document.querySelectorAll('#tablaPatentes tbody tr').forEach(row => row.classList.remove('selected'));
                fila.classList.add('selected');

                // Guardar valores seleccionados
                patenteSeleccionada = registro.patente;
                horaIngresoSeleccionada = registro.horaIngreso;

                // Rellenar input patente
                document.getElementById('patenteInput').value = patenteSeleccionada;

                // Habilitar botones
                document.getElementById('actualizarBtn').disabled = false;
                document.getElementById('eliminarBtn').disabled = false;
                document.getElementById('cobroBtn').disabled = false;
            });

            tablaBody.appendChild(fila);
        });
    });
}

function resetSeleccion() {
    patenteSeleccionada = null;
    horaIngresoSeleccionada = null;
    document.getElementById('patenteInput').value = '';
    document.getElementById('actualizarBtn').disabled = true;
    document.getElementById('eliminarBtn').disabled = true;
    document.getElementById('cobroBtn').disabled = true;

    // Quitar selección visual
    document.querySelectorAll('#tablaPatentes tbody tr').forEach(row => row.classList.remove('selected'));
}
