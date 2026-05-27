from flask import Flask, request, jsonify
from config import db, ma, Config
from models import Usuario, Producto, Categoria, Pedido, DetallePedido

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
ma.init_app(app)

# --- Schemas con Marshmallow ---
class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

# --- Endpoints ---
@app.route("/usuarios", methods=["GET"])
def get_usuarios():
    usuarios = Usuario.query.all()
    return usuarios_schema.jsonify(usuarios)

@app.route("/usuarios/<int:id>", methods=["GET"])
def get_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return usuario_schema.jsonify(usuario)

@app.route("/usuarios", methods=["POST"])
def add_usuario():
    data = request.json
    nuevo = Usuario(
        nombre=data["nombre"],
        correo=data["correo"],
        contrasena=data["contrasena"],
        tipo=data.get("tipo", "Cliente"),
        estatus=data.get("estatus", True)
    )
    db.session.add(nuevo)
    db.session.commit()
    return usuario_schema.jsonify(nuevo), 201

@app.route("/usuarios/<int:id>", methods=["PUT"])
def update_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    data = request.json
    usuario.nombre = data.get("nombre", usuario.nombre)
    usuario.correo = data.get("correo", usuario.correo)
    usuario.contrasena = data.get("contrasena", usuario.contrasena)
    usuario.tipo = data.get("tipo", usuario.tipo)
    usuario.estatus = data.get("estatus", usuario.estatus)
    db.session.commit()
    return usuario_schema.jsonify(usuario)

@app.route("/usuarios/<int:id>", methods=["DELETE"])
def delete_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado"}), 200

if __name__ == "__main__":
    app.run(debug=True)
