-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drop database if it exists
DROP DATABASE IF EXISTS tournament;
-- Create the database
CREATE DATABASE tournament;
-- Connect to the tournament database
\c tournament;

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

-- Create table tournament (id1, name1, id2, name2)
CREATE TABLE tournament (
	id1 INTEGER,
	name1 TEXT,
	id2 INTEGER,
	name2 TEXT
);

-- Create view wins (id, player, wins)
CREATE VIEW wins AS
	SELECT players.id, players.name,
	COUNT(winner) as wins FROM players LEFT JOIN matches
	ON players.id = matches.winner
	GROUP BY players.id;

-- Create view loses (id, player, loses)
CREATE VIEW losses AS
	SELECT players.id, players.name,
	COUNT(loser) as losses FROM players LEFT JOIN matches
	ON players.id = matches.loser
	GROUP BY players.id;

-- Create view standings (id, player, wins, matches)
CREATE VIEW standings AS
	SELECT players.id, players.name, wins, wins+losses as matches
	FROM players LEFT JOIN wins
	ON players.id = wins.id
	LEFT JOIN losses
	ON players.id = losses.id
	ORDER BY wins DESC;
