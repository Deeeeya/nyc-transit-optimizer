CREATE TABLE transfers (
    from_stop_id TEXT NOT NULL REFERENCES stops(stop_id),
    to_stop_id TEXT NOT NULL REFERENCES stops(stop_id),
    transfer_type INTEGER NOT NULL,
    min_transfer_time INTEGER NOT NULL,
    PRIMARY KEY (from_stop_id, to_stop_id)
);

ALTER TABLE transfers ENABLE ROW LEVEL SECURITY;