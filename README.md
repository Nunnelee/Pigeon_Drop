# Pigeon_Drop
A 2D game created with Pygame

The main program is pigeon_drop.py that accesses all of the other programs and images within the same storage file.

To stop the game at any point, press 'q' for quit.

Project Plan
1. Examine our code and determine if there is a need to refactor before implementing new features.
2. Add a single auto to the bottom corner of the screen with appropiate spacing around it.
3. Use the spacing around the first auto and the overall screen size to determine how many autos can fit on the screen. Write a loop to create autos to fill the lower portion of the screen.
4. Make the fleet move sideways and up until the entire fleet is shot down, an auto hits the pigeon, or an auto reaches the top. If the entire fleet is shot sown, we'll create a new fleet. If an auto hits the pigeon or the top, we'll destroy the pigeon and create a new fleet.
5. Limit the number of pigeons the player can use, and end the game when the player has used up the alloted pigeons.
