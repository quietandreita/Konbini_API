-- CREACIÓN DE LA BASE DE DATOS
create database Konbini;
use Konbini;

-- CREACIÓN DE TABLAS Y CLAVES PRIMARIAS
-- TABLA Usuarios
create table Usuario(
	id_Usuario int auto_increment primary key,
    nombre varchar(40) not null,
    correo varchar(100) not null,
    contrasena varchar(256) not null,
    tipo varchar(50) not null,
    estatus boolean not null
);

-- TABLA Producto
create table Producto(
	id_Producto int auto_increment primary key,
    nombre varchar(60) not null,
    precio float not null,
    existencias int not null,
    estatus boolean not null,
    imagen longblob,
    descripcion varchar(150) null,
    id_Categoria int not null
);

-- TABLA Categoría
create table Categoria(
	id_Categoria int auto_increment primary key,
    nombre varchar(20) not null,
    imagen longblob,
    estatus boolean not null
);
-- TABLA Pedido
create table Pedido(
	id_Pedido int auto_increment primary key,
    fecha date null,
    direccion varchar(160) null,
    total float null,
    estatus int not null,
    id_Usuario int not null
);
-- TABLA Detalle Pedido
create table DetallePedido(
	id_Detalle int auto_increment primary key,
    precio float not null,
    subtotal float not null,
    cantidad int not null,
    id_Producto int not null,
    id_Pedido int not null
);

-- IMPLEMENTACIÓN DE RESTRICCIONES DE INTEGRIDAD REFERENCIAL "FK"
-- TABLA Pedido
alter table Pedido add constraint Pedido_Usuario_FK
foreign key (id_Usuario) references Usuario (id_Usuario) ;
-- TABLA Producto
alter table Producto add constraint Producto_Categoria_FK
foreign key (id_Categoria) references Categoria(id_Categoria);
-- TABLA Detalle Pedido
alter table DetallePedido add constraint DetallePedido_Producto_FK
foreign key (id_Producto) references Producto(id_Producto);
alter table DetallePedido add constraint DetallePedido_Pedido_FK
foreign key (id_Pedido) references Pedido(id_Pedido);

-- IMPLEMENTACIÓN DE RESTRICCIONES DE IDENTIDAD "UNIQUE"
alter table Usuario add constraint uq_nombreU unique (nombre);
alter table Usuario add constraint uq_correoU unique (correo);
alter table Producto add constraint uq_nombreProd unique (nombre);
alter table Categoria add constraint uq_nombrecat unique (nombre);

-- APLICACIÓN DE RESTRICCIONES DE DOMINIO
-- TABLA Usuario
alter table Usuario add constraint chk_correoU check (correo regexp('^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'));
alter table Usuario add constraint chk_tipo check (tipo in('Cliente', 'Administrador'));
-- TABLA Pedido
alter table Pedido add constraint chk_total check (total >= 0);
-- TABLA Detalle Pedido
alter table DetallePedido add constraint chk_cantidad check (cantidad > 0);
-- TABLA Producto
alter table Producto add constraint chk_precio check (precio>0);

-- APLICACIÓN DE DEFAULTS
alter table Usuario alter column estatus set default true;
alter table Usuario alter column tipo set default 'Cliente';
alter table Categoria alter column estatus set default true;
alter table DetallePedido alter column cantidad set default 1;
alter table Pedido alter column estatus set default 1;
alter table Producto alter column estatus set default true;

-- INSERCIONES
-- TABLA USUARIOS
insert into usuario values(1,'Andrea','a@gmail.com','contra.123','Administrador',1);
insert into usuario values(2,'Cliente','c@gmail.com','contra.123','Cliente',1);

-- TABLA CATEGORÍA
insert into Categoria(nombre,estatus) values('Bebidas',1);
insert into Categoria(nombre,estatus) values('Ramen',1);
insert into Categoria(nombre,estatus) values('Dulces',1);
insert into Categoria(nombre,estatus) values ('Snacks', 1);

-- TABLA PRODUCTO
insert into producto(nombre, precio, existencias,estatus, descripcion, id_Categoria) 
values('Taiyaki Feliz Cumpleaños', 35.00, 52, true, 
'Deliciosa galleta en forma de taiyaki.', 3);
insert into producto(nombre, precio, existencias,estatus, descripcion, id_Categoria) 
values('Pocky Chocolate', 28.00, 40, false, 'Palitos crujientes cubiertos con chocolate japonés.', 3);
insert into producto(nombre, precio, existencias,estatus, descripcion, id_Categoria) 
values('Mochi de Fresa', 30.00, 50, true, 'Dulce japonés relleno de fresa con masa de arroz suave', 3);
insert into producto(nombre, precio, existencias,estatus, descripcion, id_Categoria) 
 values('Ramen Shin Spicy', 38.00, 25, true, 'Ramen coreano picante con fideos gruesos y caldo intenso', 2);
insert into producto(nombre, precio, existencias,estatus, descripcion, id_Categoria) 
 values('Pringles de Topokki Rosé', 100, 13, true, 
'Edición especial inspirada en uno de los platos más populares del Corea: el Topokki rosé.', 4);

select * from Producto;
select * from producto;
select * from categoria;