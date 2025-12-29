This is the root repo for my lego sorter project. It contains both information about the different Raspberry Pis that are necessary and the hardware that is necessary to construct the physical structure.

### Pis
Each folder corresponds to a specific raspberry pi that is part of the system and contains it's own readme to explain its specific functions in more detail.

#### Identifier
- This pi is responsible for managing the identification chamber - controlling the input and output of bricks to it and outputting the brick type to the pick and place pi

#### Pick and Place
- This pi is responsible for moving the bricks from the output of the identification chamber to their specific sorted containers or to the discard for resorting with different containers.

#### Colour Determination
- This pi is responsible for determining the colour of parts before they enter the identifier chamber. This is used to aid the Pick and Place machine in sorting as the identification process doesn't care about part colour


### Structure
The physical structure is composed of several parts:
- The Colour Determination Location
- The part identifier
- Pick and Place Sorter
- Straight Belt
- Turn Belt
- Part Separator

#### Pick and Place
- NEMA 17 Steppers
- DRV2588 Driver Chip