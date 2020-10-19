DROP TABLE IF EXISTS viewer_user;
DROP TABLE IF EXISTS uploader_user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS internal_user;
DROP TABLE IF EXISTS centroSalud;
DROP TABLE IF EXISTS ubicacion;
DROP TABLE IF EXISTS paciente;
DROP TABLE IF EXISTS usuarioCarga;
DROP TABLE IF EXISTS usuarioLector;
DROP TABLE IF EXISTS cargaDiaria;

CREATE TABLE centroSalud(
    id INTEGER UNSIGNED NOT NULL,
    nombre VARCHAR(45) NOT NULL,
    ubicacion INTEGER NOT NULL,
    direccion VARCHAR(45) NOT NULL,
    mail VARCHAR(50) NOT NULL,
    responsable INTEGER NOT NULL,
    telefono INTEGER NOT NULL,
    publico BOOLEAN NOT NULL,

    CONSTRAINT pk_centroSalud
    PRIMARY KEY (id),

    CONSTRAINT fk_centroSalud_ubicacion
    FOREIGN KEY (ubicacion) REFERENCES ubicacion(cp),

    CONSTRAINT fk_centroSalud_usuarioCarga
    FOREIGN KEY (responsable) REFERENCES usuarioCarga(dni)
);

CREATE TABLE ubicacion(
    cp INTEGER UNSIGNED NOT NULL,
    provincia VARCHAR(45) NOT NULL,
    ciudad VARCHAR(45) NOT NULL,

    CONSTRAINT pk_ubicacion
    PRIMARY KEY (cp)
);


CREATE TABLE paciente(
    dni INTEGER UNSIGNED NOT NULL,
    nombre VARCHAR(45) NOT NULL,
    apellido VARCHAR(45) NOT NULL,
    telefono INTEGER,
    estado VARCHAR(45) NOT NULL,

    CONSTRAINT pk_paciente
    PRIMARY KEY (dni)
);


CREATE TABLE usuarioLector(
    dni INTEGER UNSIGNED NOT NULL,
    nombre VARCHAR(45) NOT NULL,
    apellido VARCHAR(45) NOT NULL,
    jurisdiccion INTEGER NOT NULL,

    CONSTRAINT pk_usuarioLector
    PRIMARY KEY (dni),

    CONSTRAINT fk_usuarioLector_ubicacion
    FOREIGN KEY (jurisdiccion) REFERENCES ubicacion(cp)
);

CREATE TABLE usuarioCarga(
    dni INTEGER UNSIGNED NOT NULL,
    nombre VARCHAR(45) NOT NULL,
    apellido VARCHAR(45) NOT NULL,
    centroSalud INTEGER UNSIGNED NOT NULL,

    CONSTRAINT pk_usuarioCarga
    PRIMARY KEY (dni),

    CONSTRAINT fk_usuarioCarga_centroSalud
    FOREIGN KEY (centroSalud) REFERENCES centroSalud(id)
);

CREATE TABLE cargaDiaria(
    id INTEGER AUTO_INCREMENT,
    centroSalud INTEGER UNSIGNED NOT NULL,
    fecha DATE NOT NULL,
    respDisp INTEGER NOT NULL,
    respOc INTEGER NOT NULL,
    camaUTIDisp INTEGER NOT NULL,
    camaUTIOc INTEGER NOT NULL,
    camaGCDisp INTEGER NOT NULL,
    camaGCOc INTEGER NOT NULL,
    pacAlta INTEGER UNSIGNED,
    pacCOVIDAlta INTEGER UNSIGNED,
    pacFall INTEGER UNSIGNED,
    pacCOVIDFall INTEGER UNSIGNED,
    pacCOVIDUTI INTEGER UNSIGNED,
    pacUTI INTEGER UNSIGNED,

    CONSTRAINT pk_cargaDiaria
    PRIMARY KEY (id),

    CONSTRAINT fk_cargaDiaria_centroSalud
    FOREIGN KEY (centroSalud) REFERENCES centroSalud(id)

);

CREATE TABLE viewer_user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE uploader_user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);


CREATE TABLE admin (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);


CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);