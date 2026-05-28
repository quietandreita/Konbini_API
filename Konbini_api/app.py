from flask import Flask, request, jsonify
from config import db, ma, Config
from models import Usuario, Categoria, Producto, Pedido, DetallePedido

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
ma.init_app(app)

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

@app.route("/usuarios", methods=["POST"])
def add_usuario():
    nuevo = Usuario(**request.json)
    db.session.add(nuevo)
    db.session.commit()
    return usuario_schema.jsonify(nuevo), 201

# Categoría
@app.route("/categorias", methods=["GET"])
def get_categorias():
    return categorias_schema.jsonify(Categoria.query.all())

@app.route("/categorias", methods=["POST"])
def add_categoria():
    nuevo = Categoria(**request.json)
    db.session.add(nuevo)
    db.session.commit()
    return categoria_schema.jsonify(nuevo), 201

# Producto
@app.route("/productos", methods=["GET"])
def get_productos():
    return productos_schema.jsonify(Producto.query.all())

@app.route("/productos", methods=["POST"])
def add_producto():
    nuevo = Producto(**request.json)
    db.session.add(nuevo)
    db.session.commit()
    return producto_schema.jsonify(nuevo), 201

# Pedido
@app.route("/pedidos", methods=["GET"])
def get_pedidos():
    return pedidos_schema.jsonify(Pedido.query.all())

@app.route("/pedidos", methods=["POST"])
def add_pedido():
    nuevo = Pedido(**request.json)
    db.session.add(nuevo)
    db.session.commit()
    return pedido_schema.jsonify(nuevo), 201

# DetallePedido
@app.route("/detalles", methods=["GET"])
def get_detalles():
    return detalles_schema.jsonify(DetallePedido.query.all())

@app.route("/detalles", methods=["POST"])
def add_detalle():
    nuevo = DetallePedido(**request.json)
    db.session.add(nuevo)
    db.session.commit()
    return detalle_schema.jsonify(nuevo), 201

# ------------------ MAIN ------------------
if __name__ == "__main__":
    app.run(debug=True)
