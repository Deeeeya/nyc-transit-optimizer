CREATE TABLE stop_times (
    trip_id TEXT NOT NULL REFERENCES trips(trip_id),
    stop_sequence INTEGER NOT NULL,
    stop_id TEXT NOT NULL REFERENCES stops(stop_id),
    arrival_seconds INTEGER NOT NULL,
    departure_seconds INTEGER NOT NULL,
    PRIMARY KEY (trip_id, stop_sequence)
);

ALTER TABLE stop_times ENABLE ROW LEVEL SECURITY;