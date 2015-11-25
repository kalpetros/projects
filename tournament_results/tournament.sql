-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Initial commands
-- Connect to database
\c tournament;
-- Drop tables if they exist
-- Drop players table
--DROP TABLE IF EXISTS players CASCADE;
-- Drop matches table
--DROP TABLE IF EXISTS matches CASCADE;

-- Tables (players, matches)
-- Create table players (id, player)
CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	name TEXT
);

-- Create table matches (id, winner, loser)
CREATE TABLE matches (
	id SERIAL PRIMARY KEY,
	winner INTEGER references players(id),
	loser INTEGER references players(id)
);

-- Create view wins (id, player, wins)
CREATE VIEW wins AS
	SELECT players.id, players.name,
	COUNT(winner) as wins FROM players LEFT JOIN matches
	ON players.id = matches.winner
	GROUP BY players.id
	ORDER BY wins DESC;

-- Create view loses (id, player, loses)
CREATE VIEW loses AS
	SELECT players.id, players.name,
	COUNT(loser) as loses FROM players LEFT JOIN matches
	ON players.id = matches.loser
	GROUP BY players.id
	ORDER BY loses DESC;

-- Create view standings (id, player, wins, matches)
CREATE VIEW standings AS
	SELECT players.id, players.name, wins, loses, wins+loses as matches
	FROM players LEFT JOIN wins
	ON players.id = wins.id
	LEFT JOIN loses
	ON players.id = loses.id
	ORDER BY players.id ASC;

-- Tests
--INSERT INTO players (name) VALUES ('Petros'); --1
--INSERT INTO players (name) VALUES ('Manos'); --2
--INSERT INTO players (name) VALUES ('Antonis'); --3
--INSERT INTO players (name) VALUES ('John'); --4
--INSERT INTO players (name) VALUES ('Michael'); --5
--INSERT INTO players (name) VALUES ('Brad'); --6
--INSERT INTO players (name) VALUES ('Joseph'); --7
--INSERT INTO players (name) VALUES ('Will'); --8

--INSERT INTO matches (winner,loser) VALUES (1,2);
--INSERT INTO matches (winner,loser) VALUES (3,4);
--INSERT INTO matches (winner,loser) VALUES (6,7);
--INSERT INTO matches (winner,loser) VALUES (1,5);
--INSERT INTO matches (winner,loser) VALUES (2,1);
--INSERT INTO matches (winner,loser) VALUES (3,1);

SELECT * FROM players;
SELECT * FROM matches;
SELECT * FROM wins;
SELECT * FROM loses;
SELECT * FROM standings;