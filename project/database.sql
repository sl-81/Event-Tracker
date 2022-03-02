CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);


CREATE UNIQUE INDEX username ON users (username);

CREATE TABLE events(
    user_id INTEGER,
    event_time DATETIME,
    activity TEXT NOT NULL,
    event_type TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

SELECT * FROM events WHERE event_time >= CURRENT_TIMESTAMP AND event_time <= DATE("NOW", "+7 DAY");

SELECT * FROM events WHERE user_id=1 AND DATE(event_time) = '2022-07-14';