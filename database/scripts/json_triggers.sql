-- Tworzenie triggera dla tabeli Grupy
CREATE OR REPLACE TRIGGER trg_grupy
BEFORE INSERT ON grupa
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := grupy_seq.NEXTVAL;
    END IF;
END;
/

-- Tworzenie triggera dla tabeli Podgrupy
CREATE OR REPLACE TRIGGER trg_podgrupy
BEFORE INSERT ON podgrupa
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := podgrupy_seq.NEXTVAL;
    END IF;
END;
/

-- Tworzenie triggera dla tabeli NazwyKierunków
CREATE OR REPLACE TRIGGER trg_nazwy_kier
BEFORE INSERT ON nazwa_kierunkow
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := nazwy_kier_seq.NEXTVAL;
    END IF;
END;
/
-- Tworzenie triggera dla tabeli Stopnie
CREATE OR REPLACE TRIGGER trg_stopnie
BEFORE INSERT ON stopien
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := stopnie_seq.NEXTVAL;
    END IF;
END;
/

-- Tworzenie triggera dla tabeli Kierunki
CREATE OR REPLACE TRIGGER trg_kierunki
BEFORE INSERT ON kierunek
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := kierunki_seq.NEXTVAL;
    END IF;
END;
/