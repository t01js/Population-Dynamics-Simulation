## Simulation of Population Dynamics

### Overview
This Python program simulates a population of agents searching for food in a 2D space. The agents, represented by arrows, move randomly until they detect food within a certain range. When food is detected, the agents move towards it and consume it, replenishing their energy. The simulation continues until all agents have died due to lack of energy.

### Configuration
The following parameters can be configured to modify the behavior of the simulation:
- **WIDTH** and **HEIGHT**: dimensions of the 2D space.
- **NUM_FLECHAS**: number of agents.
- **NUM_COMIDA**: number of food items.
- **ENERGIA_INICIAL**: initial energy level of agents.
- **ENERGIA_GASTO_MIN** and **ENERGIA_GASTO_MAX**: minimum and maximum energy consumption rate of agents.
- **VELOCIDAD_MIN** and **VELOCIDAD_MAX**: minimum and maximum speed of agents.
- **RANGO_VISION_MIN** and **RANGO_VISION_MAX**: minimum and maximum range of vision of agents.
- **TAMANO_MIN** and **TAMANO_MAX**: minimum and maximum size of agents.

### How it works
The simulation uses the Pygame library to create a window and handle user input. The `Flecha` class represents agents and contains attributes such as position, speed, and energy level. The `Comida` class represents food items and contains position information. The `mover()` method of the `Flecha` class is responsible for determining the next movement of the agent based on the location of nearby food items and the agent's energy level. The `dibujar()` method of both classes is responsible for drawing the agents and food items on the screen.

### Running the program
To run the simulation, ensure that Pygame is installed and run the `main()` function. The simulation can be terminated by closing the window or when all agents have died.
