# app.py

from proyecto import app, db
from proyecto.tablas import Usuario, Producto, datos_producto, datos_acceso
import os,random,string
from flask import render_template, request, flash, redirect, url_for,session
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
                session['usuario']=correo
                next_url = request.form.get("next")
                if next_url == None or not next_url == "/":
                    next_url = url_for('productos')
                return redirect(next_url)

            elif correoacceso[i] == correo and check_password_hash(contrasenaacceso[i], contrasena):
                usuario = Usuario.query.filter_by(correo=correo).first()
                login_user(usuario)
                session['usuario']=correo
                session['nombre']=correo.split('@')[0]
                next_url = request.form.get("next")
                if next_url == None or not next_url == "/":
                    next_url = url_for('productosEmpleado',empleado=session['nombre'])
                return redirect(next_url)

        flash('Usuario y contraseña no coinciden', "errorIngresar")
        return render_template("inicio.html")
    return render_template("inicio.html")


# ruta recuperar contraseña
@app.route('/recuperar-contrasena', methods=['GET', 'POST'])
def recuperarContrasena():
    if request.method == 'POST' and "correoRecuperar" in request.form:
        nueva = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8)) + str(random.randint(0, 9))
        correo = request.form['correoRecuperar']
        contrasena_encriptada = generate_password_hash(nueva)
        usuario = Usuario.query.filter_by(correo=correo).first()
        usuario.contrasena = contrasena_encriptada
        db.session.add(usuario)
        db.session.commit()
        yag = yagmail.SMTP(user='inventario.lacafeteria@gmail.com', password='Grupof2020')
        yag.send(to=correo, subject='Recuperar contraseña', contents='<p>Estimado '+usuario.nombre+','+'</p>'
                                                                     '<h4>Su nueva contraseña es: '+ nueva +'</h4>'
                                                                     '<p> Para iniciar sesión haga click en el siguiente link:</p>'                                       
                                                                     '<p><a href="http://127.0.0.1:5000/">La Cafetería</a></p>')
        return redirect(url_for("inicio"))
    return render_template("recuperarContrasena.html")


# ruta para registrar nuevos usuarios
@app.route('/admin/registro', methods=['GET', 'POST'])
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
        yag.send(to=correo, subject='Nuevo Usuario', contents='<p>Estimado '+usuario.nombre+','+'</p>'
                                                              '<p>Felicitaciones. Su registro se ha compleado satisfactoriamente.</p> '
                                                              '<h4> Su nueva contraseña es: '+ request.form['contrasena']+'</h4>'
                                                              '<p> Para iniciar sesión haga click en el siguiente link:</p>'                                       
                                                              '<p><a href="http://127.0.0.1:5000/">La Cafetería</a></p>')
        return redirect(url_for("productos"))
    return render_template("registro.html")


# ruta página de productos de administrador
@app.route('/admin/inventario', methods=['GET', 'POST'])
@login_required
def productos():
    (referencia, nombre, cantidad, valor, imagenes) = datos_producto()

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
@app.route('/<string:empleado>/inventario', methods=['GET', 'POST'])
@login_required
def productosEmpleado(empleado):
    (referencia, nombre, cantidad, valor, imagenes) = datos_producto()
    return render_template('productosEmpleado.html', imagenes=imagenes, referencias=referencia, nombre=nombre,
                           cantidad=cantidad, valor=valor)


# ruta para crear productos
@app.route('/admin/crear-producto', methods=['GET', 'POST'])
@login_required
def crearProducto():

    if request.method == 'POST' and 'referencia' in request.form:
        img = request.files.get('imagen')
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


#ruta para actualizar productos
@app.route('/admin/actualizar-producto', methods=['GET', 'POST'])
@login_required
def actualizarProducto():
    referencia, nombre, cantidad, valor, imagenes = datos_producto()
    if request.method == 'POST' and 'imagenProd' in request.form:
        imagenActualizar = request.form['imagenProd']
        referenciaActualizar = request.form['referenciaProd']
        nombreActualizar = request.form['nombreProd']
        cantidadActualizar = request.form['cantidadProd']
        valorActualizar = request.form['valorProd']
        return render_template('actualizarProducto.html', imagenes=imagenes, referencias=referencia, nombre=nombre,
                               cantidad=cantidad, valor=valor, imagenActualizar=imagenActualizar,
                               referenciaActualizar=referenciaActualizar, nombreActualizar=nombreActualizar,
                               cantidadActualizar=cantidadActualizar, valorActualizar=valorActualizar)

    elif request.method == 'POST' and 'nombreActualizar' in request.form:
        producto = Producto.query.filter_by(referencia=request.form['referenciaActualizar']).first()
        producto.nombre=request.form['nombreActualizar']
        producto.cantidad=request.form['cantidadActualizar']
        producto.valor=request.form['precioActualizar']
        img = request.files.get('imagen')
        if not img.filename:
            ruta = request.form['noImagen']
        elif img.filename:
            filename = secure_filename(img.filename)
            img.save(os.path.join("proyecto/static/img", filename))
            ruta = '../static/img/' + filename;
        producto.imagen=ruta
        db.session.add(producto)
        db.session.commit()
        return redirect(url_for('productos'))

    elif request.method == 'POST' and 'eliminar' in request.form:
        referenciaEliminar = request.form['referenciaActualizar']
        Producto.query.filter_by(referencia=referenciaEliminar).delete()
        db.session.commit()
    return redirect(url_for('productos'))



@app.route('/<string:empleado>/ventas', methods=['GET', 'POST'])
@login_required
def ventas(empleado):
    referencia, nombre, cantidad, valor, imagenes = datos_producto()
    if request.method == 'POST' and 'imagenProd' in request.form:
        imagenVentas = request.form['imagenProd']
        referenciaVentas = request.form['referenciaProd']
        nombreVentas = request.form['nombreProd']
        cantidadVentas = request.form['cantidadProd']
        valorVentas = request.form['valorProd']

        return render_template('ventas.html', imagenes=imagenes, referencias=referencia, nombre=nombre,
                               cantidad=cantidad, valor=valor, imagenVentas=imagenVentas,
                               referenciaVentas=referenciaVentas, nombreVentas=nombreVentas,
                               cantidadVentas=cantidadVentas, valorVentas=valorVentas)

    elif request.method == 'POST' and 'referenciaVentas' in request.form:
        producto = Producto.query.filter_by(referencia=request.form['referenciaVentas']).first()
        producto.cantidad = producto.cantidad- int(request.form['ventas'])
        db.session.add(producto)
        db.session.commit()
        return redirect(url_for('productosEmpleado',empleado=session['nombre']))

    return redirect(url_for('productosEmpleado',empleado=session['nombre']))


# ruta para cerrar sesión
@app.route('/cerrar-sesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect(url_for("inicio"))

#restringir acceso de empleado a página de administrador
@app.before_request
def soloAdmin():
    if request.path.startswith('/admin'):
        if 'admin@admin.com' not in session['usuario']:
            return redirect(url_for('productosEmpleado',empleado=session['nombre']))



if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
