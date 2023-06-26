drop table if exists webform;
drop table if exists events;

create table webform ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL DEFAULT no_name,
    phonenumber TEXT NOT NULL,
    url TEXT NOT NULL,
    event_date TIMESTAMP
);

create table events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    event_date TIMESTAMP,
    is_event INTEGER NOT NULL 
);