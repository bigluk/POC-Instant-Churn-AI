CREATE TABLE ISBD_USERS (
    id BIGINT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(30),
    age INT,
    job VARCHAR(100),
    marital VARCHAR(50),
    education VARCHAR(100),
    default_status VARCHAR(10),
    balance NUMERIC(12,2),
    housing VARCHAR(10),
    loan VARCHAR(10),
    investment_propensity NUMERIC(10,2)
);


CREATE TABLE INVESTMENT_PROPENSITY_USER (
    user_id BIGINT REFERENCES ISBD_USERS(id) ON DELETE CASCADE,
    investment_propensity NUMERIC(10,2) NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, timestamp)
);


INSERT INTO ISBD_USERS (id, first_name, last_name, email, phone_number, age, job, marital, education, default_status, balance, housing, loan, investment_propensity) VALUES
(239029, 'John', 'Doe', 'john.doe@example.com', '+390211234567', 41, 'management', 'single', 'tertiary', 'no', 572.00, 'yes', 'no', NULL),
(99820014, 'Alice', 'Brown', 'alice.brown@example.com', '+390212345678', 40, 'technician', 'single', 'secondary', 'no', 1775.00, 'no', 'yes', NULL),
(551102, 'Mark', 'Wilson', 'mark.wilson@example.com', '+390213456789', 33, 'management', 'single', 'tertiary', 'no', 71.00, 'no', 'no', NULL),
(73488901, 'Emma', 'Taylor', 'emma.taylor@example.com', '+390214567890', 43, 'self-employed', 'married', 'tertiary', 'no', 4324.00, 'yes', 'no', NULL),
(11892, 'James', 'Anderson', 'james.anderson@example.com', '+390215678901', 33, 'management', 'married', 'secondary', 'no', 5197.00, 'yes', 'no', NULL),
(99017733, 'Sophia', 'Miller', 'sophia.miller@example.com', '+390216789012', 47, 'management', 'single', 'secondary', 'no', 1562.00, 'yes', 'no', NULL),
(441100, 'Oliver', 'Moore', 'oliver.moore@example.com', '+390217890123', 49, 'entrepreneur', 'married', 'tertiary', 'no', -3058.00, 'no', 'no', NULL),
(80010299, 'Mia', 'Clark', 'mia.clark@example.com', '+390218901234', 32, 'management', 'married', 'tertiary', 'no', 6274.00, 'yes', 'no', NULL),
(70045, 'Lucas', 'Hall', 'lucas.hall@example.com', '+390219012345', 29, 'blue-collar', 'single', 'secondary', 'no', 0.00, 'yes', 'no', NULL),
(991100233, 'Charlotte', 'Lewis', 'charlotte.lewis@example.com', '+390211112233', 18, 'admin.', 'single', 'secondary', 'no', 5683.00, 'no', 'yes', NULL),
(11770001, 'Henry', 'Martin', 'henry.martin@example.com', '+390211223344', 50, 'management', 'married', 'tertiary', 'no', 4654.00, 'no', 'no', NULL),
(33009914, 'Amelia', 'Allen', 'amelia.allen@example.com', '+390211334455', 30, 'admin.', 'married', 'secondary', 'no', 15.00, 'yes', 'no', NULL),
(93012, 'Liam', 'Baker', 'liam.baker@example.com', '+39 345 2219940', 28, 'technician', 'single', 'secondary', 'no', 1210.00, 'yes', 'no', NULL),
(4482910, 'Emma', 'Turner', 'emma.turner@example.com', '+39 331 4401293', 36, 'admin.', 'married', 'secondary', 'no', 520.00, 'no', 'no', NULL),
(712003, 'Noah', 'Ricci', 'noah.ricci@example.com', '+39 392 1184432', 45, 'management', 'single', 'tertiary', 'no', 3370.00, 'yes', 'yes', NULL),
(90211488, 'Ava', 'Conti', 'ava.conti@example.com', '+39 347 9915523', 31, 'blue-collar', 'single', 'secondary', 'no', -150.00, 'no', 'no', NULL),
(550129, 'Oliver', 'Galli', 'oliver.galli@example.com', '+39 348 7621841', 52, 'entrepreneur', 'married', 'tertiary', 'no', 7200.00, 'yes', 'yes', NULL),
(77220014, 'Sophia', 'Moretti', 'sophia.moretti@example.com', '+39 350 1198203', 26, 'admin.', 'single', 'secondary', 'no', 200.00, 'no', 'no', NULL),
(3105592, 'James', 'Ferri', 'james.ferri@example.com', '+39 380 4400288', 39, 'self-employed', 'married', 'secondary', 'no', 2890.00, 'yes', 'no', NULL),
(14882012, 'Mia', 'Lombardi', 'mia.lombardi@example.com', '+39 351 8820032', 34, 'management', 'single', 'tertiary', 'no', 1050.00, 'no', 'no', NULL),
(99214, 'Benjamin', 'Serra', 'benjamin.serra@example.com', '+39 345 9102231', 22, 'student', 'single', 'secondary', 'no', 50.00, 'no', 'no', NULL),
(6400128, 'Isabella', 'Costa', 'isabella.costa@example.com', '+39 333 1192930', 47, 'management', 'married', 'tertiary', 'no', 5980.00, 'yes', 'no', NULL),
(882190, 'Ethan', 'Sartori', 'ethan.sartori@example.com', '+39 320 8811335', 29, 'technician', 'single', 'secondary', 'no', 740.00, 'no', 'no', NULL),
(71290045, 'Charlotte', 'Villa', 'charlotte.villa@example.com', '+39 334 5518823', 51, 'entrepreneur', 'married', 'tertiary', 'no', 4500.00, 'yes', 'yes', NULL),
(5512309, 'Alexander', 'De Luca', 'alex.deluca@example.com', '+39 345 2193844', 33, 'blue-collar', 'married', 'secondary', 'no', -320.00, 'yes', 'no', NULL),
(440912, 'Amelia', 'Gentile', 'amelia.gentile@example.com', '+39 360 2283492', 24, 'admin.', 'single', 'secondary', 'no', 120.00, 'no', 'no', NULL),
(72319902, 'Logan', 'Vitale', 'logan.vitale@example.com', '+39 345 7791230', 42, 'technician', 'married', 'tertiary', 'no', 3125.00, 'yes', 'no', NULL),
(112349, 'Harper', 'Marini', 'harper.marini@example.com', '+39 347 1299930', 37, 'management', 'single', 'tertiary', 'no', 2100.00, 'no', 'no', NULL),
(88012234, 'Lucas', 'Palmieri', 'lucas.palmieri@example.com', '+39 331 8890123', 48, 'self-employed', 'married', 'secondary', 'no', 3980.00, 'yes', 'yes', NULL),
(599012, 'Evelyn', 'Fabbri', 'evelyn.fabbri@example.com', '+39 320 4420193', 41, 'blue-collar', 'married', 'secondary', 'no', 750.00, 'yes', 'no', NULL),
(3401922, 'Mason', 'Neri', 'mason.neri@example.com', '+39 366 2211329', 23, 'student', 'single', 'secondary', 'no', 80.00, 'no', 'no', NULL),
(99881100, 'Ella', 'Riva', 'ella.riva@example.com', '+39 339 2219910', 55, 'entrepreneur', 'married', 'tertiary', 'no', 8120.00, 'yes', 'yes', NULL);
