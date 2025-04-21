-- Tworzenie tabeli Grupy
CREATE TABLE grupa (
    id NUMBER PRIMARY KEY,
    nazwa VARCHAR2(200) NOT NULL
);

-- Tworzenie tabeli Podgrupy
CREATE TABLE podgrupa (
    id NUMBER PRIMARY KEY,
    nazwa VARCHAR2(200) NOT NULL,
    grupa_id NUMBER NOT NULL,
    CONSTRAINT fk_Podgrupy_Grupy FOREIGN KEY (grupa_id) REFERENCES grupa(id)
);

-- Tworzenie tabeli NazwyKierunków
CREATE TABLE nazwa_kierunkow (
    id NUMBER PRIMARY KEY,
    nazwa VARCHAR2(200) NOT NULL,
    podgrupa_id NUMBER NOT NULL,
    CONSTRAINT fk_NazwyKierunków_Podgrupy FOREIGN KEY (podgrupa_id) REFERENCES podgrupa(id)
);

-- Tworzenie tabeli Stopnie
CREATE TABLE stopien (
    id NUMBER PRIMARY KEY,
    nazwa VARCHAR2(200) NOT NULL
);

-- Tworzenie tabeli Kierunki
CREATE TABLE kierunek (
    id NUMBER PRIMARY KEY,
    nazwa VARCHAR2(200) NOT NULL,
    nazwa_kierunkow_id NUMBER NOT NULL,
    stopien_id NUMBER NOT NULL,
    CONSTRAINT fk_Kierunki_NazwyKierunków FOREIGN KEY (nazwa_kierunkow_id) REFERENCES nazwa_kierunkow(id),
    CONSTRAINT fk_Kierunki_Stopnie FOREIGN KEY (stopien_id) REFERENCES stopien(id)
);

-- Tworzenie sekwencji
CREATE SEQUENCE grupy_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE podgrupy_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE nazwy_kier_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE stopnie_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE kierunki_seq START WITH 1 INCREMENT BY 1;
