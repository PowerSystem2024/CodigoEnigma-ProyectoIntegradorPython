let patenteSeleccionada = null;
let horaIngresoSeleccionada = null;
//Lista de patentes cobradas
let patentesCobradas = [];


document.addEventListener('DOMContentLoaded', function() {
    listarPatentes();
    actualizarTimer();
    setInterval(actualizarTimer, 1000);
    verificarEstadoServidor();
});

function actualizarTimer() {
    const ahora = new Date();
    const hora = ahora.toLocaleTimeString();
    document.getElementById('timer').textContent = `Hora actual: ${hora}`;
}

function getArgentinaISOString() {
    const ahora = new Date();
    const pad = n => n.toString().padStart(2, '0');
    const yyyy = ahora.getFullYear();
    const mm = pad(ahora.getMonth() + 1);
    const dd = pad(ahora.getDate());
    const hh = pad(ahora.getHours());
    const mi = pad(ahora.getMinutes());
    const ss = pad(ahora.getSeconds());
    return `${yyyy}-${mm}-${dd}T${hh}:${mi}:${ss}`;
}

document.getElementById('agregarBtn').addEventListener('click', function() {
    const patenteInput = document.getElementById('patenteInput');
    const precioInput  = document.getElementById('precioHoraInput');
    const errorDiv     = document.getElementById('errorPatente');
    const patente      = patenteInput.value.trim();
    const ahoraArgentina = getArgentinaISOString();

    // Limpiar mensaje de error previo
    errorDiv.style.display = 'none';
    errorDiv.textContent   = '';

    // Validación básica de patente vacía
    if (patente === '') {
        errorDiv.textContent = 'Por favor ingrese una patente válida.';
        errorDiv.style.display = 'block';
        return;
    }

    // Construir payload
    const payload = {
        patente: patente,
        hora_ingreso: ahoraArgentina,
        precio_hora: parseFloat(precioInput.value),
        hora_actualizacion: ahoraArgentina
    };

    fetch('http://127.0.0.1:5000/patentes/agregar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) {
            // Si el backend responde con error, lo parseamos y mostramos
            return response.json().then(err => {
                errorDiv.textContent = err.message || 'Error al agregar la patente.';
                errorDiv.style.display = 'block';
                throw new Error(err.message);
            });
        }
        return response.json();
    })
    .then(data => {
        // Éxito: ocultar error, refrescar lista y limpiar campos
        errorDiv.style.display = 'none';
        patenteInput.value = '';
        precioInput.value  = '';
        listarPatentes();
    })
    .catch(err => {
        console.error('Fetch error:', err);
    });
});


document.getElementById('actualizarBtn').addEventListener('click', function() {
    const patenteNueva = document.getElementById('patenteInput').value.trim();
    const precioHora = parseFloat(document.getElementById('precioHoraInput').value);

    if (!patenteSeleccionada) {
        alert('Seleccione un registro para actualizar.');
        return;
    }

    const ahoraArgentina = getArgentinaISOString();

    fetch('http://127.0.0.1:5000/patentes/actualizar', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            patenteOriginal: patenteSeleccionada,
            patenteNueva: patenteNueva,
            precio_hora: precioHora,
            hora_actualizacion: ahoraArgentina
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

    fetch('http://127.0.0.1:5000/patentes/eliminar', {
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

    if (confirm(`Cobro total para patente "${patenteSeleccionada}": $${total} (${diffHoras} hs)\n\n¿Marcar como cobrado?`)) {
        fetch('http://127.0.0.1:5000/patentes/cobrar', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ patente: patenteSeleccionada })
        })
        .then(response => response.json())
        .then(data => {
            patentesCobradas.push({ // guardar la patente cobrada
                patente: patenteSeleccionada,
                total: total
            });
            listarPatentes();
            mostrarPatentesCobradas(); // mostrar en la nueva sección
            
            resetSeleccion();
        });
    }
});

// Mostrar patentes cobradas en tabla
function mostrarPatentesCobradas() {
    const tbody = document.querySelector("#tablaCobradas tbody");
    tbody.innerHTML = "";

    patentesCobradas.forEach(entry => {
        const row = document.createElement("tr");

        const tdPatente = document.createElement("td");
        tdPatente.textContent = entry.patente;

        const tdTotal = document.createElement("td");
        tdTotal.textContent = `$${entry.total}`;

        row.appendChild(tdPatente);
        row.appendChild(tdTotal);

        tbody.appendChild(row);
    });
}




// Verificación automática del estado del servidor
function verificarEstadoServidor() {
    fetch('http://127.0.0.1:5000/patentes/activas')
    .then(response => {
        if (response.ok) {
            document.getElementById('estadoServidor').textContent = ' Online';
            document.getElementById('puntoEstado').className = 'online';
        } else {
            document.getElementById('estadoServidor').textContent = ' Offline';
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

function listarPatentes() {
    fetch('http://127.0.0.1:5000/patentes/activas')
    .then(response => response.json())
    .then(data => {
        const tablaBody = document.querySelector('#tablaPatentes tbody');
        tablaBody.innerHTML = '';
        data.forEach((registro, index) => {
            const horaIngreso = registro.hora_ingreso
                ? new Date(registro.hora_ingreso).toLocaleTimeString()
                : '';
            const horaActualizacion = registro.hora_actualizacion
                ? new Date(registro.hora_actualizacion).toLocaleTimeString()
                : '';
            const fila = document.createElement('tr');
            fila.innerHTML = `
                <td>${index + 1}</td>
                <td>${registro.patente}</td>
                <td>${horaIngreso}</td>
                <td>${registro.precio_hora ?? ''}</td>
                <td>${horaActualizacion}</td>
            `;

            fila.addEventListener('click', function() {
                // Quitar selección anterior
                document.querySelectorAll('#tablaPatentes tbody tr').forEach(row => row.classList.remove('selected'));
                fila.classList.add('selected');

                // Guardar valores seleccionados
                patenteSeleccionada = registro.patente;
                horaIngresoSeleccionada = registro.hora_ingreso;

                // Rellenar input patente
                document.getElementById('patenteInput').value = patenteSeleccionada;
                
                // Rellenar input precio_hora con el valor de la patente seleccionada
                document.getElementById('precioHoraInput').value = registro.precio_hora ?? '';

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