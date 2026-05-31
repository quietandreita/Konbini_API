from flask import Flask, request, jsonify
from config import db, ma, Config
from models import Usuario, Categoria, Producto, Pedido, DetallePedido
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
ma.init_app(app)
CORS(app)

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
def add_usuario():
    nuevo = Usuario(**request.json)
    db.session.add(nuevo)
    db.session.commit()
    return usuario_schema.jsonify(nuevo), 201

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
def add_categoria():
    nuevo = Categoria(**request.json)
    db.session.add(nuevo)
    db.session.commit()
    return categoria_schema.jsonify(nuevo), 201

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
    nuevo = Producto(**request.json)
    db.session.add(nuevo)
    db.session.commit()
    return producto_schema.jsonify(nuevo), 201

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
    return pedidos_schema.jsonify(Pedido.query.all())

@app.route("/pedidos/<int:id>", methods=["GET"])
def get_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    return pedido_schema.jsonify(pedido)

@app.route("/pedidos", methods=["POST"])
def add_pedido():
    nuevo = Pedido(**request.json)
    db.session.add(nuevo)
    db.session.commit()
    return pedido_schema.jsonify(nuevo), 201

@app.route("/pedidos/<int:id>", methods=["PUT"])
def update_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    for key, value in request.json.items():
        setattr(pedido, key, value)
    db.session.commit()
    return pedido_schema.jsonify(pedido)

@app.route("/pedidos/<int:id>", methods=["DELETE"])
def delete_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    db.session.delete(pedido)
    db.session.commit()
    return jsonify({"message": "Pedido eliminado"}), 200


# DetallePedido
@app.route("/detalles", methods=["GET"])
def get_detalles():
    return detalles_schema.jsonify(DetallePedido.query.all())

@app.route("/detalles/<int:id>", methods=["GET"])
def get_detalle(id):
    detalle = DetallePedido.query.get_or_404(id)
    return detalle_schema.jsonify(detalle)

@app.route("/detalles", methods=["POST"])
def add_detalle():
    nuevo = DetallePedido(**request.json)
    db.session.add(nuevo)
    db.session.commit()
    return detalle_schema.jsonify(nuevo), 201

@app.route("/detalles/<int:id>", methods=["PUT"])
def update_detalle(id):
    detalle = DetallePedido.query.get_or_404(id)
    for key, value in request.json.items():
        setattr(detalle, key, value)
    db.session.commit()
    return detalle_schema.jsonify(detalle)

@app.route("/detalles/<int:id>", methods=["DELETE"])
def delete_detalle(id):
    detalle = DetallePedido.query.get_or_404(id)
    db.session.delete(detalle)
    db.session.commit()
    return jsonify({"message": "Detalle eliminado"}), 200


# ------------------ MAIN ------------------
if __name__ == "__main__":
    app.run(debug=True)
