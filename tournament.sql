-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- Create the "players" table
CREATE TABLE players(
	player_id serial PRIMARY KEY,
	player_username varchar(16)
);

-- Create the "tournaments" table
CREATE TABLE tournaments(
	player_id int REFERENCES players (player_id),
	score int,
	matches int,
	PRIMARY KEY (player_id)
);