from config import db

class Usuario(db.Model):
    __tablename__ = "Usuario"
    id_Usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40), unique=True, nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(256), nullable=False)
    tipo = db.Column(db.String(50), nullable=False, default="Cliente")
    estatus = db.Column(db.Boolean, default=True)

class Categoria(db.Model):
    __tablename__ = "Categoria"
    id_Categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), unique=True, nullable=False)
    estatus = db.Column(db.Boolean, default=True)

class Producto(db.Model):
    __tablename__ = "Producto"
    id_Producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), unique=True, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    existencias = db.Column(db.Integer, nullable=False)
    estatus = db.Column(db.Boolean, default=True)
    descripcion = db.Column(db.String(150))
    id_Categoria = db.Column(db.Integer, db.ForeignKey("Categoria.id_Categoria"), nullable=False)

class Pedido(db.Model):
    __tablename__ = "Pedido"
    id_Pedido = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    direccion = db.Column(db.String(160))
    total = db.Column(db.Float, default=0)
    estatus = db.Column(db.Integer, default=1)
    id_Usuario = db.Column(db.Integer, db.ForeignKey("Usuario.id_Usuario"), nullable=False)

class DetallePedido(db.Model):
    __tablename__ = "DetallePedido"
    id_Detalle = db.Column(db.Integer, primary_key=True)
    precio = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, default=1)
    id_Producto = db.Column(db.Integer, db.ForeignKey("Producto.id_Producto"), nullable=False)
    id_Pedido = db.Column(db.Integer, db.ForeignKey("Pedido.id_Pedido"), nullable=False)
