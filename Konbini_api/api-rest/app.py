from flask import Flask, request, jsonify
from config import db, ma, Config
from models import Usuario, Categoria, Producto, Pedido, DetallePedido,db
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS
from datetime import date

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "clav3"  
jwt = JWTManager(app)
app.config.from_object(Config)
db.init_app(app)
ma.init_app(app)
CORS(app)

# Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    usuario = Usuario.query.filter_by(correo=data["correo"]).first()
    if usuario and check_password_hash(usuario.contrasena, data["contrasena"]):
        token = create_access_token(identity={"id": usuario.id_Usuario, "tipo": usuario.tipo})
        return jsonify({
            "access_token": token,
            "id_Usuario": usuario.id_Usuario,
            "tipo": usuario.tipo
        })
    return jsonify({"error": "Credenciales inválidas"}), 401

# Ruta protegida
@app.route("/perfil", methods=["GET"])
@jwt_required()
def perfil():
    id_usuario = get_jwt_identity()
    usuario = Usuario.query.get(id_usuario)
    return jsonify({"nombre": usuario.nombre, "correo": usuario.correo})

# Registro de usuario
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    try:
        nuevo = Usuario(
            nombre=data["nombre"],
            correo=data["correo"],
            contrasena=generate_password_hash(data["contrasena"]),  # guarda encriptada
            tipo="Cliente",
            estatus=True
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({
            "message": "Usuario registrado correctamente",
            "id_Usuario": nuevo.id_Usuario
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# ------------------ SCHEMAS ------------------
class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True

class CategoriaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        load_instance = True

class ProductoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        load_instance = True

class PedidoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pedido
        load_instance = True

class DetallePedidoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DetallePedido
        load_instance = True

# Instancias de schemas
usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)
categoria_schema = CategoriaSchema()
categorias_schema = CategoriaSchema(many=True)
producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)
pedido_schema = PedidoSchema()
pedidos_schema = PedidoSchema(many=True)
detalle_schema = DetallePedidoSchema()
detalles_schema = DetallePedidoSchema(many=True)

# ------------------ ENDPOINTS ------------------
# Usuario
@app.route("/usuarios", methods=["GET"])
def get_usuarios():
    return usuarios_schema.jsonify(Usuario.query.all())

@app.route("/usuarios/<int:id>", methods=["GET"])
def get_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return usuario_schema.jsonify(usuario)

@app.route("/usuarios", methods=["POST"])
def create_usuario():
    data = request.get_json()
    try:
        nuevo = Usuario(
            nombre=data["nombre"],
            correo=data["correo"],
            contrasena=data["contrasena"],
            tipo=data.get("tipo", "Cliente"),
            estatus=data.get("estatus", True)
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"message": "Usuario creado", "id": nuevo.id_Usuario}), 201
    except Exception as e:
        db.session.rollback()
        print("Error al crear usuario:", e)  
        return jsonify({"error": str(e)}), 500

@app.route("/usuarios/<int:id>", methods=["PUT"])
def update_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    for key, value in request.json.items():
        setattr(usuario, key, value)
    db.session.commit()
    return usuario_schema.jsonify(usuario)

@app.route("/usuarios/<int:id>", methods=["DELETE"])
def delete_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado"}), 200


# Categoría
@app.route("/categorias", methods=["GET"])
def get_categorias():
    return categorias_schema.jsonify(Categoria.query.all())

@app.route("/categorias/<int:id>", methods=["GET"])
def get_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    return categoria_schema.jsonify(categoria)

@app.route("/categorias", methods=["POST"])
def create_categoria():
    data = request.json
    nueva = Categoria(nombre=data["nombre"], estatus=data["estatus"])
    db.session.add(nueva)
    db.session.commit()
    return jsonify({
        "message": "Categoría creada",
        "id_Categoria": nueva.id_Categoria
    }), 201

@app.route("/categorias/<int:id>", methods=["PUT"])
def update_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    for key, value in request.json.items():
        setattr(categoria, key, value)
    db.session.commit()
    return categoria_schema.jsonify(categoria)

@app.route("/categorias/<int:id>", methods=["DELETE"])
def delete_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({"message": "Categoría eliminada"}), 200


# Producto
@app.route("/productos", methods=["GET"])
def get_productos():
    return productos_schema.jsonify(Producto.query.all())

