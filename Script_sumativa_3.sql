create database db_administradores;
use db_administradores;
create table AppAdministracion_Vehiculos
(
	patente varchar(6) primary key,
	numero_chasis varchar(17) unique not null,
	marca varchar(20) not null,
	modelo varchar(10) not null,
	ultima_revision datetime not null,
	proxima_revision datetime not null,
	observaciones varchar(200)
);

create table AppAdministracion_InsumosComputacionales
(
	numero_insumo int primary key,
	nombre varchar(50) not null,
	fecha_adquisicion datetime not null,
	marca varchar(30) not null,
	stock int not null,
	descripcion varchar(100) not null
);

create table AppAdministracion_InsumosOficina
(
	nro_articulo int primary key,
	nombre varchar(50) not null,
	ubicacion varchar(25) not null,
	stock int not null,
	descripcion varchar(100) not null
);

create table AppAdministracion_Usuarios
(
	username varchar(25) primary key,
	password varchar(40) unique not null,
	email varchar(60) not null,
	nombre varchar(60) not null,
	perfil int not null
);

insert into AppAdministracion_Usuarios values('admin', 'adminadmin','a@admin.cl','administrador general',0)