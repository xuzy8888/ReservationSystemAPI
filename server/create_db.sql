
-- Maintains information on the reservations
DROP TABLE IF EXISTS reservations;
CREATE TABLE reservations (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR,
    equipment VARCHAR,
    start_date DATETIME,
    end_date DATETIME,
    active BOOLEAN,
    cost INTEGER,
    downpayment INTEGER,
    location VARCHAR,
    FOREIGN KEY (username) REFERENCES users(username)
);


-- Maintains information on the precise time that machines are booked
DROP TABLE IF EXISTS machine_bookings;
CREATE TABLE IF NOT EXISTS machine_bookings (
    reservation_id INTEGER,
    equipment VARCHAR,
    time_slot DATETIME,
    active BOOLEAN,
    machine_id VARCHAR
   
);

-- Maintains user information
DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR,
    first_name VARCHAR,
    active BOOLEAN
);

-- Maintains information about user roles
DROP TABLE IF EXISTS roles;
CREATE TABLE IF NOT EXISTS roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role VARCHAR
);

-- Maintains information about which users have which roles
DROP TABLE IF EXISTS user_roles;
CREATE TABLE user_roles (
    user_id INTEGER,
    role_id INTEGER,
    PRIMARY KEY (user_id, role_id)
);

-- Maintains information on the number of machines available
DROP TABLE IF EXISTS machines;
CREATE TABLE IF NOT EXISTS machines (
    equipment VARCHAR,
    available INTEGER,
    cost int
);

----- CREATE VIEWS TO MAKE LIFE EASIER -----
DROP VIEW IF EXISTS user_roles_view;
CREATE VIEW user_roles_view AS
    SELECT
        u.user_id,
        u.username,
        u.first_name,
        u.active,
        r.role
    FROM users u
    INNER JOIN user_roles ur ON u.user_id = ur.user_id
    INNER JOIN roles r ON ur.role_id = r.role_id;

DROP VIEW IF EXISTS reservations_view;
CREATE VIEW reservations_view AS
    SELECT
        r.reservation_id,
        r.username as username,
        u.first_name,
        r.equipment as equipment,
        r.start_date,
        r.end_date,
        r.active,
        r.cost,
        r.downpayment,
        r.location
    FROM reservations r
    INNER JOIN users u ON r.username = u.username;