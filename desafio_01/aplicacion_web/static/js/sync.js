
const socket = io();

let intervalo;

function iniciarSocket() {
    // Emitir cada 3 segundos (más estable)
    intervalo = setInterval(() => {
        socket.emit("mostrar_valor");
    }, 2000);
}

socket.on("connect", () => {
    console.log("[✔] Conectado al servidor");
    iniciarSocket();
});

socket.on("disconnect", () => {
    clearInterval(intervalo);
    console.log("[✘] Desconectado del servidor");
});

socket.on("muestra", function (data) {
    const nombre = data.nombre_muestra;
    const nombreSpan = document.getElementById("nombre_muestra");
    const img = document.querySelector('.container_photo img');

    nombreSpan.textContent = nombre;

    if (nombre !== "Desconocido") {
        img.src = `/static/muestras/${encodeURIComponent(nombre)}.jpg`;
    } else {
        img.src = "/static/img/default.jpg";
        document.getElementById("nombre_persona").textContent = "Esperando...";
        document.querySelector(".container_person img").src = "/static/img/default.jpg";
    }
});

socket.on("persona", function (data) {
    const campoNombre = document.querySelector('#nombre_muestra').textContent;
    const spanPersona = document.querySelector('#nombre_persona');

    if (data && data.data_persona && campoNombre !== "Desconocido") {
        const nom_per = data.data_persona[1];  // Asegurate que sea [1] el nombre
        spanPersona.textContent = nom_per;
    } else {
        spanPersona.textContent = "Esperando...";
    }
});


socket.on("img_pri", function (data) {
    const campoNombre = document.querySelector('#nombre_muestra').textContent;
    const img = document.querySelector('.container_person img');

    if (campoNombre !== "Desconocido" && data && data.data_img) {
        const nombre = data.data_img;
        img.src = `/static/muestras/${encodeURIComponent(nombre)}`;
    } else {
        img.src = "/static/img/default.jpg";
    }
});





