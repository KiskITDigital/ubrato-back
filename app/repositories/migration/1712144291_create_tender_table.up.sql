CREATE TABLE IF NOT EXISTS tender (
    id                  SERIAL          PRIMARY KEY,
    name                VARCHAR(255)    NOT NULL,
    price               INT             NOT NULL,
    is_contract_price   BOOLEAN         NOT NULL DEFAULT FALSE,
    city_id             INT             NOT NULL REFERENCES cities(id),
    floor_space         INT             NOT NULL,
    description         VARCHAR(400)    NULL,
    wishes              VARCHAR(400)    NULL,
    attachments         TEXT[]          NULL,
    services_groups     INTEGER[]       NULL,
    services_types      INTEGER[]       NULL,
    active              BOOLEAN         NOT NULL DEFAULT FALSE,
    reception_start     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reception_end       TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    work_start          TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    work_end            TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    object_group_id     INT             REFERENCES objects_groups(id),
    object_type_id      INT             REFERENCES objects_types(id),
    user_id             VARCHAR(40)     NOT NULL REFERENCES users(id),
    created_at          TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    verified            BOOLEAN         NOT NULL DEFAULT FALSE,
    document_tsv        tsvector
);

CREATE INDEX idx_tender_city_id ON tender(city_id);

CREATE OR REPLACE FUNCTION update_tender_document_tsv() RETURNS TRIGGER AS $$
BEGIN
    SELECT setweight(to_tsvector('russian', coalesce(NEW.name, '')), 'A') ||
           setweight(to_tsvector('russian', coalesce(NEW.description, '')), 'B') ||
           setweight(to_tsvector('russian', coalesce(NEW.wishes, '')), 'B') ||
           setweight(to_tsvector('russian', coalesce(cities.name, '')), 'B')
    INTO NEW.document_tsv
    FROM cities
    WHERE cities.id = NEW.city_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsvector_update_tender
BEFORE INSERT OR UPDATE OF name, description, wishes ON tender
FOR EACH ROW EXECUTE FUNCTION update_tender_document_tsv();
