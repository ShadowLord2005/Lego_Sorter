This is the root repo for my lego sorter project. Each folder corresponds to a specific raspberry pi that is part of the system and contains it's own readme to explain its specific functions in more detail.

#### Identifier
- This pi is responsible for managing the identification chamber - controlling the input and output of bricks to it and outputting the brick type to the pick and place pi

#### Pick and Place
- This pi is responsible for moving the bricks from the output of the identification chamber to their specific sorted containers or to the discard for resorting with different containers.

#### Colour Determination
- This pi is responsible for determining the colour of parts before they enter the identifier chamber. This is used to aid the Pick and Place machine in sorting as the identification process doesn't care about part colour