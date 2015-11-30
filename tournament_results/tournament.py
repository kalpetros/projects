#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches")
    DB.commit() 
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players")
    DB.commit()
    DB.close()

def deleteTournament():
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM tournament")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT count(*) FROM players")
    rows = c.fetchone()
    DB.close()
    return rows[0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    DB.commit()
    DB.close()

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
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT id, name, wins, matches FROM standings")
    rows = c.fetchall()
    DB.close()
    return rows

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO matches (winner,loser) VALUES (%s,%s)", (winner,loser,))
    DB.commit()
    DB.close()

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
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * FROM standings")
    rows = c.fetchall()
    pairings = []
    i = 0
    rowslength = len(rows)
    while i < rowslength:
    	pid1 = rows[i][0]
    	pname1 = rows[i][1]
    	pid2 = rows[i+1][0]
    	pname2 = rows[i+1][1]
    	pairings.append((pid1, pname1, pid2, pname2))
    	i = i + 2
    DB.close()
    return pairings

def checkRematches():
    """Checks if two players have already played against each other
    Args:
        player1: the id number of first player to check
        player2: the id number of second player to check
    Return false if players have already played against each other, true if not
    """
    matches = swissPairings()
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT winner+loser as sum FROM matches")
    rows = c.fetchall()
    i = 0
    for row in rows:
        if row[0] != matches[i][0]+matches[i][2]:
            c.execute("INSERT INTO tournament VALUES (%s,%s,%s,%s)", (matches[i][0],matches[i][1],matches[i][2],matches[i][3],))
            DB.commit()
        else:
            return False
        i = i + 1
    DB.close()