@app.route("/productos/<int:id>", methods=["GET"])
def get_producto(id):
    producto = Producto.query.get_or_404(id)
    return producto_schema.jsonify(producto)

@app.route("/productos", methods=["POST"])
def add_producto():
    data = request.get_json()
    try:
        nuevo = Producto(
            nombre=data["nombre"],
            precio=data["precio"],
            existencias=data["existencias"],
            estatus=data.get("estatus", True),
            descripcion=data.get("descripcion", ""),
            id_Categoria=data["id_Categoria"] 
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"message": "Producto creado", "producto": {
            "id_Producto": nuevo.id_Producto,
            "nombre": nuevo.nombre,
            "precio": nuevo.precio,
            "existencias": nuevo.existencias,
            "estatus": nuevo.estatus,
            "descripcion": nuevo.descripcion,
            "id_Categoria": nuevo.id_Categoria
        }}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/productos/<int:id>", methods=["PUT"])
def update_producto(id):
    producto = Producto.query.get_or_404(id)
    for key, value in request.json.items():
        setattr(producto, key, value)
    db.session.commit()
    return producto_schema.jsonify(producto)

@app.route("/productos/<int:id>", methods=["DELETE"])
def delete_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return jsonify({"message": "Producto eliminado"}), 200


# Pedido
@app.route("/pedidos", methods=["GET"])
def get_pedidos():
    pedidos = Pedido.query.all()
    result = [
        {
            "id_Pedido": p.id_Pedido,
            "fecha": p.fecha.isoformat() if p.fecha else None,
            "direccion": p.direccion,
            "total": p.total,
            "estatus": p.estatus,
            "id_Usuario": p.id_Usuario
        } for p in pedidos
    ]
    return jsonify(result)

@app.route("/pedidos/<int:id>", methods=["GET"])
def get_pedido(id):
    p = Pedido.query.get_or_404(id)
    return jsonify({
        "id_Pedido": p.id_Pedido,
        "fecha": p.fecha.isoformat() if p.fecha else None,
        "direccion": p.direccion,
        "total": p.total,
        "estatus": p.estatus,
        "id_Usuario": p.id_Usuario
    })

@app.route("/pedidos", methods=["POST"])
def create_pedido():
    data = request.get_json()
    try:
        nuevo = Pedido(
            fecha=date.today(),
            direccion=data.get("direccion", ""),
            total=data.get("total", 0),
            estatus=data.get("estatus", 1),
            id_Usuario=data["id_Usuario"]
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"message": "Pedido creado", "id": nuevo.id_Pedido}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/pedidos/<int:id>", methods=["PUT"])
def update_pedido(id):
    p = Pedido.query.get_or_404(id)
    data = request.get_json()
    p.direccion = data.get("direccion", p.direccion)
    p.total = data.get("total", p.total)
    p.estatus = data.get("estatus", p.estatus)
    p.id_Usuario = data.get("id_Usuario", p.id_Usuario)
    db.session.commit()
    return jsonify({"message": "Pedido actualizado"})

@app.route("/pedidos/<int:id>", methods=["DELETE"])
def delete_pedido(id):
    p = Pedido.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "Pedido eliminado"})

#  Obtener o crear el pedido activo de un usuario
@app.route("/pedidos/activo/<int:id_usuario>", methods=["GET"])
def get_pedido_activo(id_usuario):
    pedido = Pedido.query.filter_by(id_Usuario=id_usuario, estatus=1).first()
    if not pedido:
        pedido = Pedido(
            fecha=date.today(),
            direccion="pendiente",
            total=0,
            estatus=1,
            id_Usuario=id_usuario
        )
        db.session.add(pedido)
        db.session.commit()
    return jsonify({
        "id_Pedido": pedido.id_Pedido,
        "fecha": str(pedido.fecha),
        "direccion": pedido.direccion,
        "total": pedido.total,
        "estatus": pedido.estatus,
        "id_Usuario": pedido.id_Usuario
    })


