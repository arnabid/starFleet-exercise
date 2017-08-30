Starfleet Mine Clearing Exercise

----------------------------------------------------------------------------------------------------------------------------------------

Steps to build :

1) Clone the repository

2) Open command prompt and cd to the local repository location

3) Run command: python starFleet.py tests/test1.field tests/field1.script

----------------------------------------------------------------------------------------------------------------------------------------

Brief Overview:

The program maintains a set of active mines in the cuboid, the current x,y,z co-ordinates of the ship, number of moves and volleys fired during the simulation run. It also maintains a boolean array of location of mines at different depths and the index of the mine at the highest depth in the cuboid. This makes it possible to check if the ship has "passed" a mine in constant time.

The program has the following methods:

1) parseGrid - parses the field file and builds the collection of mines

2) parseScript - parses the script file and builds the list of steps for the simulation run

3) displayGrid - displays the current state of the mine grid before and after each step in the simulation

4) different firing pattern methods - removes the mines destroyed from the collection and updates the location of mines

5) navigate - executes each line of command in the script file

6) main - carries out the simulation run while certain conditions hold

6) score - calculates the score of a simulation run according to rules in the problem statement
