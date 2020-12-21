from wtforms import Form, SubmitField, StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import  DataRequired

class Contactenos(Form):
    nombre = StringField('Nombre', validators=[DataRequired(message='No dejar vacío, completar')])
    correo = EmailField('Correo', validators=[DataRequired(message='No dejar vacío, completar')])
    mensaje = StringField('Mensaje', validators=[DataRequired(message='No dejar vacío, completar')])
    password = PasswordField('Password', validators=[DataRequired()])
    enviar = SubmitField('Enviar Mensaje')

#
# API
# @app.route('/sesion15')
# def sesion15():
#     return jsonify(({"mensaje":"hola"}))
#
#
# @app.route('/productos')
# def getproductos():
#     return jsonify({{"productos":productos}})
#
# @app.route('/productos/<string:nombreproducto>')
# def getproducto(nombreproducto):
#     buscar=[producto for producto in productos if producto['nombre']==nombreproducto ]
#     if(len(buscar)>0):
#         return jsonify({'productos':buscar[0]})
#     return jsonify({'mensaje':'producto no encontrado'})


#productos.py
# productos = [
#     {"nombre": "Espresso ", "precio": 25000, "cantidad": 5},
#     {"nombre": "galletas", "precio": 45000, "cantidad": 3},
#     {"nombre": "Sandwich jamón queso", "precio": 35000, "cantidad": 7}
# ]

# tipo de imagenes permitidas
# tipo = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
#
#
# # verifica si la imagen es permitida
# def imagen_permitida(imagen):
#     return '.' in imagen and \
#            imagen.rsplit('.', 1)[1].lower() in tipo
# if img and imagen_permitida(img.filename):