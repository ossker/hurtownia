DROP TABLE IF EXISTS uczelnia;
DROP TABLE IF EXISTS miasto;
DROP TABLE IF EXISTS wojewodztwo;

CREATE TABLE IF NOT EXISTS wojewodztwo (
    id SERIAL PRIMARY KEY,
    nazwa VARCHAR(100) NOT NULL,
    powierzchnia DECIMAL(10, 2) NOT NULL,
    liczba_ludnosci INTEGER NOT NULL,
    tablica_rejestracyjna VARCHAR(10) NOT NULL,
    kod_teryt VARCHAR(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS miasto (
    id SERIAL PRIMARY KEY,
    nazwa VARCHAR(100) NOT NULL,
    wojewodztwo_id INTEGER NOT NULL,
    powierzchnia DECIMAL(10, 2) NOT NULL,
    liczba_ludnosci INTEGER NOT NULL,
    tablica_rejestracyjna VARCHAR(10) NOT NULL,
    FOREIGN KEY (wojewodztwo_id) REFERENCES wojewodztwo(id)
);


CREATE TABLE IF NOT EXISTS uczelnia (
    id SERIAL PRIMARY KEY,
    nazwa VARCHAR(150) NOT NULL,
    miasto_id INTEGER NOT NULL,
    FOREIGN KEY (miasto_id) REFERENCES miasto(id)
);
