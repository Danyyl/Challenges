DIRECTION_DOWN, DIRECTION_NONE, DIRECTION_UP = -1, 0, 1


class HardwareElevator:
    """This is the hardware elevator (engine) which provides an interface
    for the main business logic programmed in Elevator.
    This class cannot and MUST NOT be changed.
    """

    def move_up(self):
        self.current_direction = DIRECTION_UP

    def move_down(self):
        self.current_direction = DIRECTION_DOWN

    def stop_and_open_doors(self):
        self.current_direction = DIRECTION_NONE

    def set_doors_closed_callback(self, callback):
        """Set a function to be called when the doors automatically close.
        """
        pass

    def set_before_floor_callback(self, callback):
        """Set a function to be called when the elevator is about to arrive
        to a floor.
        NOTE: self.get_current_floor() will return at this moment not the
        floor the elevator is about to arrive to.
        """
        pass

    def set_floor_button_callback(self, callback):
        """Set a function to be called when someone presses a button on a floor.
        The callback is passed the floor number and the desired direction.
        """
        pass

    def set_cabin_button_callback(self, callback):
        """Set a function to be called when someone presses a button inside the
        cabin.
        The callback is passed the desired floor number.
        """
        pass

    def get_current_floor(self):
        return self.current_floor

    def get_current_direction(self):
        """Return the direction in which the elevator is currently moving.
        When the elevator is stopped on a floor, the direction is None.
        """
        return self.current_direction


class Elevator:

    def __init__(self, floors):
        self.floors = floors
        self.opened_door = False
        self.outside_cabin = {i + 1: 0 for i in range(floors)}
        self.inside_cabin = {i + 1: 0 for i in range(floors)}
        self.global_direction = DIRECTION_NONE
        self.elevator = HardwareElevator()
        self.elevator.current_direction = DIRECTION_NONE
        self.elevator.current_floor = 1
        self.elevator.set_doors_closed_callback(self.on_doors_closed)
        self.elevator.set_before_floor_callback(self.on_before_floor)
        self.elevator.set_floor_button_callback(self.on_floor_button_pressed)
        self.elevator.set_cabin_button_callback(self.on_cabin_button_pressed)
        self.move = {1: self.elevator.move_up, -1: self.elevator.move_down}

    def __iter__(self):
        return self

    def __next__(self):
        # Emulation of working elevator with iterator
        if self.elevator.get_current_direction() == DIRECTION_NONE:
            if self.opened_door:
                self.on_doors_closed()
            else:
                print("Waiting")
            return
        self.on_before_floor()

    def set_global_direction(self, floor):
        current_floor = self.elevator.get_current_floor()
        if floor > current_floor:
            self.global_direction = DIRECTION_UP
            self.elevator.move_up()
        else:
            self.global_direction = DIRECTION_DOWN
            self.elevator.move_down()

    def check_floors_for_direction(self, reverse=False):
        # Check if have active buttons on floors on current direction
        direction = self.global_direction
        if reverse:
            direction = 1 if direction == -1 else -1
        floors = range(1, self.elevator.get_current_floor()) if direction == -1 \
            else range(self.elevator.get_current_floor() + 1, self.floors + 1)
        for floor in floors:
            if self.inside_cabin[floor] or self.outside_cabin[floor]:
                return True
        return False

    def on_doors_closed(self):
        """This callback is called when the doors automatically close"""
        print(f"Door closed on {self.elevator.get_current_floor()} floor")
        if self.check_floors_for_direction():
            self.move[self.global_direction]()
        elif self.check_floors_for_direction(reverse=True):
            reverse_direction = 1 if self.global_direction == -1 else -1
            self.move[reverse_direction]()
        self.opened_door = False

    def on_before_floor(self):
        """This callback is called when the elevator is about to arrive
        to a floor."""
        print(f"On before floor {self.elevator.get_current_floor() + self.elevator.get_current_direction()} floor")
        next_floor = self.elevator.get_current_floor() + self.elevator.get_current_direction()
        # If inside cabin pressed button with next floor, we will stop
        if self.inside_cabin[next_floor]:
            self.elevator.stop_and_open_doors()
            self.inside_cabin[next_floor] = 0
            self.opened_door = True
        # If elevator goes up and on next floor pressed button up, we will stop
        if self.global_direction == 1 and self.outside_cabin[next_floor] in [1, 2]:
            self.elevator.stop_and_open_doors()
            self.outside_cabin[next_floor] = 0 if self.outside_cabin[next_floor] == 1 else -1
            self.opened_door = True
        # If elevator goes down and on next floor pressed button down, we will stop
        if self.global_direction == -1 and self.outside_cabin[next_floor] in [-1, 2]:
            self.elevator.stop_and_open_doors()
            self.outside_cabin[next_floor] = 0 if self.outside_cabin[next_floor] == -1 else 1
            self.opened_door = True
        # If elevator goes up and on next floor pressed button down and there are not pressed button upper, we will stop
        if (self.global_direction == 1 and (self.outside_cabin[next_floor] == -1)
                and not self.check_floors_for_direction()):
            self.elevator.stop_and_open_doors()
            self.outside_cabin[next_floor] = 0
            self.opened_door = True
        # If elevator goes down and on next floor pressed button up and there are not pressed button lower, we will stop
        if (self.global_direction == -1 and (self.outside_cabin[next_floor] == 1)
                and not self.check_floors_for_direction()):
            self.elevator.stop_and_open_doors()
            self.outside_cabin[next_floor] = 0
            self.opened_door = True
        self.elevator.current_floor = next_floor  # for testing

    def on_floor_button_pressed(self, floor, direction):
        """This callback is called when someone presses a button on a floor"""
        print(f"On floor button pressed {floor} floor direction  {direction}")
        self.outside_cabin[floor] = 2 if self.outside_cabin[floor] not in [0, direction] else direction
        if self.global_direction == DIRECTION_NONE:
            self.set_global_direction(floor)

    def on_cabin_button_pressed(self, floor):
        """This callback is called when someone presses a button inside the
        cabin."""
        print(f"On cabin button pressed {floor} floor")
        self.inside_cabin[floor] = 1
        if self.global_direction == DIRECTION_NONE:
            self.set_global_direction(floor)


def move_elevator(elevator, steps):
    for _ in range(steps):
        next(elevator)


if __name__ == "__main__":
    """
    1 
    2
    3
    4
    5
    There are 5 users
    """
    elevator = Elevator(10)
    move_elevator(elevator, 1)
    elevator.on_floor_button_pressed(3, 1)  # 1 call elevator to go up
    move_elevator(elevator, 2)
    elevator.on_cabin_button_pressed(9)  # 1 decide to go to 9 floor
    move_elevator(elevator, 1)
    elevator.on_floor_button_pressed(5, 1)  # 2 call elevator to go up
    move_elevator(elevator, 1)
    elevator.on_floor_button_pressed(6, -1)  # 3 call elevator to go down
    move_elevator(elevator, 1)
    elevator.on_floor_button_pressed(7, 1)  # 4 call elevator to go up
    elevator.on_floor_button_pressed(7, -1)  # 5 call elevator to go down
    move_elevator(elevator, 1)
    elevator.on_cabin_button_pressed(6)  # 2 decide to go to 6 floor
    move_elevator(elevator, 3)
    elevator.on_cabin_button_pressed(9)  # 3 decide to go to 9 floor
    move_elevator(elevator, 5)
    elevator.on_cabin_button_pressed(2)  # 4 decide to go to 2 floor
    move_elevator(elevator, 2)
    elevator.on_cabin_button_pressed(1)  # 5 decide to go to 1 floor
    move_elevator(elevator, 10)




