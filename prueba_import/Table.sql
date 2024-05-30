-- Crear la tabla estadisticas
CREATE TABLE estadisticas (
    victorias_jugador INT DEFAULT 0,
    derrotas_jugador INT DEFAULT 0,
    victorias_ia INT DEFAULT 0,
    derrotas_ia INT DEFAULT 0
);

-- Insertar los datos iniciales
INSERT INTO estadisticas (victorias_jugador, derrotas_jugador, victorias_ia, derrotas_ia)
VALUES (0, 0, 0, 0);

-- Verificar los datos insertados
SELECT * FROM estadisticas;