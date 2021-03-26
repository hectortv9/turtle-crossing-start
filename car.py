import random
from screen_box import ScreenBox
from turtle import Turtle

FILL_COLORS = ["cornflower blue", "lime green", "orchid", "bisque3", "DarkOliveGreen4", "turquoise3", "purple3"]
CAR_COLOR = "white"
CAR_SHAPE_NAME = "car"
CAR_SHAPE = ((3, -10), (3, -6), (10, -5), (10, 4), (3, 6), (3, 10), (-7, 10), (-7, 7), (-10, 6),
             (-10, 4), (-7, 3), (-7, -3), (-10, -4), (-10, -6), (-7, -7), (-7, -10))
ScreenBox().screen.register_shape(name=CAR_SHAPE_NAME, shape=CAR_SHAPE)


class Car(Turtle):

    def __init__(self, x, y, car_width_ratio, car_length_ratio):
        super().__init__(shape=CAR_SHAPE_NAME, visible=False)
        self.speed(0)
        self.setheading(180)
        self.shapesize(stretch_wid=car_width_ratio, stretch_len=car_length_ratio)
        self.penup()
        self.color(CAR_COLOR)
        self.fillcolor(random.choice(FILL_COLORS))
        self.setposition(x, y)
        self.showturtle()

    def park(self, x, y):
        self.hideturtle()
        self.goto(x, y)

    def exit_parking_lot(self, x, y):
        self.goto(x, y)
        self.showturtle()
