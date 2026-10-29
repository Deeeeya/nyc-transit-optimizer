CREATE TABLE calendar_dates (
    service_id TEXT NOT NULL,
    service_date DATE NOT NULL,
    exception_type INTEGER NOT NULL,
    PRIMARY KEY (service_id, service_date)
);

ALTER TABLE calendar_dates ENABLE ROW LEVEL SECURITY;