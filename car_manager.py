import random
import court
from car import Car
from screen_box import ScreenBox

X, Y = 0, 1
DEFAULT_CAR_LENGTH_RATIO = 1


class Lane:

    def __init__(self):
        self.cars = []

    def append(self, item):
        self.cars.append(item)


class CarManager:

    class Calculations:

        def __init__(self, game_court, car_length_ratio=DEFAULT_CAR_LENGTH_RATIO):
            self.car_length_ratio = car_length_ratio
            self.car_width_ratio = 0.8

            self.car_length = self.car_length_ratio * court.GAP_SIZE
            self.half_gap_size = int(court.GAP_SIZE / 2)
            # car_grid_gap_offset becomes 0 if car_length_ratio is odd or half gap if it's even
            self.car_grid_gap_offset = self.half_gap_size * abs((self.car_length_ratio % 2) - 1)
            self.car_grid_bound_offset = int((self.car_length_ratio - 1) / 2) * court.GAP_SIZE
            self.car_center_to_bumper_distance = self.half_gap_size * self.car_length_ratio

            self.lane_count = game_court.vertical_gap_count - 2  # gaps used for turtle and goal
            self.bottom_lane_gap = (
                game_court.right_bound - self.half_gap_size,  # bottom-right corner gap
                game_court.lowest_gap[Y] + game_court.gap_size)
            self.bottom_starter_gap = (
                self.bottom_lane_gap[X] + game_court.gap_size + self.car_grid_gap_offset + self.car_grid_bound_offset,
                self.bottom_lane_gap[Y])
            self.first_car_gap_x = self.bottom_starter_gap[X] - self.car_length
            self.out_of_screen_x = ScreenBox().left_bound - int(self.car_length / 2)
            self.hit_x = game_court.center_gap[X] + (self.half_gap_size * (self.car_length_ratio - 1))
            # do not compare collision_distance with equal to operators
            self.collision_distance = self.car_center_to_bumper_distance + self.half_gap_size
            self.lane_y_coord_map = {index: self.bottom_lane_gap[Y] + index * game_court.gap_size
                                     for index in range(self.lane_count)}
            self.parking_gap = (self.first_car_gap_x, game_court.lowest_gap[Y])

    def __init__(self, game_court):
        self.court = game_court
        self.calc = CarManager.Calculations(self.court)
        self.lanes = [Lane() for _ in range(self.calc.lane_count)]
        self.available_lanes = [lane for lane in self.lanes]
        self.busy_lanes = []
        self.parked_cars = []
        Car.register_car_shape()

    def set_car_length(self, car_length_ratio, player):
        self.calc = CarManager.Calculations(self.court, car_length_ratio)
        self.clear_highway()
        for car in self.parked_cars:  # update size and position for all cars in parking lot
            car.change_car_size(self.calc.car_width_ratio, self.calc.car_length_ratio)
            car.park(self.calc.parking_gap[X], self.calc.parking_gap[Y])
        self.create_traffic(player)

    def clear_highway(self):
        for lane in self.lanes:  # return all cars to parking lot
            while lane.cars:
                self.return_car_to_parking_lot(lane)

    def create_traffic(self, player):
        for _ in range(self.court.horizontal_gap_count + 1):
            self.move_cars(player)

    def drive_car_to_lane(self, lane):
        self.available_lanes.remove(lane)
        self.busy_lanes.append(lane)
        lane_number = self.lanes.index(lane)
        if self.parked_cars:
            car = self.parked_cars.pop()
            car.exit_parking_lot(self.calc.bottom_starter_gap[X], self.calc.lane_y_coord_map[lane_number])
        else:
            car = Car(self.calc.bottom_starter_gap[X], self.calc.lane_y_coord_map[lane_number],
                      self.calc.car_width_ratio, self.calc.car_length_ratio)
        self.lanes[lane_number].append(car)

    def return_car_to_parking_lot(self, lane):
        car = lane.cars.pop(0)
        car.park(self.calc.parking_gap[X], self.calc.parking_gap[Y])
        self.parked_cars.append(car)

    def move_cars(self, player):
        for lane in self.lanes:
            cars = lane.cars
            if cars:
                for car in cars:
                    if player.is_dead:
                        return
                    else:
                        car.forward(court.GAP_SIZE)
                    if car.xcor() == self.calc.hit_x:
                        if player.ycor() == self.calc.lane_y_coord_map[self.lanes.index(lane)]:
                            player.kill()
                            return
                if lane in self.busy_lanes:
                    if cars[-1].xcor() <= self.calc.first_car_gap_x:  # check if car can be queued in lane
                        self.busy_lanes.remove(lane)
                        self.available_lanes.append(lane)
                if cars[0].xcor() <= self.calc.out_of_screen_x:
                    self.return_car_to_parking_lot(lane)
        self.queue_random_cars()

    def queue_random_cars(self):
        min_cars_added = 0
        max_cars_added = 3
        for _ in range(random.randint(min_cars_added, max_cars_added + 1)):  # add 1 to max because of range function
            if self.available_lanes:
                lane = random.choice(self.available_lanes)
                self.drive_car_to_lane(lane)

    def check_collision(self, player):
        lane_number = list(self.calc.lane_y_coord_map.values()).index(player.ycor())
        lane = self.lanes[lane_number]
        for car in lane.cars:
            if car.xcor() - self.calc.collision_distance < player.xcor() < car.xcor() + self.calc.collision_distance:
                player.kill()

    def finalize(self):
        self.lanes.clear()
        self.available_lanes.clear()
        self.busy_lanes.clear()
        self.parked_cars.clear()
        del self.lanes
        del self.available_lanes
        del self.busy_lanes
        del self.parked_cars
