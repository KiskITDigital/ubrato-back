CREATE TABLE IF NOT EXISTS document_types (
    id     SERIAL       PRIMARY KEY,
    name   VARCHAR(255) NOT NULL
);

INSERT INTO document_types(name)
VALUES
    ('ЕГРЮЛ'),
    ('Карточка компании'),
    ('Приказ о назначение гендиректора'),
    ('Устав компании');