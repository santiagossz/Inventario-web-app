# app.py

from proyecto import app, db
from proyecto.tablas import Usuario, Producto,datos_producto, datos_acceso
import os
from flask import render_template, request, flash, redirect, url_for
import yagmail as yagmail
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash


# ruta inicio sesión
@app.route('/', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST' and 'correoInicio' in request.form:
        correo = request.form['correoInicio']
        contrasena = request.form['contrasena']
        correoacceso, contrasenaacceso = datos_acceso()

        for i in range(len(correoacceso)):
            if 'admin' in correo and correoacceso[i] == correo and check_password_hash(contrasenaacceso[i], contrasena):
                usuario = Usuario.query.filter_by(correo=correo).first()
                login_user(usuario)
                next_url = request.form.get("next")
                if next_url == None or not next_url == "/":
                    next_url = url_for('productos')
                return redirect(next_url)

            elif correoacceso[i] == correo and check_password_hash(contrasenaacceso[i], contrasena):
                usuario = Usuario.query.filter_by(correo=correo).first()
                login_user(usuario)
                next_url = request.form.get("next")
                if next_url == None or not next_url == "/":
                    next_url = url_for('productosEmpleado')
                return redirect(next_url)

        flash('Usuario y contraseña no coinciden', "errorIngresar")
        return render_template("inicio.html")
    return render_template("inicio.html")


# ruta recuperar contraseña
@app.route('/recuperar-contrasena', methods=['GET', 'POST'])
def recuperarContrasena():
    if request.method == 'POST' and "correoRecuperar" in request.form:
        correo = request.form['correoRecuperar']
        yag = yagmail.SMTP(user='inventario.lacafeteria@gmail.com', password='Grupof2020')
        yag.send(to=correo, subject='Recuperar contraseña', contents='<h4>Su nueva contraseña es HGFgd88c</h4>'
                                                                     '<p><a href="http://127.0.0.1:5000/">Iniciar Sesión</a></p>')
        return redirect(url_for("inicio"))
    return render_template("recuperarContrasena.html")


# ruta página de productos de administrador
@app.route('/administrador', methods=['GET', 'POST'])
@login_required
def productos():
    (referencia, nombre, cantidad, valor,imagenes) = datos_producto()

    # Eliminar producto
    if request.method == 'POST' and 'eliminar' in request.form:
        return render_template('productos.html', imagenes=imagenes, referencias=referencia, nombre=nombre,
                               cantidad=cantidad, valor=valor)
    # Ventas del producto por el empelado/ vueve a pag productos de empleado
    elif request.method == 'POST' and 'cantidades' in request.form:
        return render_template('productosEmpleado.html', imagenes=imagenes)

    return render_template('productos.html', imagenes=imagenes, referencias=referencia, nombre=nombre,
                           cantidad=cantidad, valor=valor)


# ruta página de productos de administrador
@app.route('/empleado', methods=['GET', 'POST'])
@login_required
def productosEmpleado():
    referencia, nombre, cantidad, valor,imagenes = datos_producto()
    return render_template('productosEmpleado.html', imagenes=imagenes, referencias=referencia, nombre=nombre,
                           cantidad=cantidad, valor=valor)




# ruta para crear productos
@app.route('/crear-producto', methods=['GET', 'POST'])
@login_required
def crearProducto():
    if request.method == 'POST' and 'referencia' in request.form:
        img = request.files['imagen']
        filename = secure_filename(img.filename)
        # guardar imagenes en la ruta static/img
        img.save(os.path.join("proyecto/static/img", filename))
        ruta = "../static/img/" + filename
        producto = Producto(referencia=request.form['referencia'], nombre=request.form['nombre'],
                            cantidad=request.form['cantidad'],
                            valor=request.form['valor'], imagen=ruta)
        db.session.add(producto)
        db.session.commit()
        return redirect(url_for("productos"))
    return render_template('crearProducto.html')


# ruta para registrar nuevos usuarios
@app.route('/registro', methods=['GET', 'POST'])
@login_required
def registro():
    if request.method == 'POST' and 'correoRegistro' in request.form:
        contrasena_encriptada = generate_password_hash(request.form['contrasena'])
        usuario = Usuario(tipo=False, nombre=request.form['nombre'], correo=request.form['correoRegistro'],
                          contrasena=contrasena_encriptada, estado=True)
        db.session.add(usuario)
        db.session.commit()
        correo = request.form['correoRegistro']
        yag = yagmail.SMTP(user='inventario.lacafeteria@gmail.com', password='Grupof2020')
        yag.send(to=correo, subject='Nuevo Usuario', contents='<h4>Usuario # creado satisfactoriamente</h4> '
                                                              '<p>Su contraseña es Gb444F2c</p>'
                                                              '<p><a href="http://127.0.0.1:5000/">Iniciar Sesión</a></p>')
        return redirect(url_for("productos"))
    return render_template("registro.html")


@app.route('/actualizar-producto', methods=['GET', 'POST'])
@login_required
def actualizarProducto():
    # referencia, nombre, cantidad, valor = visualizarDatos()
    # # for i in range(len(referencia)):
    # if request.method == 'POST':
    #     print(request.form['referenciaProd'][1])
    if request.method == 'POST' and 'actualizar' in request.form:
        redirect(url_for("productos"))
    return render_template('actualizarProducto.html')

# ruta para cerrar sesión
@app.route('/cerrar-sesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect(url_for("inicio"))


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)

# , referencias=referenciaActualizar, nombre=nombreActualizar,
#                            cantidad=cantidadActualizar, valor=valorActualizar

# referenciaActualizar = referencia[i]
# nombreActualizar = nombre[i]
# cantidadActualizar = cantidad[i]
# valorActualizar = valor[i]

#
# for i in range(len(referencia)):
#      if referencia[i] == request.form['referenciaProd']:
