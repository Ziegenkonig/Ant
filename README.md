# Ant
I just had an intense craving one day to program some ants and here we are. There's no real end-goal here, I'm doing this purely for fun and learning. It's taught me a lot about Python's OOP practices as well as OOP practices in general. These ants are my children

This program is riddled with bugs. (Ehehe,  not really, just an ant pun)

Stuff that's done:

1) Create single dot on canvas
2) Have dot wander aimlessly
3) Have many dots wander aimlessly
4) Create Ant class for OO approach
5) Create Fruit class
6) Have ants move to fruit, all at once
7) Teach ants to recognize collision with fruit
8) Give Ants a home, as a class
9) When ants find food, they take some home
10) When they take some home, any ant they collide with learns about food
11) Ants who learn about the food go get the food
12) Food as FP that gets diminished every time it's harvested, home has a Food counter
13) Add Tunnel counter to home
14) If ant is idle and > 10 food in home, ant makes a tunnel (this takes time)
15) Should make an Ant Swarm class (done)
16) Give Fruit another rect that is roughly 3x bigger than it's hitbox; this is it's Smell Box
17) More tunnels = more ant
18) Forager ants; subclass to Ant, has it's own Scent Box (different than Smell Box) that expands radius for finding food
19) When ant carries food, a new object called Food Bit is created
20) Food Bit is centered on the ant to simulate being carried. Need a check for being carried maybe
21) Have ant take a few seconds to harvest
22) Have non-forager ants wander, but prevent from getting too far from home
23) Tweak so only foragers can communicate food whereabouts
24) Implement Scent Trails (Pheremone System) somehow

    24.a) Non-forager ants leave territory scent markers periodically
    
    24.b) All Scents decay at different rates, as follows: (Shortest) Food Trail --> Territory --> Explored (Longest)
    
    24.c) Forager Ants leave Explored Scent markers while not actively gathering food
    
    24.d) Tweak Scents so that they generate in a random spot around the ant, not right on top of ant
    
    24.e) Explored Scent: If Explored Scent exists in scent_box, don't place a new one
    
    24.f) All ants leave food trail scents while delivering food and traveling to food
    
25) Implement path-finding algorithm (A*) for forager ants, who can share the path that's generated with others

    25.a) Using the Explored Scents as a map of nodes, use A* to find the shortest route back home
    
    25.b) Connect each Explored Scent to it's neighbors via a specific radius (This was not easy)
    
    25.c) Trigger algorithm that builds path when Forager initially finds food
    
    25.d) Make goal node hardcoded at home
    
    25.e) Make start node hardcoded at the food source
    
    25.f) Make Hunt() exclusive to Foragers, have the algorithm trigger there
    
    25.g) Create new Ant method for traveling along the path, backwards and forwards
    
    25.h) Ensure A* only runs once per food source, even if another Forager finds the source

