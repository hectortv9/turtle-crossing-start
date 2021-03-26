import random
import court
from car import Car
from screen_box import ScreenBox

X, Y = 0, 1
STARTING_MOVE_DISTANCE = 3
MOVE_INCREMENT = 20

CAR_LENGTH_RATIO = 3
CAR_LENGTH = CAR_LENGTH_RATIO * court.GAP_SIZE
CAR_WIDTH_RATIO = 0.8
HALF_GAP_SIZE = int(court.GAP_SIZE / 2)
CAR_GRID_GAP_OFFSET = HALF_GAP_SIZE * abs((CAR_LENGTH_RATIO % 2) - 1)  # 0 if ratio is odd, half gap if even
CAR_GRID_BOUND_OFFSET = int((CAR_LENGTH_RATIO - 1) / 2) * court.GAP_SIZE
CAR_CENTER_TO_BUMPER_DISTANCE = HALF_GAP_SIZE * CAR_LENGTH_RATIO

INITIAL_CAR_COUNT = 100


class Lane:

    def __init__(self):
        self.cars = []

    def append(self, item):
        self.cars.append(item)


class CarManager:

    def __init__(self, court2: court.CourtGrid):
        self.court = court2
        self.lane_count = self.court.vertical_gap_count - 2  # gaps used for turtle and goal
        self.bottom_lane_gap = (
            self.court.right_bound - HALF_GAP_SIZE,  # bottom-right corner gap
            self.court.lowest_gap[Y] + self.court.gap_size)
        self.bottom_starter_gap = (
            self.bottom_lane_gap[X] + self.court.gap_size + CAR_GRID_GAP_OFFSET + CAR_GRID_BOUND_OFFSET,
            self.bottom_lane_gap[Y])
        self.first_car_gap_x = self.bottom_starter_gap[X] - CAR_LENGTH
        self.out_of_screen_x = ScreenBox().left_bound - int(CAR_LENGTH / 2)
        self.hit_x = self.court.center_gap[X] + (HALF_GAP_SIZE * (CAR_LENGTH_RATIO - 1))
        self.collision_distance = CAR_CENTER_TO_BUMPER_DISTANCE + HALF_GAP_SIZE  # do not compare with equal to
        self.lanes = [Lane() for _ in range(self.lane_count)]
        self.available_lanes = [lane for lane in self.lanes]
        self.busy_lanes = []
        self.lane_y_coord_map = {index: self.bottom_lane_gap[Y] + index * self.court.gap_size
                                 for index in range(self.lane_count)}
        self.parking_gap = (self.first_car_gap_x, self.court.lowest_gap[Y])
        self.parked_cars = []
        # self.available_horizontal_gap_count = self.court.horizontal_gap_count - CAR_LENGTH_RATIO

    def create_traffic(self, player):
        for _ in range(self.court.horizontal_gap_count + 1):
            self.move_cars(player)

    def drive_car_to_lane(self, lane):
        self.available_lanes.remove(lane)
        self.busy_lanes.append(lane)
        lane_number = self.lanes.index(lane)
        if self.parked_cars:
            car = self.parked_cars.pop()
            car.exit_parking_lot(self.bottom_starter_gap[X], self.lane_y_coord_map[lane_number])
        else:
            car = Car(self.bottom_starter_gap[X], self.lane_y_coord_map[lane_number], CAR_WIDTH_RATIO, CAR_LENGTH_RATIO)
        self.lanes[lane_number].append(car)

    def return_car_to_parking_lot(self, lane):
        car = lane.cars.pop(0)
        car.park(self.parking_gap[X], self.parking_gap[Y])
        self.parked_cars.append(car)

    def move_cars(self, player):
        for lane in self.lanes:
            cars = lane.cars
            if cars:
                for car in cars:
                    if player.is_dead:
                        return
                    else:
                        car.forward(MOVE_INCREMENT)
                    if car.xcor() == self.hit_x:
                        if player.ycor() == self.lane_y_coord_map[self.lanes.index(lane)]:
                            player.kill()
                            return
                if lane in self.busy_lanes:
                    if cars[-1].xcor() <= self.first_car_gap_x:  # check if car can be queued in lane
                        self.busy_lanes.remove(lane)
                        self.available_lanes.append(lane)
                if cars[0].xcor() <= self.out_of_screen_x:
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
        lane_number = list(self.lane_y_coord_map.values()).index(player.ycor())
        lane = self.lanes[lane_number]
        for car in lane.cars:
            if car.xcor() - self.collision_distance < player.xcor() < car.xcor() + self.collision_distance:
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

    """
    def get_random_gap_x(self):
        random_gap = random.randint(0, self.available_horizontal_gap_count)
        offsets = CAR_GRID_GAP_OFFSET + CAR_GRID_BOUND_OFFSET
        x = self.court.lowest_gap[X] + (random_gap * self.court.gap_size) + offsets
        return x
        
    def get_random_lane_y(self):
        r = random.randrange(self.lane_count)
        y = self.lane_y_coord_map[r]
        return y
    """
