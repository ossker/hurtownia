-- Tworzenie tabeli Grupy
CREATE TABLE Grupy (
    IdGrupy NUMBER PRIMARY KEY,
    nazwa VARCHAR2(200) NOT NULL
);

-- Tworzenie tabeli Podgrupy
CREATE TABLE Podgrupy (
    IdPodgrupy NUMBER PRIMARY KEY,
    nazwa VARCHAR2(200) NOT NULL,
    IdGrupy NUMBER NOT NULL,
    CONSTRAINT fk_Podgrupy_Grupy FOREIGN KEY (IdGrupy) REFERENCES Grupy(IdGrupy)
);

-- Tworzenie tabeli NazwyKierunków
CREATE TABLE NazwyKierunków (
    IdNazwKierunków NUMBER PRIMARY KEY,
    nazwa VARCHAR2(200) NOT NULL,
    IdPodgrupy NUMBER NOT NULL,
    CONSTRAINT fk_NazwyKierunków_Podgrupy FOREIGN KEY (IdPodgrupy) REFERENCES Podgrupy(IdPodgrupy)
);

-- Tworzenie tabeli Stopnie
CREATE TABLE Stopnie (
    IdStopnia NUMBER PRIMARY KEY,
    nazwa VARCHAR2(200) NOT NULL
);

-- Tworzenie tabeli Kierunki
CREATE TABLE Kierunki (
    idKierunku NUMBER PRIMARY KEY,
    nazwaKierunku VARCHAR2(200) NOT NULL,
    idNazwKierunków NUMBER NOT NULL,
    IdStopnia NUMBER NOT NULL,
    CONSTRAINT fk_Kierunki_NazwyKierunków FOREIGN KEY (idNazwKierunków) REFERENCES NazwyKierunków(IdNazwKierunków),
    CONSTRAINT fk_Kierunki_Stopnie FOREIGN KEY (IdStopnia) REFERENCES Stopnie(IdStopnia)
);

-- Tworzenie sekwencji
CREATE SEQUENCE grupy_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE podgrupy_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE nazwy_kier_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE stopnie_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE kierunki_seq START WITH 1 INCREMENT BY 1;

-- Tworzenie triggera dla tabeli Grupy
CREATE OR REPLACE TRIGGER trg_grupy
BEFORE INSERT ON Grupy
FOR EACH ROW
BEGIN
    IF :NEW.IdGrupy IS NULL THEN
        SELECT grupy_seq.NEXTVAL INTO :NEW.IdGrupy FROM dual;
    END IF;
END;
/

-- Tworzenie triggera dla tabeli Podgrupy
CREATE OR REPLACE TRIGGER trg_podgrupy
BEFORE INSERT ON Podgrupy
FOR EACH ROW
BEGIN
    IF :NEW.IdPodgrupy IS NULL THEN
        SELECT podgrupy_seq.NEXTVAL INTO :NEW.IdPodgrupy FROM dual;
    END IF;
END;
/

-- Tworzenie triggera dla tabeli NazwyKierunków
CREATE OR REPLACE TRIGGER trg_nazwy_kier
BEFORE INSERT ON NazwyKierunków
FOR EACH ROW
BEGIN
    IF :NEW.IdNazwKierunków IS NULL THEN
        SELECT nazwy_kier_seq.NEXTVAL INTO :NEW.IdNazwKierunków FROM dual;
    END IF;
END;
/

-- Tworzenie triggera dla tabeli Stopnie
CREATE OR REPLACE TRIGGER trg_stopnie
BEFORE INSERT ON Stopnie
FOR EACH ROW
BEGIN
    IF :NEW.IdStopnia IS NULL THEN
        SELECT stopnie_seq.NEXTVAL INTO :NEW.IdStopnia FROM dual;
    END IF;
END;
/

-- Tworzenie triggera dla tabeli Kierunki
CREATE OR REPLACE TRIGGER trg_kierunki
BEFORE INSERT ON Kierunki
FOR EACH ROW
BEGIN
    IF :NEW.idKierunku IS NULL THEN
        SELECT kierunki_seq.NEXTVAL INTO :NEW.idKierunku FROM dual;
    END IF;
END;
/
