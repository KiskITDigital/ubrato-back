CREATE TABLE IF NOT EXISTS draft_tender (
    id                  SERIAL          PRIMARY KEY,
    user_id             VARCHAR(40)     NOT NULL REFERENCES users(id),
    name                VARCHAR(255)    NOT NULL,
    price               INT             NULL,
    is_contract_price   BOOLEAN         NULL DEFAULT NULL,
    is_nds_price        BOOLEAN         NULL DEFAULT NULL,
    city_id             INT             NULL DEFAULT NULL REFERENCES cities(id),
    floor_space         INT             NULL DEFAULT NULL,
    description         VARCHAR(400)    NULL DEFAULT NULL,
    wishes              VARCHAR(400)    NULL DEFAULT NULL,
    specification       VARCHAR(400)    NULL DEFAULT NULL,
    attachments         TEXT[]          NULL DEFAULT NULL,
    reception_start     TIMESTAMPTZ     NULL DEFAULT NULL,
    reception_end       TIMESTAMPTZ     NULL DEFAULT NULL,
    work_start          TIMESTAMPTZ     NULL DEFAULT NULL,
    work_end            TIMESTAMPTZ     NULL DEFAULT NULL,
    update_at           TIMESTAMPTZ     NULL DEFAULT NULL
);