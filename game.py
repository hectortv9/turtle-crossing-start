from screen_box import ScreenBox
import time
import court
import scoreboard
import player
import car_manager
import gc

UP, DOWN, LEFT, RIGHT = "Up", "Down", "Left", "Right"  # Key names
INITIAL_DELAY = 0.35
DELAY_DECREMENT = 0.05
DELAY_AFTER_SCORE = 1
SCREEN_TITLE = "Turtle Crossing"
MAX_SCORE = 10
X, Y = 0, 1


class Game:

    def __init__(self):
        self.screen_box = ScreenBox(title=SCREEN_TITLE)
        self.screen = self.screen_box.screen
        self.scoreboard = scoreboard.Scoreboard(self.screen_box.up_bound, self.screen_box.complementary_color)
        self.court = court.CourtGrid(self.scoreboard)
        self.car_manager = car_manager.CarManager(self.court)
        self.player = player.Player(self.court, self.car_manager)
        self.initialize_game()
        # self.get_visual_help()

    def initialize_game(self):
        backup_tracer = self.screen.tracer()
        self.screen.tracer(0)
        self.car_manager.create_traffic(self.player)
        self.start_listening()
        self.screen.tracer(backup_tracer)

    def start_listening(self):
        self.screen.onkeypress(self.player.up, UP)
        self.screen.onkeypress(self.player.down, DOWN)
        self.screen.listen()

    def get_visual_help(self):
        backup_tracer = self.screen.tracer()
        self.screen.tracer(0)
        self.screen_box.get_visual_help()
        self.court.draw_grid()
        # self.court.get_visual_help()
        self.screen.tracer(backup_tracer)

    def stop_listening(self):
        self.screen.onkeypress(None, UP)
        self.screen.onkeypress(None, DOWN)

    def do_start_game(self):
        player_input = self.screen.textinput(
            "Get ready", "Help the turtle cross the road using <UP> and <DOWN> keys.\n"
                         "Close this window whenever you are ready to start playing;\n "
                         "otherwise, type 'q' or 'quit' and click [OK] to exit game.")
        return player_input is None or (player_input.lower() != "q" and player_input.lower() != "quit")

    def finalize_game(self):
        self.player.finalize()
        del self.player
        self.car_manager.finalize()
        del self.car_manager
        self.screen_box.clear_screen()
        gc.collect()

    def play(self):
        delay = INITIAL_DELAY
        self.screen.tracer(0)
        while True:
            self.car_manager.move_cars(self.player)
            self.screen.update()
            if self.player.is_dead:
                self.stop_listening()
                self.scoreboard.print_game_over()
                break
            elif not self.player.is_player_move_enabled:
                self.player.level_cleared_animation()
                self.scoreboard.increase_score()
                self.player.return_to_starting_point()
                self.screen.update()
                delay = delay - DELAY_DECREMENT
            time.sleep(delay)
        self.screen.textinput(
            "GAME OVER", f"You reached [ Level {self.scoreboard.score} ]. Close this dialog to continue.")
        self.finalize_game()
