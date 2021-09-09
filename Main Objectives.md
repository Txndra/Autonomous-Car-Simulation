1.	Designing a display menu
1.1	Display option to design a map
1.2	Display option to add/remove obstacles from maps
1.3	Display option to run simulation
1.4	Quit program

2.	Creating a user-designed track
2.1	Allow user to design shape of map
2.2	Allow user to place obstacles
2.3	Allow user to undo/redo actions
2.4	Allow user to select start and end locations

3	Allowing user to save map
3.1	Should save map to a local file
3.2	Should allow users to name file

4	Creating a neural network
4.1	Network should be able to detect wall boundaries with 5 sensors
4.2	Distance from wall edges will be considered as inputs to each starting neuron
4.3	Outer layers of neural network should be commands to turn left, turn right, slow down or speed up
4.4	Outputs of input neurons will determine which command will be executed
	
5.	Cars should run around the chosen track as quick as possible without crashing
5.1	Cars that move the furthest gain a higher fitness
5.2	Cars that move the fastest gain a higher fitness
5.3	Higher fitness cars regenerate in the next generation

6.	Allowing user to run car simulation
6.1	Neural networks should trigger commands turn left, right, speed up or slow down
6.2	50 cars per generation running at once
6.3	Algorithm senses when the edge of a track is hit by a car
6.3.1	This car will die and be deleted
6.4	Algorithm selects 3 cars with the highest fitness and regenerates them when cars die
6.5	Algorithm runs until a car makes it through the track

7.	Display stats interface
7.1	Display number of generations
7.2	Display cars left for each generation
7.3	Display generation number

8.	Allowing user to quit
8.1	Exits the program when option is selected.
