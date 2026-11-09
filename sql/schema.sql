/*CREACIÓN DE LA BASE DE DATOS

En el caso de que existan datos antiguos se
eliminan con DROP TABLE IF EXISTS*/

CREATE DATABASE IF NOT EXISTS etl_carburantes;
USE etl_carburantes;

DROP TABLE IF EXISTS precio;
DROP TABLE IF EXISTS gasolinera;
DROP TABLE IF EXISTS carburante;
DROP TABLE IF EXISTS empresa;

CREATE TABLE empresa(
    id INT AUTO_INCREMENT,
    nombre VARCHAR(150) NOT NULL UNIQUE,
    PRIMARY KEY(id)
);

CREATE TABLE carburante(
    id INT AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY(id)
);

CREATE TABLE gasolinera(
    id INT AUTO_INCREMENT,
    empresa_id INT NOT NULL,
    tipo CHAR(1) NOT NULL,
    provincia VARCHAR(50) NOT NULL,
    municipio VARCHAR(100) NOT NULL,
    localidad VARCHAR(100) NOT NULL,
    codigo_postal CHAR(5) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    margen CHAR(1),
    latitud DECIMAL(9,6),
    longitud DECIMAL(9,6),
    fecha_toma_datos DATETIME,
    horario VARCHAR(150) NOT NULL,
    tipo_venta VARCHAR(60) NOT NULL,
    rem CHAR(2) NOT NULL,
    tipo_servicio VARCHAR(600),
    pct_bioalcohol DECIMAL(5,2),
    pct_ester_metilico DECIMAL(5,2),
    PRIMARY KEY(id),
    CONSTRAINT fk_gasolinera_empresa
        FOREIGN KEY (empresa_id) REFERENCES empresa(id)
);

CREATE TABLE precio(
    gasolinera_id INT,
    carburante_id INT,
    precio DECIMAL(7,3) NOT NULL,
    PRIMARY KEY(gasolinera_id, carburante_id),
    CONSTRAINT fk_precio_gasolinera
        FOREIGN KEY (gasolinera_id) REFERENCES gasolinera(id),
    CONSTRAINT fk_precio_carburante
        FOREIGN KEY (carburante_id) REFERENCES carburante(id)
);
