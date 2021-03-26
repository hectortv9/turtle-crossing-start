from turtle import Turtle
import random

X, Y = 0, 1
PLAYER_SHAPE = "turtle"
PLAYER_COLOR = "gold"


class Player(Turtle):

    def __init__(self, court, car_manager, player_color=None):
        super().__init__(shape=PLAYER_SHAPE, visible=False)
        if player_color is None:
            player_color = PLAYER_COLOR
        self.court = court
        self.car_manager = car_manager
        self.is_player_move_enabled = True
        self.is_dead = False
        self.player_color = player_color
        self.x_initial = self.court.center_gap[X]
        self.y_initial = self.court.lowest_gap[Y]
        self.goal_gap = self.court.goal_gap
        self.heading_initial = 90
        self.move_distance = self.court.gap_size
        self.setheading(self.heading_initial)
        self.color(self.player_color)
        self.penup()
        self.speed(0)
        self.shapesize(stretch_wid=1, stretch_len=0.6)
        self.setposition(self.x_initial, self.y_initial)
        self.showturtle()

    @staticmethod
    def get_dead_body(player):
        dead_body = Player(player.court, player.car_manager)
        dead_body.hideturtle()
        dead_body.setposition(player.xcor(), player.ycor())
        dead_body.showturtle()
        player.hideturtle()
        player.getscreen().update()
        return dead_body

    @staticmethod
    def get_blood_stain(player):
        blood_stain = []
        for index in range(4):
            blood = Turtle(shape="circle", visible=False)
            blood.color("red")
            blood.penup()
            blood.setheading(105 * index)
            blood.speed(0)
            blood.shapesize(stretch_wid=0.6, stretch_len=0.4)
            blood.setposition(player.xcor(), player.ycor())
            blood.showturtle()
            blood_stain.append(blood)
        blood_stain[0].shapesize(stretch_wid=0.6, stretch_len=0.6)
        return blood_stain

    def kill(self):
        self.is_player_move_enabled = False
        self.is_dead = True
        self.kill_animation()

    def finalize(self):
        del self.court
        del self.car_manager

    def get_random_rgb(self):
        colormode = self.getscreen().colormode()
        r = random.randrange(int(colormode))
        g = random.randrange(int(colormode))
        b = random.randrange(int(colormode))
        return r, g, b

    def level_cleared_animation(self):
        for _ in range(120):
            self.setheading(self.heading() + 6)
            self.color(self.get_random_rgb())
            self.getscreen().update()
        self.color(self.player_color)
        self.getscreen().update()

    def kill_animation(self):
        dead_body = Player.get_dead_body(self)
        for _ in range(self.car_manager.collision_distance * 2):
            dead_body.setposition(dead_body.xcor() - 1, dead_body.ycor())
            dead_body.setheading(dead_body.heading() + 20)
            dead_body.getscreen().update()
        blood_stain = Player.get_blood_stain(dead_body)
        dead_body = Player.get_dead_body(dead_body)
        dead_body.getscreen().update()
        for _ in range(self.car_manager.collision_distance):
            for layer in range(len(blood_stain)):
                blood = blood_stain[layer]
                if layer == 0:
                    blood.shapesize(stretch_wid=blood.shapesize()[X] + 0.064, stretch_len=blood.shapesize()[Y] + 0.064)
                else:
                    blood.shapesize(stretch_wid=blood.shapesize()[X] + 0.08, stretch_len=blood.shapesize()[Y] + 0.044)
                    blood.getscreen().update()

    def return_to_starting_point(self):
        self.setheading(self.heading_initial)
        self.color(self.player_color)
        self.setposition(self.x_initial, self.y_initial)
        self.is_player_move_enabled = True

    def up(self):
        if self.is_player_move_enabled:
            self.setposition(self.xcor(), self.ycor() + self.move_distance)
            if self.ycor() >= self.goal_gap[Y]:
                self.is_player_move_enabled = False
            else:
                self.car_manager.check_collision(self)
                self.getscreen().update()

    def down(self):
        if self.is_player_move_enabled:
            if self.ycor() > self.court.lowest_gap[Y]:
                self.setposition(self.xcor(), self.ycor() - self.move_distance)
                if self.ycor() >= self.car_manager.bottom_lane_gap[Y]:
                    self.car_manager.check_collision(self)
                self.getscreen().update()
