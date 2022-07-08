// Se obtiene el elemento form del html
const form = document.getElementById("form");

form.addEventListener("submit", (e) => {

  // Se obtienen todos los valores de los inputs que interesan validar
  const nombre = document.getElementById("nombre").value;
  const desarrollador = document.getElementById("desarrollador").value;
  const imagen = document.getElementById("imagen").value;
  const precio = document.getElementById("precio").value;
  const descuento = document.getElementById("descuento").value;
  const calificacion = document.getElementById("calificacion").value;
  
  // Elemento div vacío con id "error" donde se cargarán los mensajes
  const error = document.getElementById("error");
  
  // Lista de mensajes que inicia vacía y se va llenando a medida que se encuentra un error
  const MENSAJES = [];
  error.innerText = "";
  if (!isValid(nombre)) {
    MENSAJES.push("*Por favor, introduzca un nombre válido");
  }

  if (!isValid(desarrollador)) {
    MENSAJES.push("*Por favor, introduzca un desarrollador válido");
  }

  if(!isValid(imagen)) {
    if(document.querySelector(".img-thumbnail")) {
      let imgSrc = document.querySelector(".img-thumbnail").src
      if(!imgSrc) {
        MENSAJES.push("*El archivo imagen no puede ser nulo");
      }
  } else {
    MENSAJES.push("*El archivo imagen no puede ser nulo")
  }
}

if(isValid(imagen) && (imagen.slice(-4) !== '.jpg' && imagen.slice(-4) !== '.png')) {
  MENSAJES.push("*El archivo imagen debe tener extension .jpg o .png");
}

  if (!isValid(precio) || precio < 0 || !Number(precio)) {
    MENSAJES.push("*Por favor incluya un precio válido");
  }

if (descuento < 0 || descuento > 100 || (!Number(descuento) && (isValid(descuento)) && descuento != 0)) {
      MENSAJES.push("*El valor del descuento debe ser entre 0 y 100 sin símbolos");
  }

  if (!isValid(calificacion) || calificacion < 0 || calificacion > 100) {
    MENSAJES.push("*La calificación debe ser entre 0 y 100 y no debe ser nula");
  }

  // Si la lista de mensajes tiene al menos un elemento, se ejecuta lo siguiente, caso contrario, se envía el formulario
  if (MENSAJES.length > 0) {
    e.preventDefault();
    // Se cargan todos los errores de la lista de mensajes en el elemento div unidos por "\n" que es un quiebre de linea
    error.innerText = MENSAJES.join("\n");
  }
});

// Esta funcion comprueba que los inputs no se envíen en blanco/nulos
function isValid(element) {
    return element !== '' && element !== null;
}