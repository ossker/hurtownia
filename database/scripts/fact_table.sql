CREATE TABLE statystyki (
    id NUMBER PRIMARY KEY,
    rok VARCHAR2(5) NOT NULL,
    kierunek_id NUMBER NOT NULL,
    studenci_id NUMBER NOT NULL,
    absolwenci_id NUMBER NOT NULL,
    uczelnia_id NUMBER NOT NULL,
    CONSTRAINT fk_statystki_kierunek FOREIGN KEY (kierunek_id) REFERENCES kierunek(id),
    CONSTRAINT fk_statystki_studenci FOREIGN KEY (studenci_id) REFERENCES studenci(id),
    CONSTRAINT fk_statystki_absolwenci FOREIGN KEY (absolwenci_id) REFERENCES absolwenci(id),
    CONSTRAINT fk_statystki_uczelnia FOREIGN KEY (uczelnia_id) REFERENCES uczelnia(id)
);