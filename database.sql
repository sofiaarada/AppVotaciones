
CREATE DATABASE IF NOT EXISTS votaciones_db;
USE votaciones_db;


CREATE TABLE IF NOT EXISTS puestos_votacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lugar VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    mesa INT NOT NULL,
    zona VARCHAR(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS ciudadanos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    identificacion VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    puesto_id INT,
    FOREIGN KEY (puesto_id) REFERENCES puestos_votacion(id)
);


INSERT INTO puestos_votacion (lugar, direccion, mesa, zona) VALUES
('Escuela Nacional', 'Calle Principal 123', 1, 'Zona 1'),
('Colegio Central', 'Avenida Central 456', 2, 'Zona 2'),
('Instituto Técnico', 'Plaza Mayor 789', 3, 'Zona 3');