#  Importar las herramientas
# Acceder a las herramientas para crear la app web
from flask import Flask, request, jsonify

# Para manipular la DB
from flask_sqlalchemy import SQLAlchemy 

# Módulo cors es para que me permita acceder desde el frontend al backend
from flask_cors import CORS

# Crear la app
app = Flask(__name__)

# permita acceder desde el frontend al backend
CORS(app)


# Configurar a la app la DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://usuario:contraseña@localhost:3306/nombre_de_la_base_de_datos'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/usuariosgamers'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://com24167:codo2024@com24167.mysql.pythonanywhere-services.com/com24167$default'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Crear un objeto db, para informar a la app que se trabajará con sqlalchemy
db = SQLAlchemy(app)


# Definir la tabla 
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    nombre_usuario = db.Column(db.String(50))
    correo_electronico = db.Column(db.String(50))
    contraseña = db.Column(db.String(12))
    sexo=db.Column(db.String(50))
    pais=db.Column(db.String(50))
    imagen=db.Column(db.String(400))

    def __init__(self,nombre,apellido,nombre_usuario,correo_electronico,contraseña,sexo,pais,imagen):   #crea el  constructor de la clase
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.apellido=apellido
        self.nombre_usuario=nombre_usuario
        self.correo_electronico=correo_electronico
        self.contraseña=contraseña
        self.sexo=sexo
        self.pais=pais
        self.imagen=imagen

# 8. Crear la tabla al ejecutarse la app
with app.app_context():
    db.create_all()

# Crear ruta de acceso
# / es la ruta de inicio
@app.route("/")
def index():
    return f'App Web para registrar usuarios'

# Crear un registro en la tabla Usuarios
@app.route("/registro", methods=['POST']) 
def registro():
    # {"nombre": "Felipe", ...} -> input tiene el atributo name="nombre"
    nombre_recibido = request.json["nombre"]
    apellido=request.json['apellido']
    nombre_usuario=request.json['nombre_usuario']
    correo_electronico=request.json['correo_electronico']
    contraseña=request.json['contraseña']
    sexo=request.json['sexo']
    pais=request.json['pais']
    imagen=request.json['imagen']

    nuevo_registro = Usuario(nombre=nombre_recibido,apellido=apellido,nombre_usuario=nombre_usuario,correo_electronico=correo_electronico, contraseña=contraseña, sexo=sexo, pais=pais,imagen=imagen)
    db.session.add(nuevo_registro)
    db.session.commit()

    return "Solicitud de post recibida"
    

# Retornar todos los registros en un Json
@app.route("/usuarios",  methods=['GET'])
def usuarios():
    # Consultar en la tabla todos los usuarios
    # all_registros -> lista de objetos
    all_registros = Usuario.query.all()

    # Lista de diccionarios
    data_serializada = []
    
    for objeto in all_registros:
        data_serializada.append({"id":objeto.id, "nombre":objeto.nombre, "apellido":objeto.apellido, "nombre_usuario":objeto.nombre_usuario, "correo_electronico":objeto.correo_electronico, "contraseña":objeto.contraseña, "sexo":objeto.sexo, "pais":objeto.pais, "imagen":objeto.imagen})

    return jsonify(data_serializada)


# Modificar un registro
@app.route('/update/<id>', methods=['PUT'])
def update(id):
    # Buscar el registro a modificar en la tabla por su id
    usuario = Usuario.query.get(id)

    # {"nombre": "Felipe"} -> input tiene el atributo name="nombre"
    nombre = request.json["nombre"]
    apellido=request.json['apellido']
    nombre_usuario=request.json['nombre_usuario']
    correo_electronico=request.json['correo_electronico']
    contraseña=request.json['contraseña']
    sexo=request.json['sexo']
    pais=request.json['pais']
    imagen=request.json['imagen']

    usuario.nombre=nombre
    usuario.apellido=apellido
    usuario.nombre_usuario=nombre_usuario
    usuario.correo_electronico=correo_electronico
    usuario.contraseña=contraseña
    usuario.sexo=sexo
    usuario.pais=pais
    usuario.imagen=imagen
    db.session.commit()

    data_serializada = [{"id":usuario.id, "nombre":usuario.nombre, "apellido":usuario.apellido, "nombre_usuario":usuario.nombre_usuario, "correo_electronico":usuario.correo_electronico, "contraseña":usuario.contraseña, "sexo":usuario.sexo, "pais":usuario.pais, "imagen":usuario.imagen}]
    
    return jsonify(data_serializada)

   
@app.route('/borrar/<id>', methods=['DELETE'])
def borrar(id):
    
    # Se busca a la usuarios por id en la DB
    usuario = Usuario.query.get(id)

    # Se elimina de la DB
    db.session.delete(usuario)
    db.session.commit()

    data_serializada = [{"id":usuario.id, "nombre":usuario.nombre, "apellido":usuario.apellido, "nombre_usuario":usuario.nombre_usuario, "correo_electronico":usuario.correo_electronico, "contraseña":usuario.contraseña, "sexo":usuario.sexo, "pais":usuario.pais, "imagen":usuario.imagen}]

    return jsonify(data_serializada)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

