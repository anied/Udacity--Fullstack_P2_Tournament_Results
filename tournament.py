#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def clean(dirty_string):
    """Shorthand to use bleach to clean out any HTML tags.  Eventually API should invoke an error and UI should, if possible, attempt to apply the same rules."""
    return bleach.clean(dirty_string, strip=True)


def db_execute(sql_command, additional_argument=None):
    """Helper function to make a command to the DB-- avoids a lot of duplicate code."""
    db = connect()
    c = db.cursor()

    # Only attempt to pass in an additional argument if one is included in the call
    if additional_argument:
        c.execute(sql_command, additional_argument)
    else:
        c.execute(sql_command)

    db.commit()

    c.close()
    db.close()


def db_execute_and_fetch(sql_command, additional_argument=None):
    """Helper function to make a command to the DB-- avoids a lot of duplicate code."""
    db = connect()
    c = db.cursor()

    # Only attempt to pass in an additional argument if one is included in the call
    if additional_argument:
        c.execute(sql_command, additional_argument)
    else:
        c.execute(sql_command)

    data_return = c.fetchall()

    db.commit()

    c.close()
    db.close()

    return data_return


def deleteMatches():
    """Remove all the match records from the database."""

    command = "DELETE FROM tournaments *;"

    db_execute(command)


def addToTournament(p_id):
    """Helper function to registerPlayer to add a newly registered player to the tournament (used to avoid needing to write 'upsert' functionality)"""
    command = "INSERT INTO tournaments (player_id) VALUES (%s)"

    db_execute(command, p_id)


def deletePlayers():
    """Remove all the player records from the database."""

    # Call delete matches first, as they share a reference on primary key
    deleteMatches()

    command = "DELETE FROM players *;"

    db_execute(command)


def countPlayers():
    """Returns the number of players currently registered."""

    command = "SELECT count(player_id) FROM players;"

    count = (db_execute_and_fetch(command))[0][0]

    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    command = "INSERT INTO players (player_username) VALUES (%s) RETURNING player_id;"

    # newly issued player_id serial will be returned due to RETURNING statement in command
    player_id = (db_execute_and_fetch(command, (clean(name),)))[0]

    # Call to a helper fun to add the new player to the tournament, avoiding need to implement an 'upsert' elsewhere
    addToTournament(player_id)


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    command = """SELECT players.player_id, player_username, COALESCE(score, 0) AS score, COALESCE(matches, 0) AS matches
                    FROM players
                    LEFT JOIN tournaments
                    ON players.player_id = tournaments.player_id
                    ORDER BY tournaments.score;"""

    player_standings = db_execute_and_fetch(command)

    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    # We don't use the helper function db_execute here because we want to bundle these two commands in a transaction (BEGIN/COMMIT)
    db = connect()
    c = db.cursor()

    increment_winner = """UPDATE tournaments
                            SET score = COALESCE(score, 0) + 1, matches = COALESCE(matches, 0) + 1
                            WHERE player_id = %s;"""

    increment_loser = """UPDATE tournaments
                            SET matches = COALESCE(matches, 0) + 1
                            WHERE player_id = %s;"""

    c.execute('BEGIN;')

    c.execute(increment_winner, (winner,))
    c.execute(increment_loser, (loser,))

    c.execute('COMMIT;')

    c.close()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    # Fetch players from playerStandings (already sorted)
    players = playerStandings()

    # Instantiate empty list to hold pairings
    pairings = []

    # Iterate over every two returned players, bundle them into a tuple and append them to the pairings list
    for x in xrange(0, (len(players)/2)):
        i = x*2
        pair = (players[i][0], players[i][1], players[i+1][0], players[i+1][1])
        pairings.append(pair)

    # Return the pairings list
    return pairings
