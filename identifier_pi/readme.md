This folder contains the code files for the Pi that is responsible for running the identification chamber.
It will have 5 camera inputs used for determining which piece is present in the chamber and will control both the section of conveyor in the chamber and the conveyor that leads to the pick and place machine which places the parts in the appropriate bins.
It will also be where the control screen is located and will be the main brain of the operations.

The screen will both display static information and statistics about the current processing as well as giving the operator several configuration options to enable fine tuning.

Screen Info:
- Configuration of Pick and Place Bins
- Part Sorting Rate
- Rate of discard for resorting
- Current Camera Views

Screen Options:
- Confirm Current Part Selection
- Verification Mode
    - Expect one particular type of part and just check they all agree + Count number of parts
- Start Sorting
- Input Bins (Auto + Manual)