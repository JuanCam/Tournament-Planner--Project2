-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
-- POSTGRESQL Tables for a database swiss tournament
-- By Juan Camilo Gutierrez

--drop database tournament;
--create database tournament;

drop view PlayerMatchPl,PlayerWins,PlayerLost;
drop table Players,Tournaments,Matches;
drop sequence idPlayerSeq,idTournament,idMatch;



create table Players (
	idPlayer int PRIMARY KEY,
	Name varchar(255)
	--LastName varchar(255)
);
create table Tournaments(
	idTournament int PRIMARY KEY,
	TournamentName varchar(255)
	--WinnerName varchar(255),
	--idWinner int, 
	--FOREIGN KEY(idWinner) REFERENCES Players(idPlayer)
);
create table Matches (
	idMatch int PRIMARY KEY,
	idWinner int,
	idLoser int,
	idTournament int,
	FOREIGN KEY (idWinner) REFERENCES Players(idPlayer),
    FOREIGN KEY (idLoser) REFERENCES Players(idPlayer),
    FOREIGN KEY (idTournament) REFERENCES Tournaments(idTournament)
);
create view PlayerWins AS SELECT Players.idPlayer, Players.Name, COUNT(Matches.idWinner) AS Wins FROM Players LEFT JOIN Matches ON Players.idPlayer=Matches.idWinner GROUP BY Players.idPlayer, Players.Name ORDER BY Wins DESC;
create view PlayerLost AS SELECT Players.idPlayer, Players.Name, COUNT(Matches.idLoser) AS Lost FROM Players LEFT JOIN Matches ON Players.idPlayer=Matches.idLoser GROUP BY Players.idPlayer, Players.Name ORDER BY Lost DESC;
create view PlayerMatchPl AS SELECT PlayerWins.idPlayer, PlayerWins.Name, PlayerWins.Wins, PlayerLost.Lost FROM PlayerWins LEFT JOIN PlayerLost ON PlayerWins.idPlayer = PlayerLost.idPlayer GROUP BY PlayerWins.idPlayer,PlayerWins.Name,PlayerWins.Wins, PlayerLost.Lost;


create sequence idPlayerSeq owned by Players.idPlayer;
create sequence idTournamentSeq owned by Tournaments.idTournament;
create sequence idMatch owned by Matches.idMatch;

ALTER TABLE Players ALTER COLUMN idPlayer SET default nextval('idPlayerSeq');
ALTER TABLE Tournaments ALTER COLUMN idTournament SET default nextval('idTournamentSeq');
ALTER TABLE Matches ALTER COLUMN idMatch SET default nextval('idMatch');
