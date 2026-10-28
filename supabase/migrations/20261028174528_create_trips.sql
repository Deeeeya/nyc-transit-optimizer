CREATE TABLE trips (
    trip_id TEXT PRIMARY KEY,
    route_id TEXT NOT NULL REFERENCES routes(route_id),
    service_id TEXT NOT NULL,
    trip_headsign TEXT NOT NULL,
    direction_id INTEGER NOT NULL
);

ALTER TABLE trips ENABLE ROW LEVEL SECURITY;