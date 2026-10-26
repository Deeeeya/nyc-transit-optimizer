CREATE TABLE routes (
    route_id TEXT PRIMARY KEY,
    route_short_name TEXT NOT NULL,
    route_long_name TEXT NOT NULL,
    route_type INTEGER NOT NULL,
    route_color TEXT NOT NULL,
    route_text_color TEXT NOT NULL,
    route_sort_order INTEGER NOT NULL
);

ALTER TABLE routes ENABLE ROW LEVEL SECURITY;