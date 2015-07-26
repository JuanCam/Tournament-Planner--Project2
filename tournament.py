#!/usr/bin/env python
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
    c.execute("DELETE FROM Matches")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM Players")
    DB.commit()
    DB.close()


def deleteTournaments():
    """Remove all tournaments"""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM Tournaments")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(idPlayer) AS NumberOfPlayers FROM Players")
    for row in c.fetchall():
        number_of_players = row[0]
    DB.commit()
    DB.close()
    return number_of_players


def registerPlayer(name, last_name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    #Inserts a player into the data base with its Name
    c.execute("INSERT INTO Players(Name) " +
              "VALUES (%s)", (name, ))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a 
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """ 
    DB = connect()
    c = DB.cursor()
    standings = []
    c.execute("SELECT PlayerMatchPl.idPlayer,PlayerMatchPl.Name,PlayerMatchPl.Wins,PlayerMatchPl.Lost FROM PlayerMatchPl ORDER BY Wins DESC")
    #Reports the wins and matches played by player
    #by using the PlayerMatchPl view which contains the
    #the name, id, number of wins and nomber of lost of
    #each player.
    for row in c.fetchall():
        total = int(row[2])+int(row[3])
        standings.append((str(row[0]), row[1], int(row[2]), total))

    DB.commit()
    DB.close()

    return standings


def reportMatch(winner, loser, tournament):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    #Inserts a match between two players, its always mandatory a
    #winner and a loser. Also the idof the tournament is requiered
    c.execute("INSERT into Matches (idWinner,idLoser,idTournament)"+
              " VALUES (%s,%s,%s)",(winner, loser, tournament,))
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
    single_match = []
    match_list = []
    m = 0;
    #Select a list of all players and sorting them by their win games.
    c.execute('SELECT * FROM PlayerWins ORDER BY Wins DESC')
    #Create pairs and insert them into the list.
    for row in c.fetchall():
        single_match.append(str(row[0]))
        single_match.append(row[1])
        if (m>=1):
            match_list.append(tuple(single_match))
            single_match = []
        m = (m + 1) % 2
    return match_list
    DB.commit()
    DB.close()


def createTournament(name):
    """Creates tournaments for supporting new tournaments
       Args:
         name - Is a string of the tournament name
       Returns:
       Boolean true if tournament was instered succesfully or false if not.
    """
    DB = connect()
    c = DB.cursor()
    #Inserts tournament into the tournaments table
    c.execute("INSERT INTO Tournaments (TournamentName) VALUES (%s)",(name ,))
    DB.commit()
    DB.close()


def selectTorunament(name):
    """Selects a tournament by its name
       Args:
         name - Is a string of the tournament name
       Returns:
       a list of tuples in which each tuple contains:
       id: id number of the tournament
       name: tournament name
    """
    tournament_info = []
    DB = connect()
    c = DB.cursor()
    #Selects tournaments by its name
    c.execute("SELECT idTournament,TournamentName FROM Tournaments WHERE TournamentName LIKE '%name%'")
    for row in c.fetchall():
        tournament_info.append((row[0], row[1]))
    return tournament_info
    DB.commit()
    DB.close()
