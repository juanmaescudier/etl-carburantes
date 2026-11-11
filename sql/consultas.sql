/*DOCUMENTO DE CONSULTAS SQL DE LA ACTIVIDAD 1 DE BASES DE DATOS AVANZADAS

  En siguiente documento se muestran las 5 consultas resultado de la
  realización de la actividad 1 de Bases de Datos Avanzadas del PFU
 */

-- Consulta 1: Nombre de la empresa con más estaciones de servicio terrestres.

SELECT e.nombre AS nombre_empresa, COUNT(g.id) AS num_estaciones_terrestres
FROM empresa e
    INNER JOIN gasolinera g ON e.id = g.empresa_id
WHERE g.tipo='T' AND e.nombre <> 'DESCONOCIDA'
GROUP BY e.nombre
ORDER BY num_estaciones_terrestres DESC
LIMIT 1;

-- Consulta 2: Nombre de la empresa con más estaciones de servicio marítimas.

SELECT e.nombre AS nombre_empresa, COUNT(g.id) AS num_estaciones_maritimas
FROM empresa e
    INNER JOIN gasolinera g ON e.id = g.empresa_id
WHERE g.tipo='M' AND e.nombre <> 'DESCONOCIDA'
GROUP BY e.nombre
ORDER BY num_estaciones_maritimas DESC
LIMIT 1;

-- Consulta 3: Estación con el precio más bajo para Gasolina 95 E5 en Madrid.
--
-- Hay 4 estaciones empatadas en el precio mínimo (1,499 €), comprobado
-- ejecutando la consulta sin LIMIT. El LIMIT 4 depende de los datos de esta
-- foto: con otro fichero habría que revisarlo. Alternativa más robusta
-- (sugerida con ayuda de IA): filtrar con una subconsulta
-- WHERE p.precio = (SELECT MIN(...) ...), que devuelve todas las empatadas.

SELECT
    e.nombre AS NOMBRE_EMPRESA,
    g.provincia AS PROVINCIA,
    g.municipio AS MUNICIPIO,
    g.localidad AS LOCALIDAD,
    g.direccion AS DIRECCION,
    g.margen AS MARGEN,
    c.nombre AS CARBURANTE,
    p.precio AS PRECIO
FROM empresa e
    INNER JOIN gasolinera g ON e.id=g.empresa_id
    INNER JOIN precio p ON p.gasolinera_id=g.id
    INNER JOIN carburante c ON c.id=p.carburante_id
WHERE c.nombre='gasolina 95 E5' AND g.provincia='MADRID'
ORDER BY PRECIO
LIMIT 4;

-- Consulta 4: Estación con el precio más bajo para Gasóleo A si resido en el
-- centro de Albacete y no quiero desplazarme más de 10 km.
--
-- Las coordenadas de @lat_centro y @lon_centro son el punto tomado como
-- centro de Albacete. La distancia se calcula en línea recta con
-- ST_Distance_Sphere (en metros; se divide entre 1000 para mostrarla en km),
-- no por carretera. Ojo: POINT recibe primero la longitud y luego la latitud.
--
-- Comprobado ejecutando la consulta sin LIMIT: 40 estaciones a menos de
-- 10 km venden Gasóleo A y 4 empatan en el precio mínimo (1,729 €). Por eso
-- se ordena por PRECIO y, en caso de empate, por DISTANCIA_KM: así LIMIT 1
-- devuelve siempre la más cercana de las más baratas, y no una cualquiera.

SET @lat_centro = 38.99485260992702;
SET @lon_centro = -1.8536802323420551;

SELECT
    e.nombre AS NOMBRE_EMPRESA,
    g.municipio AS MUNICIPIO,
    g.localidad AS LOCALIDAD,
    g.direccion AS DIRECCION,
    g.margen AS MARGEN,
    c.nombre AS CARBURANTE,
    p.precio AS PRECIO,
    ROUND(ST_Distance_Sphere(
       POINT(g.longitud, g.latitud),
       POINT(@lon_centro, @lat_centro)
       ) / 1000, 3) AS DISTANCIA_KM
FROM empresa e
    INNER JOIN gasolinera g ON g.empresa_id = e.id
    INNER JOIN precio p ON g.id = p.gasolinera_id
    INNER JOIN carburante c ON c.id = p.carburante_id
WHERE c.nombre = 'gasóleo A'
    AND g.tipo = 'T'
    AND ST_Distance_Sphere(
        POINT(g.longitud, g.latitud),
        POINT(@lon_centro, @lat_centro)
        ) <= 10000
ORDER BY PRECIO, DISTANCIA_KM
LIMIT 1;

-- Consulta 5: Provincia donde se encuentra la estación marítima con el precio
-- de Gasolina 95 E5 más caro
--
-- Comprobado ejecutando la consulta sin LIMIT: el precio máximo (2,200 €) lo
-- tiene una sola estación, así que no hay empate y LIMIT 1 es correcto con
-- los datos de esta foto. Si con otro fichero empataran varias, habría que
-- revisarlo. Alternativa más robusta (sugerida con ayuda de IA): filtrar con
-- WHERE p.precio = (SELECT MAX(...) ...), que devuelve todas las empatadas.

SELECT
    g.provincia AS PROVINCIA,
    c.nombre AS CARBURANTE,
    p.precio AS PRECIO
FROM carburante c
    INNER JOIN precio p ON c.id=p.carburante_id
    INNER JOIN gasolinera g ON p.gasolinera_id=g.id
WHERE g.tipo='M' AND c.nombre='gasolina 95 E5'
ORDER BY PRECIO DESC
LIMIT 1;

-- Chequeo para comprobar si las tablas están vacías o no

SELECT 'empresa' AS tabla, COUNT(*) AS filas FROM empresa
UNION ALL SELECT 'carburante', COUNT(*) FROM carburante
UNION ALL SELECT 'gasolinera', COUNT(*) FROM gasolinera
UNION ALL SELECT 'precio', COUNT(*) FROM precio;