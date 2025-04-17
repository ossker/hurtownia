CREATE TABLE wojewodztwo (
    id NUMBER PRIMARY KEY,
    nazwa VARCHAR2(150) NOT NULL
);

CREATE TABLE miasto (
    id NUMBER PRIMARY KEY,
    nazwa VARCHAR2(150) NOT NULL,
    wojewodztwo_id NUMBER NOT NULL,
    CONSTRAINT fk_miasto_wojewodztwo FOREIGN KEY (wojewodztwo_id) REFERENCES wojewodztwo(id)
);

CREATE TABLE uczelnia (
    id NUMBER PRIMARY KEY,
    nazwa VARCHAR2(150) NOT NULL,
    miasto_id NUMBER NOT NULL,
    CONSTRAINT fk_uczelnia_miasto FOREIGN KEY (miasto_id) REFERENCES miasto(id)
);
