CREATE DATABASE IF NOT EXISTS proyecto2;

CREATE TABLE IF NOT EXISTS users(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(40) NOT NULL,
    password_hash VARCHAR(40) NOT NULL,
    isAdmin TINYINT DEFAULT 0

);

INSERT INTO users username, password_hash, isAdmin VALUES 'admin',
'a21531094c7a6c8c89eb9d1e087393996e3ae2ae81ce24646435312ca335c1225be90de216299102fcf5490ecb6ebb7419c6fd8f091c0ba70190ecccd4d74bb8', 1;
INSERT INTO users username, password_hash, isAdmin VALUES 'ejemplo',
'a21531094c7a6c8c89eb9d1e087393996e3ae2ae81ce24646435312ca335c1225be90de216299102fcf5490ecb6ebb7419c6fd8f091c0ba70190ecccd4d74bb8', 0;

--CREATE TABLE IF NOT EXISTS models(
--    model_id INT AUTO_INCREMENT PRIMARY KEY,
--    filename VARCHAR(40) NOT NULL,
--    object_key VARCHAR(2083) NOT NULL
--);


