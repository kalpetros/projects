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
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches CASCADE;
DROP VIEW IF EXISTS standings CASCADE;

-- Tables (players, matches)
CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	player TEXT
);

CREATE TABLE matches (
	id SERIAL PRIMARY KEY,
	winner INTEGER references players(id),
	loser INTEGER references players(id)
);

CREATE VIEW standings AS
	SELECT a.id, a.player,
		(SELECT COUNT(winner) FROM matches GROUP BY id) as wins,
		(SELECT COUNT (winner) + COUNT (loser) FROM matches GROUP BY id) as matches
		FROM players as a LEFT JOIN matches as b
		ON a.id = b.winner
		ORDER BY wins DESC;