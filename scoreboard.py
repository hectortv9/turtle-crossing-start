from turtle import Turtle
from tkinter.font import Font
from screen_box import ScreenBox

SCORE_FONT = ("Terminal", 16, "bold")
GAME_OVER_FONT = ("Terminal", 50, "bold")
X, Y = 0, 1
SCORE_COLOR = "magenta"
GAME_OVER_SHADOW_COLOR = "yellow"
GAME_OVER_COLOR = "red"
TOP_MARGIN = 20
BOTTOM_MARGIN = 10


class Scoreboard(Turtle):

    def __init__(self, up_bound, color=None):
        super().__init__(visible=False)
        color = SCORE_COLOR if color is None else color
        self.score = 1
        self.scoreboard_width = 0
        self.scoreboard_height = self.get_font_height(SCORE_FONT) + TOP_MARGIN + BOTTOM_MARGIN
        self.starting_position = 0, up_bound - (self.scoreboard_height - BOTTOM_MARGIN)
        self.pencolor(color)
        self.speed(0)
        self.setundobuffer(None)
        self.penup()
        self.print_score()

    @staticmethod
    def get_font_height(font):
        font_config = Font(font=font)
        font_ascent = font_config.metrics('ascent')  # keep this just for reference
        line_space = font_config.metrics('linespace') - font_ascent
        return int(font_ascent + line_space)

    def print_score(self):
        self.clear()
        self.setposition(self.starting_position)
        baseline_start = self.position()[X]
        self.write(f"Level {self.score}", move=True, align="center", font=SCORE_FONT)
        baseline_end = self.position()[X]
        self.setposition(self.starting_position)

        self.scoreboard_width = baseline_end - baseline_start

    def print_end_of_game(self, message, do_celebrate):
        x = 0
        y = - int(self.get_font_height(GAME_OVER_FONT) / 2)

        self.draw_message_shadow(x, y, message, GAME_OVER_SHADOW_COLOR, GAME_OVER_FONT)
        self.write_simple_message(x, y, message, GAME_OVER_COLOR, GAME_OVER_FONT)

        if do_celebrate:
            banner_width = ScreenBox().right_bound - ScreenBox().left_bound
            banner_height = abs(y * 3)
            banner_bottom_left_xy = (ScreenBox().left_bound, - int(banner_height / 2))
            self.setheading(0)
            for _ in range(400):
                self.goto(banner_bottom_left_xy[X], banner_bottom_left_xy[Y])
                color = ScreenBox().get_random_rgb()
                self.fillcolor(color)
                self.begin_fill()
                for _ in range(2):
                    self.forward(banner_width)
                    self.left(90)
                    self.forward(banner_height)
                    self.left(90)
                self.end_fill()
                self.write_simple_message(x, y, message, ScreenBox().get_complementary_color(color), GAME_OVER_FONT)
                self.getscreen().update()

    def draw_message_shadow(self, x, y, message, color, font):
        self.color(color)
        rotation_degrees = 45
        for _ in range(int(360 / rotation_degrees)):
            self.setposition(x, y)
            self.right(rotation_degrees)
            self.forward(8)
            self.write(message, move=False, align="center", font=font)

    def write_simple_message(self, x, y, message, color, font):
        self.setposition(x, y)
        self.color(color)
        self.write(message, move=False, align="center", font=font)

    def increase_score(self):
        self.score += 1
        self.print_score()
