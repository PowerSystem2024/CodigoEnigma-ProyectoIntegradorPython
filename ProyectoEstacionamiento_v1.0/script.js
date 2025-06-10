// Actualizar el timer cada segundo
function actualizarHora() {
    const timer = document.getElementById('timer');
    const ahora = new Date();
    const hora = ahora.toLocaleTimeString();
    timer.textContent = `Hora actual: ${hora}`;
}

setInterval(actualizarHora, 1000);
actualizarHora(); // llamada inicial

// Manejar el agregado de patentes a la tabla
let contador = 1;
let filaSeleccionada = null;

document.getElementById('agregarBtn').addEventListener('click', function() {
    const patenteInput = document.getElementById('patenteInput');
    const patente = patenteInput.value.trim();

    if (patente === '') {
        alert('Por favor ingrese una patente válida.');
        return;
    }

    const tablaBody = document.querySelector('#tablaPatentes tbody');
    const nuevaFila = document.createElement('tr');

    const celdaNumero = document.createElement('td');
    celdaNumero.textContent = contador++;

    const celdaPatente = document.createElement('td');
    celdaPatente.textContent = patente;

    const celdaHora = document.createElement('td');
    const ahora = new Date();
    celdaHora.textContent = ahora.toLocaleTimeString();

    nuevaFila.appendChild(celdaNumero);
    nuevaFila.appendChild(celdaPatente);
    nuevaFila.appendChild(celdaHora);

    // Guardar la hora real de ingreso en propiedad personalizada
    nuevaFila.dataset.horaIngreso = ahora.toISOString();

    // Hacer clic en la fila → seleccionar para actualizar / eliminar / cobrar
    nuevaFila.addEventListener('click', function() {
        seleccionarFila(this);
    });

    tablaBody.appendChild(nuevaFila);

    patenteInput.value = '';
    patenteInput.focus();
});

// Manejar la selección de fila
function seleccionarFila(fila) {
    // Desmarcar la fila anterior
    if (filaSeleccionada) {
        filaSeleccionada.classList.remove('selected');
    }

    filaSeleccionada = fila;
    filaSeleccionada.classList.add('selected');

    // Poner la patente en la casilla
    const patente = filaSeleccionada.cells[1].textContent;
    document.getElementById('patenteInput').value = patente;

    // Habilitar botones
    document.getElementById('actualizarBtn').disabled = false;
    document.getElementById('eliminarBtn').disabled = false;
    document.getElementById('cobroBtn').disabled = false;
}

// Manejar la actualización de la fila seleccionada
document.getElementById('actualizarBtn').addEventListener('click', function() {
    if (!filaSeleccionada) {
        alert('Seleccione una fila primero.');
        return;
    }

    const patenteInput = document.getElementById('patenteInput');
    const nuevaPatente = patenteInput.value.trim();

    if (nuevaPatente === '') {
        alert('Por favor ingrese una patente válida.');
        return;
    }

    // Actualizar la celda de patente
    filaSeleccionada.cells[1].textContent = nuevaPatente;

    // Limpiar selección
    limpiarSeleccion();
});

// Manejar eliminación (baja) de la fila seleccionada
document.getElementById('eliminarBtn').addEventListener('click', function() {
    if (!filaSeleccionada) {
        alert('Seleccione una fila primero.');
        return;
    }

    if (confirm('¿Está seguro que desea eliminar este registro?')) {
        filaSeleccionada.remove();
        limpiarSeleccion();
    }
});

// Manejar el cobro
document.getElementById('cobroBtn').addEventListener('click', function() {
    if (!filaSeleccionada) {
        alert('Seleccione una fila primero.');
        return;
    }

    const precioPorHora = parseFloat(document.getElementById('precioHoraInput').value);
    const horaIngresoStr = filaSeleccionada.dataset.horaIngreso;
    const horaIngreso = new Date(horaIngresoStr);
    const ahora = new Date();

    const diffMs = ahora - horaIngreso;
    const diffHoras = Math.ceil(diffMs / (1000 * 60 * 60)); // redondeo hacia arriba

    const total = precioPorHora * diffHoras;

    alert(`Cobro para la patente "${filaSeleccionada.cells[1].textContent}":\n\n` +
          `Horas a cobrar: ${diffHoras} hora(s)\n` +
          `Precio por hora: $${precioPorHora}\n` +
          `------------------------------\n` +
          `TOTAL: $${total}`);
});

// Función para limpiar selección
function limpiarSeleccion() {
    if (filaSeleccionada) {
        filaSeleccionada.classList.remove('selected');
    }
    filaSeleccionada = null;
    document.getElementById('patenteInput').value = '';
    document.getElementById('actualizarBtn').disabled = true;
    document.getElementById('eliminarBtn').disabled = true;
    document.getElementById('cobroBtn').disabled = true;
}
