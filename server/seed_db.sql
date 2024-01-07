-- SEED DATABASE

-- Populate Reservations
INSERT INTO reservations (username, equipment, start_date, end_date, active, cost, downpayment, location) VALUES ('jdoe', 'ore scooper', '2021-01-01 00:00:00', '2021-01-01 00:30:00', 'TRUE', 100, 50, '19 18');
INSERT INTO reservations (username, equipment, start_date, end_date, active, cost, downpayment, location) VALUES ('jp', 'ore scooper', '2021-01-01 00:00:00', '2021-01-01 00:30:00', 'TRUE', 100, 50, '19 18');
INSERT INTO reservations (username, equipment, start_date, end_date, active, cost, downpayment, location) VALUES ('jm', '1.21 gigawatt lightning harvester', '2021-01-01 00:00:00', '2021-01-01 00:30:00', 'TRUE', 100, 50, '19 18');


INSERT INTO reservations (username, equipment, start_date, end_date, active, cost, downpayment, location) VALUES ('John Doe', 'ore scooper', '2021-01-01 00:00:00', '2021-01-01 00:30:00', 'TRUE', 100, 50, '19 18');
INSERT INTO reservations (username, equipment, start_date, end_date, active, cost, downpayment, location) VALUES ('John Doe', 'ore scooper', '2021-01-01 00:00:00', '2021-01-01 00:30:00', 'TRUE', 100, 50, '19 18');

-- Populate machines
INSERT INTO machines (equipment, available, cost) VALUES ('multi-phasic radiation scanner', 4, 990);
INSERT INTO machines (equipment, available, cost) VALUES ('ore scooper', 1000, 4);
INSERT INTO machines (equipment, available, cost) VALUES ('1.21 gigawatt lightning harvester',1, 88000);



-- Populate roles
INSERT INTO roles (role) VALUES ('scheduler'); --1
INSERT INTO roles (role) VALUES ('customer'); --2
INSERT INTO roles (role) VALUES ('admin'); --3


-- Populate users -- Create at least 10
-- scheduler
INSERT INTO users (username, first_name, active) VALUES ('abk', 'Abishek', 'TRUE'); 
INSERT INTO users (username, first_name, active) VALUES ('zk', 'Zhenyi', 'TRUE'); 
INSERT INTO users (username, first_name, active) VALUES ('ank', 'Anthony', 'TRUE'); 
INSERT INTO users (username, first_name, active) VALUES ('ll', 'Leon', 'TRUE'); 
-- customer
INSERT INTO users (username, first_name, active) VALUES ('jdoe', 'John', 'TRUE');
INSERT INTO users (username, first_name, active) VALUES ('jp', 'Jane', 'TRUE');
INSERT INTO users (username, first_name, active) VALUES ('jm', 'Jim', 'TRUE');
INSERT INTO users (username, first_name, active) VALUES ('jl', 'Jill', 'TRUE');
-- admin
INSERT INTO users (username, first_name, active) VALUES ('pv', 'Peter', 'TRUE');
INSERT INTO users (username, first_name, active) VALUES ('oo', 'Oliver', 'TRUE');

-- Populate user_roles
INSERT INTO user_roles (user_id, role_id) VALUES (1, 1);
INSERT INTO user_roles (user_id, role_id) VALUES (2, 1);
INSERT INTO user_roles (user_id, role_id) VALUES (3, 1);
INSERT INTO user_roles (user_id, role_id) VALUES (4, 1);
INSERT INTO user_roles (user_id, role_id) VALUES (5, 2);
INSERT INTO user_roles (user_id, role_id) VALUES (6, 2);
INSERT INTO user_roles (user_id, role_id) VALUES (7, 2);
INSERT INTO user_roles (user_id, role_id) VALUES (8, 2);
INSERT INTO user_roles (user_id, role_id) VALUES (9, 3);
INSERT INTO user_roles (user_id, role_id) VALUES (10, 3);
