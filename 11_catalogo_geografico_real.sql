-- =============================================================================
-- PROYECTO: Sistema de Gestión de Reservas y Hospedaje - Hotel Don Quesada Boutique
-- ARCHIVO: 11_catalogo_geografico_real.sql (VERSIÓN SEGURA E IDEMPOTENTE)
-- Agrega países, estados y ciudades sin romper las llaves foráneas de guest
-- =============================================================================

-- =============================================================================
-- 1. AGREGAR PAÍSES REALES (Sin borrar los que ya usan los 1.000 huéspedes)
-- =============================================================================
INSERT INTO country (name) VALUES 
('Colombia'),
('Venezuela'),
('Ecuador'),
('Estados Unidos'),
('España'),
('Panamá'),
('México'),
('Perú')
ON CONFLICT (name) DO NOTHING;

-- Sincronizar secuencia de países
SELECT setval('country_id_country_seq', (SELECT MAX(id_country) FROM country));

-- =============================================================================
-- 2. AGREGAR DEPARTAMENTOS REALES (state)
-- =============================================================================
-- Limpiar ciudades y departamentos (que no tienen huéspedes apuntándoles directamente)
TRUNCATE TABLE city RESTART IDENTITY CASCADE;
TRUNCATE TABLE state RESTART IDENTITY CASCADE;

INSERT INTO state (name) VALUES 
('Norte de Santander'),             -- ID 1
('Santander'),                      -- ID 2
('Cesar'),                          -- ID 3
('Cundinamarca / Bogotá D.C.'),     -- ID 4
('Antioquia'),                      -- ID 5
('Atlántico'),                      -- ID 6
('Magdalena'),                      -- ID 7
('Valle del Cauca'),                -- ID 8
('Bolívar'),                        -- ID 9
('Táchira (Venezuela)');            -- ID 10

SELECT setval('state_id_state_seq', (SELECT MAX(id_state) FROM state));

-- =============================================================================
-- 3. AGREGAR CIUDADES REALES (city)
-- =============================================================================
-- Asumiendo que id_country = 1 es Colombia y id_country = 2 es Venezuela
INSERT INTO city (name, id_state, id_country) VALUES 
-- Ciudades de Norte de Santander (Provincia de Ocaña y alrededores)
('Ocaña', 1, 1),
('Ábrego', 1, 1),
('Convención', 1, 1),
('La Playa de Belén', 1, 1),
('Cúcuta', 1, 1),
('Pamplona', 1, 1),
('Los Patios', 1, 1),

-- Ciudades de Santander
('Bucaramanga', 2, 1),
('Floridablanca', 2, 1),
('Barrancabermeja', 2, 1),

-- Ciudades de Cesar (muy cercanas a Ocaña)
('Aguachica', 3, 1),
('Valledupar', 3, 1),
('Pelaya', 3, 1),
('Río de Oro', 3, 1),

-- Ciudades principales de Colombia
('Bogotá D.C.', 4, 1),
('Medellín', 5, 1),
('Barranquilla', 6, 1),
('Santa Marta', 7, 1),
('Cali', 8, 1),
('Cartagena', 9, 1),

-- Ciudades internacionales fronterizas
('San Cristóbal', 10, 2);

-- =============================================================================
-- VERIFICACIÓN
-- =============================================================================
SELECT 'Paises registrados: ' || COUNT(*) FROM country
UNION ALL
SELECT 'Departamentos registrados: ' || COUNT(*) FROM state
UNION ALL
SELECT 'Ciudades registradas: ' || COUNT(*) FROM city;
