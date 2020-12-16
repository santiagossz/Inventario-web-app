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
        const categoria = evento.target.innerHTML.toLowerCase();
        categoria === "todos"
            ? grid.filter("[data-categoria]")
            :   grid.filter((producto) => {
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


//Mostrar productos

const overlay = document.getElementById("overlay");
const imgs = document.querySelectorAll("#grid img")

imgs.forEach((elemento) => {
    const ruta = elemento.getAttribute("src");
    elemento.onclick = ((evento) => {
        overlay.classList.add("mostrar");
        overlay.querySelector("img").setAttribute("src", `${ruta}`);
    });
});
//cerrar con el boton
const cerrar = () => {
    overlay.classList.remove("mostrar")
};
//cerrar desde el overlay
// overlay.onclick = (evento) => {
// 	evento.target.id === "overlay" ? overlay.classList.remove("mostrar") :
// 		"";
// };


//alerta eliminar
const alertaEliminar = () => {
    alert("Producto de referencia # eliminado");
    overlay.classList.remove("mostrar");

};

// Omitir el mensaje de Confirm FOrm Resubmission... validar este punto
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}

//Jquery para mostrar las imagenes de la base de datos

// window.onload=(function() {
//     document.getElementById("img1").src='../SantiagoS-CV_1.pdf';
// });

