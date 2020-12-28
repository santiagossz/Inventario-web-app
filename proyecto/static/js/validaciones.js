//Función para validar inicio sesión
const validarUsuario = () => {
    const correo = document.getElementById("correo");
    const contrasena = document.getElementById("contrasena");

    const correoRe = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    const contrasenaRe = /((?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,})/;

    if (correoRe.test(correo.value) === false) {
        alert("Ingrese un correo válido");
        correo.value = "";
        contrasena.value = "";
        return false;

    } else if (contrasenaRe.test(contrasena.value) === false) {
        alert("La contraseña debe contener mínimo 8 carateres, una mayúscula, una minúscula y un número");
        contrasena.value = "";
        return false;

    } else {
        return true;
    }
};

//Función para validar recuperar contraseña

const validarRecuperar = () => {
    const correo = document.getElementById("correoRecuperar");

    const correoRe = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;

    if (correoRe.test(correo.value) === false) {
        alert("Ingrese un correo válido");
        correo.value = "";
        return false;

    } else {
        alert("Correo de recuperación de contraseña enviado a: " + correo.value);
        return true;
    }
};

//Función para validar registro usuario
const validarRegistro = () => {

    const usuario = document.getElementById("nombre");
    const correo = document.getElementById("correo");
    const contrasena1 = document.getElementById("contrasena");
    const contrasena2 = document.getElementById("contrasena2");

    const correoRe = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    const contrasenaRe = /((?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,})/;

    if (usuario.value.length < 6 && correoRe.test(correo.value) === false) {
        alert("Nombre de usuario debe contener mínimo 6 caracteres");
        usuario.value = "";
        correo.value = "";
        contrasena1.value = "";
        contrasena2.value = "";
        return false;

    } else if (usuario.value.length < 6) {
        alert("Nombre de usuario debe contener mínimo 6 caracteres");
        usuario.value = "";
        contrasena1.value = "";
        contrasena2.value = "";
        return false;

    } else if (correoRe.test(correo.value) === false) {
        alert("Ingrese un correo válido");
        correo.value = "";
        contrasena1.value = "";
        contrasena2.value = "";
        return false;

    } else if (contrasenaRe.test(contrasena1.value) === false) {
        alert("La contraseña debe contener mínimo 8 carateres, una mayúscula, una minúscula y un número");
        contrasena1.value = "";
        contrasena2.value = "";
        return false;

    } else if (contrasena2.value !== contrasena1.value) {
        alert("Contraseñas no coinciden");
        contrasena1.value = "";
        contrasena2.value = "";
        return false;

    } else {
        alert("Usuario " + usuario.value + " fue registrado satisfactoriamente\nCorreo con datos de verificación enviado a: " + correo.value);
        return true;
    }
};

//Función para Validar Producto Creador
const crearProducto = () => {
    nombre=document.getElementById('usuario').value
    alert(nombre +' fue creado satisfactoriamente');
};


//Funciones para mostrar contraseña
const lock = (elemento) => {
    elemento.classList.toggle("fa-unlock");
    const contrasena = document.getElementById("contrasena");
    contrasena.getAttribute("type") === "password"
        ? contrasena.setAttribute("type", "text")
        : contrasena.setAttribute("type", "password");
};

const lock1 = (elemento) => {
    elemento.classList.toggle("fa-unlock");
    const contrasena = document.getElementById("contrasena2");
    contrasena.getAttribute("type") === "password"
        ? contrasena.setAttribute("type", "text")
        : contrasena.setAttribute("type", "password");
};

//Función para mostrar info de la imagen en el boton de escoger imagen
const infoImagen = (elemento) => {
    nombreRuta = elemento.value;
    nombreImagen = nombreRuta.substr(nombreRuta.indexOf("h") + 2)
    document.getElementById("escogerImagen-label").innerHTML = nombreImagen
}


// Omitir el mensaje de Confirm FOrm Resubmission... validar este punto
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}

