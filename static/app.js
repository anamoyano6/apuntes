document.addEventListener("DOMContentLoaded", () => {
    const personalist = document.getElementById("persona-list");
});

function cargarPersona(){
    fetch("/personas", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then(response => response.json())
    .then(data => {
        personalist.innerHTML = "";

        data.forEach(persona => {
            const personaDiv = document.createElement("div");
            personaDiv.innerHTML = `
            <strong>Nombre:</strong>${persona.nombre} <br>
            <strong>Apellido:</strong>${persona.apellido} <br>
            <strong>Email:</strong>${persona.email} <br>
            <strong>DNI:</strong>${persona.dni} <br>
            `;
            personalist.appendChild(personaDiv);
        });
    })
}
