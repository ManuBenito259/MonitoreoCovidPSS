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
DROP TABLE IF EXISTS users;

CREATE TABLE centroSalud(
    id INTEGER AUTO_INCREMENT,
    nombre VARCHAR(45) NOT NULL,
    ubicacion INTEGER NOT NULL,
    direccion VARCHAR(45) NOT NULL,
    mail VARCHAR(50) NOT NULL,
    telefono INTEGER NOT NULL,
    publico BOOLEAN NOT NULL,
    responsable TEXT NOT NULL,

    CONSTRAINT pk_centroSalud
    PRIMARY KEY (id),

    CONSTRAINT fk_centroSalud_ubicacion
    FOREIGN KEY (ubicacion) REFERENCES ubicacion(cp),

    
    CONSTRAINT fk_centroSalud_usuarioCarga
    FOREIGN KEY (responsable) REFERENCES users(username)

     
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
    centro INTEGER,

    CONSTRAINT pk_paciente
    PRIMARY KEY (dni),

    CONSTRAINT fk_paciente_centroSalud
    FOREIGN KEY (centro) REFERENCES centroSalud(id)
);


CREATE TABLE usuarioCarga(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    centroSalud VARCHAR(45) NOT NULL,

    CONSTRAINT fk_usuarioCarga_centroSalud
    FOREIGN KEY (centroSalud) REFERENCES centroSalud(nombre)
);

CREATE TABLE cargaDiaria(
    id INTEGER AUTO_INCREMENT,
    centroSalud INTEGER UNSIGNED NOT NULL,
    fecha VARCHAR(45) NOT NULL, /*TODO: fix date type */
    respDisp INTEGER UNSIGNED NOT NULL,
    respOc INTEGER UNSIGNED NOT NULL,
    camaUTIDisp INTEGER UNSIGNED NOT NULL,
    camaUTIOc INTEGER UNSIGNED NOT NULL,
    camaGCDisp INTEGER UNSIGNED NOT NULL,
    camaGCOc INTEGER UNSIGNED NOT NULL,
    pacNuevos INTEGER UNSIGNED NOT NULL,
    pacCovidNuevos INTEGER UNSIGNED NOT NULL,
    pacAlta INTEGER UNSIGNED NOT NULL,
    pacCOVIDAlta INTEGER UNSIGNED NOT NULL,
    pacFall INTEGER UNSIGNED NOT NULL,
    pacCOVIDFall INTEGER UNSIGNED NOT NULL,
    pacCOVIDUTI INTEGER UNSIGNED NOT NULL,
    pacUTI INTEGER UNSIGNED NOT NULL,

    CONSTRAINT pk_cargaDiaria
    PRIMARY KEY (id),

    CONSTRAINT fk_cargaDiaria_centroSalud
    FOREIGN KEY (centroSalud) REFERENCES centroSalud(id)

);



CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  type TEXT NOT NULL
);


