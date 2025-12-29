from enum import Enum

from gpiozero import Button
from RpiMotorLib.RpiMotorLib import A4988Nema


class StepSize(Enum):
    FULL = 1
    HALF = 2
    QUARTER = 3
    EIGHTH = 4
    SIXTEENTH = 5
    THIRTY_SECOND = 6

    def steps(self) -> int:
        all_steps = [200, 400, 800, 1600, 3200, 6400]
        return all_steps[self.value]


    def sizes(self) -> str:
        all_sizes = ["Full", "Half", "1/4", "1/8", "1/16", "1/32"]
        return all_sizes[self.value]

class MotorDirection(Enum):
    CLOCKWISE = True
    CW = True
    COUNTERCLOCKWISE = False
    CCW = False

    def flip(self):
        if self == MotorDirection.CLOCKWISE:
            return MotorDirection.CCW
        else:
            return MotorDirection.CLOCKWISE


class PlotterMotor:
    def __init__(self, direction_pin : int, step_pin: int, mode_pins :tuple[int,int,int], track_length:float, distance_per_revolution: float, home_direction: MotorDirection, home_limit_pin: int, end_limit_pin: int) -> None:

        self.motor = A4988Nema(direction_pin, step_pin, mode_pins, "DRV8825")

        self.home_limit_check = Button(home_limit_pin)
        self.home_limit_check.when_activated = self.stop

        self.end_limit_check = Button(end_limit_pin)
        self.end_limit_check.when_activated = self.stop

        self.home_direction = home_direction
        self.track_length = track_length
        self.dpr = distance_per_revolution

        self.position = float(0)
        self.moveable = True
        self.homing = True

        self.home()

    def to_steps(self, distance:float, step_size:StepSize) -> int:
            revolutions = distance / self.dpr
            steps = round(revolutions * step_size.steps())
            return steps

    def move(self, direction:MotorDirection, distance:float):
        while self.moveable:
            if distance > (0.75 * self.track_length):
                move_distance = 0.9 * distance
                step_size = StepSize.FULL
                steps = self.to_steps(move_distance, step_size)
                self.motor.motor_go(direction.value, step_size.sizes(), steps)
                distance -= move_distance
            elif distance > (0.5 * self.track_length):
                move_distance = 0.9 * distance
                step_size = StepSize.HALF
                steps = self.to_steps(move_distance, step_size)
                self.motor.motor_go(direction.value, step_size.sizes(), steps)
                distance -= move_distance
            elif distance > (0.25 * self.track_length):
                move_distance = 0.9 * distance
                step_size = StepSize.QUARTER
                steps = self.to_steps(move_distance, step_size)
                self.motor.motor_go(direction.value, step_size.sizes(), steps)
                distance -= move_distance
            elif distance > (0.1 * self.track_length):
                move_distance = 0.9 * distance
                step_size = StepSize.EIGHTH
                steps = self.to_steps(move_distance, step_size)
                self.motor.motor_go(direction.value, step_size.sizes(), steps)
                distance -= move_distance
            else:
                move_distance = distance
                step_size = StepSize.SIXTEENTH
                steps = self.to_steps(move_distance, step_size)
                self.motor.motor_go(direction.value, step_size.sizes(), steps)
                distance -= move_distance

        self.moveable = True


    def goto(self, position:float):
        if position > self.position:
            #Need to move further away from home position
            direction = self.home_direction.flip()
            distance = position - self.position
        elif position < self.position:
            #Need to move closer to home position
            direction = self.home_direction
            distance = self.position - position
        else:
            return
        self.move(direction, distance)

    def home(self) -> None:
        self.move(self.home_direction, self.track_length)
        self.move(self.home_direction.flip(), (0.1*self.track_length))

    def stop(self, device : Button): #device is automatically made the first augment when using the callback of the button class. It is the device itself
        self.motor.motor_stop()
        self.moveable = False #Causes the Loop in self.move to terminate thus stopping any more motor moves being triggered
        if device.pin == self.home_limit_check.pin:
            self.position = 0
            self.homing = False
        elif device.pin == self.end_limit_check.pin:
            self.position = self.track_length
        elif not(self.homing):
            #If limit sensor erroneously triggered home the device, if already homing then raise exception
            self.homing = True
            self.home()
        else:
            #TODO Custom Exception
            raise Exception

if __name__ == "__main__":

    direction_pin = 4
    step_pin = 5
    mode_pins = (6,7,8)
    home_limit_pin = 15
    end_limit_pin = 16

    trackless_test_motor = PlotterMotor(direction_pin, step_pin, mode_pins, 100, 10, MotorDirection.CW, home_limit_pin, end_limit_pin)
