from turtle import Turtle
from screen_box import ScreenBox
import math

X, Y = 0, 1
UP, DOWN, LEFT, RIGHT = "up", "down", "left", "right"
GAP_SIZE = 20
GRID_EDGE_COLOR = "magenta"
HIGHWAY_COLOR = "black"
PAVEMENT_LINES_COLOR = "white"
PAVEMENT_LINES_THICKNESS = 3
PAVEMENT_LINE_SIZE = 50
PAVEMENT_LINE_GAP_SIZE = 1.2 * PAVEMENT_LINE_SIZE
SIDEWALK_COLOR = (150, 150, 150)

# Visual help variables
GRID_COLOR = "yellow"
FILL_GAP_COLOR = "orange"
FILL_GAP_SHAPE = "circle"


class CourtGrid:

    def __init__(self, scoreboard):
        self.gap_size = GAP_SIZE
        self.scoreboard = scoreboard

        self.bouncing_distance = self.gap_size * 0.55  # distance at which ball can be considered to bounce against

        self.boundaries = self.get_grid_bounds()
        self.up_bound = self.boundaries[UP]
        self.left_bound = self.boundaries[LEFT]
        self.right_bound = self.boundaries[RIGHT]
        self.down_bound = self.boundaries[DOWN]

        self.horizontal_gap_count = int(abs(self.right_bound - self.left_bound) / self.gap_size)
        self.vertical_gap_count = int(abs(self.up_bound - self.down_bound) / self.gap_size)
        self.lowest_gap = (int(self.left_bound + self.gap_size / 2), int(self.down_bound + self.gap_size / 2))
        self.center_gap = (int(self.horizontal_gap_count / 2) * self.gap_size + self.lowest_gap[X],
                           int(self.vertical_gap_count / 2) * self.gap_size + self.lowest_gap[Y])
        # center_gap will lean towards +x, +y when gaps are even, it will get perfectly centered when they are odd
        self.goal_gap = (self.center_gap[X], self.lowest_gap[Y] + (self.vertical_gap_count - 1) * self.gap_size)

        self.draw_highway()

    def get_nth_gap_x(self, gap_number, from_left_to_right=True):
        if from_left_to_right:
            return (gap_number - 1) * self.gap_size + self.lowest_gap[X]
        else:
            return (self.horizontal_gap_count - gap_number) * self.gap_size + self.lowest_gap[X]

    def get_centered_y(self, shape_height):
        grid_height = self.vertical_gap_count * self.gap_size
        if shape_height > grid_height:
            raise Exception(f"ERROR: INSUFFICIENT SPACE. COURT HEIGHT={grid_height}, SHAPE HEIGHT={grid_height}")
        shape_vertical_gap_count = int(shape_height / self.gap_size)
        if shape_vertical_gap_count % 2 == 0:  # if the vertical gap count is odd
            y = self.center_gap[Y] - int(self.gap_size / 2)
        else:
            y = self.center_gap[Y]
        return y

    def get_visual_help(self):
        self.draw_grid()
        self.draw_grid_edges()
        self.fill_lowest_gaps()

    def draw_grid_edges(self, color=None):
        color = GRID_EDGE_COLOR if color is None else color
        backup_color = ScreenBox().utility_turtle.pencolor()
        speed = ScreenBox().utility_turtle.speed()
        ScreenBox().utility_turtle.speed(0)
        ScreenBox().utility_turtle.pencolor(color)
        turtle = ScreenBox().utility_turtle
        turtle.goto(self.boundaries[LEFT], self.boundaries[UP])
        turtle.pendown()
        turtle.goto(self.boundaries[RIGHT], self.boundaries[UP])
        turtle.goto(self.boundaries[RIGHT], self.boundaries[DOWN])
        turtle.goto(self.boundaries[LEFT], self.boundaries[DOWN])
        turtle.goto(self.boundaries[LEFT], self.boundaries[UP])
        turtle.penup()
        ScreenBox().utility_turtle.pencolor(backup_color)
        ScreenBox().utility_turtle.speed(speed)

    def draw_highway(self):
        backup_tracer = ScreenBox().screen.tracer()
        ScreenBox().screen.tracer(0)
        up = self.boundaries[UP] - self.gap_size
        down = self.boundaries[DOWN] + self.gap_size
        left = ScreenBox().left_bound
        right = ScreenBox().right_bound
        turtle = ScreenBox().utility_turtle
        backup_fill_color = turtle.fillcolor()
        backup_speed = turtle.speed()
        turtle.speed(0)

        turtle.fillcolor(SIDEWALK_COLOR)
        turtle.goto(left, up)
        turtle.begin_fill()
        turtle.goto(right, up)
        turtle.goto(right, self.boundaries[UP])
        turtle.goto(left, self.boundaries[UP])
        turtle.goto(left, up)
        turtle.end_fill()

        turtle.fillcolor(HIGHWAY_COLOR)
        turtle.begin_fill()
        turtle.goto(right, up)
        turtle.goto(right, down)
        turtle.goto(left, down)
        turtle.goto(left, up)
        turtle.end_fill()
        turtle.fillcolor(backup_fill_color)

        turtle.fillcolor(SIDEWALK_COLOR)
        turtle.goto(left, down)
        turtle.begin_fill()
        turtle.goto(right, down)
        turtle.goto(right, self.boundaries[DOWN])
        turtle.goto(left, self.boundaries[DOWN])
        turtle.goto(left, down)
        turtle.end_fill()

        backup_pencolor = turtle.pencolor()
        backup_pensize = turtle.pensize()
        turtle.pencolor(PAVEMENT_LINES_COLOR)
        turtle.pensize(PAVEMENT_LINES_THICKNESS)
        highway_size = abs(right - left)
        line_count = math.ceil(highway_size / (PAVEMENT_LINE_SIZE + PAVEMENT_LINE_GAP_SIZE))
        turtle.goto(left, up - self.gap_size)
        turtle.setheading(0)
        for y_lane in range(up - self.gap_size, down, -self.gap_size):
            turtle.goto(left, y_lane)
            for _ in range(line_count):
                turtle.pendown()
                turtle.forward(PAVEMENT_LINE_SIZE)
                turtle.penup()
                turtle.forward(PAVEMENT_LINE_GAP_SIZE)

        turtle.pencolor(backup_pencolor)
        turtle.pensize(backup_pensize)
        turtle.speed(backup_speed)
        ScreenBox().screen.tracer(backup_tracer)

    def draw_grid(self):
        color = ScreenBox().utility_turtle.pencolor()
        speed = ScreenBox().utility_turtle.speed()
        ScreenBox().utility_turtle.speed(0)
        ScreenBox().utility_turtle.pencolor(GRID_COLOR)
        turtle = ScreenBox().utility_turtle
        for y in range(self.boundaries[DOWN], self.boundaries[UP] + 1, self.gap_size):
            turtle.goto(self.boundaries[LEFT], y)
            turtle.pendown()
            turtle.goto(self.boundaries[RIGHT], y)
            turtle.penup()
        for x in range(self.boundaries[LEFT], self.boundaries[RIGHT] + 1, self.gap_size):
            turtle.goto(x, self.boundaries[UP])
            turtle.pendown()
            turtle.goto(x, self.boundaries[DOWN])
            turtle.penup()
        ScreenBox().utility_turtle.pencolor(color)
        ScreenBox().utility_turtle.speed(speed)

    def fill_lowest_gaps(self):
        for x in range(self.horizontal_gap_count):
            turtle = Turtle(shape=FILL_GAP_SHAPE)
            turtle.speed(0)
            turtle.color(FILL_GAP_COLOR)
            turtle.setposition(self.lowest_gap[X] + (x * self.gap_size), self.lowest_gap[Y])
        for y in range(self.vertical_gap_count):
            turtle = Turtle(shape=FILL_GAP_SHAPE)
            turtle.speed(0)
            turtle.color(FILL_GAP_COLOR)
            turtle.setposition(self.lowest_gap[X], self.lowest_gap[Y] + (y * self.gap_size))

    @staticmethod
    def adjust_boundary(boundary, gap_size):
        # boundary is the distance between origin (0, 0) and a point at a coordinate axes
        # boundary is signed indicating the direction of axis (e.g. +x, -x, +y, -y)
        # grid will be aligned with coordinate axes but they won't overlap
        adjusted_boundary = abs(boundary)  # remove sign to work only with magnitudes
        adjusted_boundary -= abs(boundary) % (gap_size / 2)  # round down to multiples of half gap size
        if adjusted_boundary % gap_size == 0:  # means grid is aligned with origin (0, 0)
            adjusted_boundary -= gap_size / 2  #
        adjusted_boundary = int(adjusted_boundary * (abs(boundary) / boundary))  # recover sign
        return adjusted_boundary

    def get_grid_bounds(self):
        left_bound = ScreenBox().left_bound
        right_bound = ScreenBox().right_bound
        up_bound = ScreenBox().up_bound - self.scoreboard.scoreboard_height
        down_bound = ScreenBox().down_bound

        # calculate amount of gaps that can fit horizontally
        raw_width = abs(left_bound) + abs(right_bound)
        raw_width -= raw_width % self.gap_size
        # calculate amount of gaps that can fit vertically
        raw_height = abs(up_bound) + abs(down_bound)
        raw_height -= raw_height % self.gap_size
        if raw_width < self.gap_size or raw_height < self.gap_size:
            raise Exception(f"ERROR: INSUFFICIENT SPACE FOR FOOD GRID. raw_width={raw_width}, raw_height={raw_height}")
        # adjust top boundary with respect to origin and size of grid's gaps
        up = self.adjust_boundary(up_bound, self.gap_size)
        # adjust left boundary with respect to origin and size of grid's gaps
        left = self.adjust_boundary(left_bound, self.gap_size)
        # adjust right boundary with respect to origin and size of grid's gaps
        right = self.adjust_boundary(right_bound, self.gap_size)
        # adjust bottom boundary with respect to origin and size of grid's gaps
        down = self.adjust_boundary(down_bound, self.gap_size)
        if not (up > down and right > left):
            raise Exception(f"ERROR: INSUFFICIENT SPACE FOR FOOD GRID. raw_width={raw_width}, raw_height={raw_height}")

        return {UP: up, DOWN: down, LEFT: left, RIGHT: right, }
