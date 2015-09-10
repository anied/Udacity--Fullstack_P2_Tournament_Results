# Udacity Fullstack P2: Tournament Results
## Introduction
The code in this repository fulfills the requirements set out for _Project #2: Tournament Results_ for the **Udacity Fullstack Nanodegree**.
## How To Run
### Preliminary Setup
The instructions to run this code assumes that you already have the vagrant box specifically configured for the _Relational Databases_ course installed and up on your machine, and the code repo for the class is also configured properly.

To start, copy the files from this repo (excluding `readme.md`) into the `vagrant/tournament` directory in the DB course Github repo.  _tournament_test.py_ is included for your convenience.

In the terminal, `vagrant ssh` into the vagrant box, use `cd /vagrant` to access the filesystem, then navigate to the appropriate directory with `cd tournament`.

From here, you can type `psql` to access the Postgres CLI.  This solution to the P2 task utilizes a database called _tournament_ with two tables: _players_ and _tournaments_.  If you don't already have a _tournament_ DB, create it in the PSQL CLI with the `CREATE DATABASE` command (documentation [here](http://www.postgresql.org/docs/9.4/static/sql-createdatabase.html)).

If you already have this DB up and it already contain any tables named `players` or `tournaments`, make sure to remove them before proceeding:

```PLpgSQL
DROP TABLE players;
DROP TABLE tournaments;
```
### Running the Code

If you followed the steps in the section above, you should be connected to 
the vagrant box via SSH, the current directory should be `tournament` and you should be connected to the PSQL CLI with a DB called _tournament_ created and containing no tables.

Now connect to the DB with the PSQL CLI command `\c tournament`.  Once connected, run the command `\i tournament.sql` to create the necessary tables for this project.

Once the tables are created, you can exit the PSQL CLI (but leave the terminal active).  From here, run the test script with the command `python tournament_test.py`.  This should execute with all tests passing- showing that the code has properly met the requirements as set forth by the project description.