CREATE DATABASE IF NOT EXISTS mainddbb;
CREATE USER IF NOT EXISTS 'mainddbbuser'@'%' IDENTIFIED BY 'Reality is the core of percepti0n';
GRANT ALL PRIVILEGES ON mainddbb.* TO 'mainddbbuser'@'%';
FLUSH PRIVILEGES;
