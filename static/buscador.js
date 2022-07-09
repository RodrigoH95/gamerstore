const buscador = document.getElementById("buscador");
const tablaLista = document.getElementById("tabla-lista");

function buscar() {
    filtro = buscador.value.toUpperCase();
    filas = tablaLista.querySelectorAll("tr");

    for(let i = 0; i < filas.length; i ++) {
        nombre = filas[i].getElementsByTagName("td")[1];
        if(nombre) {
            valor = nombre.textContent || nombre.innerText;
            if(valor.toUpperCase().indexOf(filtro) > -1) {
                filas[i].style.display = "";
            } else {
                filas[i].style.display = "none";
            }
        }
    }
}