#  Confirmar pedido (cambiar estatus a 2)
@app.route("/pedidos/confirmar/<int:id_pedido>", methods=["PUT"])
def confirmar_pedido(id_pedido):
    pedido = Pedido.query.get_or_404(id_pedido)
    pedido.estatus = 2  # confirmado
    db.session.commit()

    # Crear nuevo pedido activo
    nuevo_pedido = Pedido(
        fecha=date.today(),
        direccion="pendiente",
        total=0,
        estatus=1,
        id_Usuario=pedido.id_Usuario
    )
    db.session.add(nuevo_pedido)
    db.session.commit()

    return jsonify({
        "message": "Pedido confirmado",
        "id_Pedido": pedido.id_Pedido,
        "nuevo_id_Pedido": nuevo_pedido.id_Pedido
    })



# DetallePedido
@app.route("/detalles", methods=["GET"])
def get_detalles():
    detalles = DetallePedido.query.all()
    result = [
        {
            "id_Detalle": d.id_Detalle,
            "precio": d.precio,
            "subtotal": d.subtotal,
            "cantidad": d.cantidad,
            "id_Producto": d.id_Producto,
            "id_Pedido": d.id_Pedido
        } for d in detalles
    ]
    return jsonify(result)

@app.route("/detalles/<int:id>", methods=["GET"])
def get_detalle(id):
    d = DetallePedido.query.get_or_404(id)
    return jsonify({
        "id_Detalle": d.id_Detalle,
        "precio": d.precio,
        "subtotal": d.subtotal,
        "cantidad": d.cantidad,
        "id_Producto": d.id_Producto,
        "id_Pedido": d.id_Pedido
    })

@app.route("/detalles", methods=["POST"])
def create_detalle():
    data = request.get_json()
    try:
        nuevo = DetallePedido(
            precio=data["precio"],
            cantidad=data["cantidad"],
            subtotal=data["precio"] * data["cantidad"],
            id_Producto=data["id_Producto"],
            id_Pedido=data["id_Pedido"]
        )
        db.session.add(nuevo)

        # actualizar total del pedido
        pedido = Pedido.query.get(nuevo.id_Pedido)
        pedido.total += nuevo.subtotal

        db.session.commit()
        return jsonify({"message": "Detalle creado", "id": nuevo.id_Detalle}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/detalles/<int:id>", methods=["PUT"])
def update_detalle(id):
    d = DetallePedido.query.get_or_404(id)
    data = request.get_json()
    d.precio = data.get("precio", d.precio)
    d.cantidad = data.get("cantidad", d.cantidad)
    d.subtotal = d.precio * d.cantidad
    d.id_Producto = data.get("id_Producto", d.id_Producto)

    # recalcular total del pedido
    pedido = Pedido.query.get(d.id_Pedido)
    pedido.total = sum(det.subtotal for det in DetallePedido.query.filter_by(id_Pedido=d.id_Pedido).all())

    db.session.commit()
    return jsonify({"message": "Detalle actualizado"})

@app.route("/detalles/<int:id>", methods=["DELETE"])
def delete_detalle(id):
    d = DetallePedido.query.get_or_404(id)
    pedido = Pedido.query.get(d.id_Pedido)
    pedido.total -= d.subtotal
    db.session.delete(d)
    db.session.commit()
    return jsonify({"message": "Detalle eliminado"})

@app.route("/detalles/pedido/<int:id_pedido>", methods=["GET"])
def get_detalles_by_pedido(id_pedido):
    detalles = DetallePedido.query.filter_by(id_Pedido=id_pedido).all()
    return jsonify([
        {
            "id_Detalle": d.id_Detalle,
            "precio": d.precio,
            "cantidad": d.cantidad,
            "subtotal": d.subtotal,
            "id_Producto": d.id_Producto,
            "id_Pedido": d.id_Pedido
        } for d in detalles
    ])

@app.route("/pedidos/<int:id_pedido>/detalles", methods=["POST"])
def add_detalle(id_pedido):
    data = request.get_json()
    pedido = Pedido.query.get_or_404(id_pedido)

    detalle = DetallePedido(
        precio=data["precio"],
        cantidad=data["cantidad"],
        subtotal=data["precio"] * data["cantidad"],
        id_Producto=data["id_Producto"],
        id_Pedido=id_pedido
    )
    db.session.add(detalle)

    # actualizar total
    pedido.total += detalle.subtotal
    db.session.commit()

    return jsonify({"message": "Detalle agregado", "id": detalle.id_Detalle}), 201

# ------------------ MAIN ------------------
if __name__ == "__main__":
    app.run(debug=True)
