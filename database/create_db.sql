-- CREATE TABLE Subscription
-- (
--     id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--     is_active   BOOLEAN,
--     duration    VARCHAR(100),
--     start       DATE,
--     `end`       DATE
-- );

CREATE TABLE Category
(
    id   INTEGER     NOT NULL PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE Recipe
(
    id          INTEGER      NOT NULL PRIMARY KEY AUTOINCREMENT,
    name        VARCHAR(60)  NOT NULL,
    url         VARCHAR(120) NOT NULL UNIQUE,
    rating      REAL,

    category_id INT          NOT NULL,

    FOREIGN KEY (category_id) REFERENCES Category (id) ON DELETE CASCADE
);

CREATE TABLE User
(
    id                   INTEGER      NOT NULL PRIMARY KEY AUTOINCREMENT,
    name                 VARCHAR(60)  NULL,
    telegram_id          VARCHAR(60)  NOT NULL UNIQUE,

    favourite_recipes_id INT          NOT NULL,
    published_recipes_id INT          NOT NULL,

    FOREIGN KEY (favourite_recipes_id) REFERENCES Recipe  (id) ON DELETE CASCADE,
    FOREIGN KEY (published_recipes_id) REFERENCES Recipe  (id) ON DELETE CASCADE,
);
