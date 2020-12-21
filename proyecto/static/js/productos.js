//Librería Muuri para trabjar con filtros
const grid = new Muuri(".grid", {
    layout: {
        rounding: false,
    },
});

// filtrar por categoría
const enlaces = document.querySelectorAll("#filtros a");
enlaces.forEach((boton) => {
    //cambiar color del boton al seleccionarse
    boton.onclick = (evento) => {
        evento.preventDefault();
        enlaces.forEach((boton) => {
            boton.classList.remove("bg-dark");
        });
        boton.classList.add("bg-dark");
        //filtrar
        const categoria = evento.target.id;
        categoria === "todos"
            ? grid.filter("[data-categoria]")
            : grid.filter((producto) => {
                return producto.getElement().dataset.categoria.includes(categoria);
            });
    };
});

//filtrar por barra de búsqueda
const filtrar = (elemento) => {
    const busqueda = elemento.value.toLowerCase();

    grid.filter((producto) => {
        return producto.getElement().dataset.etiquetas.includes(busqueda);
    });
};


//mostrar info de la imagen
const infoImagen = (elemento) => {
    nombreRuta = elemento.value;
    nombreImagen = nombreRuta.substr(nombreRuta.indexOf("h") + 2)
    document.getElementById("escogerImagen-label").innerHTML = nombreImagen
}

//verificar cantidades válidad para vender

const actualizarVentas = (nombre) =>{
    if(parseInt(document.getElementById('cantidadDisponibles').innerHTML)-
        parseInt(document.getElementById('ventas').value)>=0){
        alert('Cantidades vendidas de '+nombre+' fueron registradas satisfactoriamente')
        return true
    }
    else {
        alert('No hay suficiente disponibiliad de '+nombre )
        document.getElementById('ventas').value=""
        return false
    }
}



// Omitir el mensaje de Confirm FOrm Resubmission... validar este punto
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}

