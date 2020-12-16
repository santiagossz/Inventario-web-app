#tablas.py
import sqlite3

from proyecto import db,login_manager
from flask_login import UserMixin

#acceder al id del usuario
@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(id)

# Tablas en la base de datos
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Boolean)
    nombre = db.Column(db.VARCHAR(200))
    correo = db.Column(db.VARCHAR(200))
    contrasena = db.Column(db.VARCHAR(200))
    estado = db.Column(db.Boolean)


class Producto(db.Model):
    referencia = db.Column(db.VARCHAR, primary_key=True)
    nombre = db.Column(db.VARCHAR(200))
    cantidad = db.Column(db.Integer)
    valor = db.Column(db.Integer)
    imagen = db.Column(db.VARCHAR(200))


class Ventas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.Integer)
    referencia = db.Column(db.Integer)
    fecha = db.Column(db.VARCHAR(200))
    cantidad = db.Column(db.Integer)


# función para acceder a los datos del producto
def datos_producto():
    connection = sqlite3.connect("proyecto/database/cafeteria.db")
    cursor = connection.cursor()
    referencia = [referencia[0] for referencia in cursor.execute("SELECT referencia FROM producto")]
    nombre = [nombre[0] for nombre in cursor.execute("SELECT nombre FROM producto")]
    cantidad = [cantidad[0] for cantidad in cursor.execute("SELECT cantidad FROM producto")]
    valor = [valor[0] for valor in cursor.execute("SELECT valor FROM producto")]
    imagenes =[imagen[0] for imagen in cursor.execute("SELECT imagen FROM producto")]
    return referencia, nombre, cantidad, valor,imagenes


# función para acceder a los datos de inicio de sesión
def datos_acceso():
    connection = sqlite3.connect("proyecto/database/cafeteria.db")
    cursor = connection.cursor()
    correo = [correo[0] for correo in cursor.execute("SELECT correo FROM usuario")]
    contrasena = [contrasena[0] for contrasena in cursor.execute("SELECT contrasena FROM usuario")]
    return correo, contrasena