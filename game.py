from screen_box import ScreenBox
import time
import court
import scoreboard
import player
import car_manager
import gc

UP, DOWN, LEFT, RIGHT = "Up", "Down", "Left", "Right"  # Key names
INITIAL_DELAY = 350
DELAY_DECREMENT = 50
SCREEN_TITLE = "Turtle Crossing"
DEFAULT_DIFFICULTY = "g"
X, Y = 0, 1


class Game:

    DIFFICULTIES = {
        "e": {"win_phase": 1, "name": "Easy mode"},
        "h": {"win_phase": 2, "name": "Hard mode"},
        "g": {"win_phase": 3, "name": "Greta Thunberg mode"}}

    def __init__(self):
        self.screen_box = ScreenBox(title=SCREEN_TITLE)
        self.screen = self.screen_box.screen
        self.scoreboard = scoreboard.Scoreboard(self.screen_box.up_bound, self.screen_box.complementary_color)
        self.court = court.CourtGrid(self.scoreboard)
        self.car_manager = car_manager.CarManager(self.court)
        self.player = player.Player(self.court, self.car_manager)
        self.difficulty = Game.DIFFICULTIES[DEFAULT_DIFFICULTY]
        self.initialize_game()
        # self.get_visual_help()

    def initialize_game(self):
        backup_tracer = self.screen.tracer()
        self.screen.tracer(0)
        self.car_manager.create_traffic(self.player)
        self.start_listening()
        self.screen.tracer(backup_tracer)
        self.set_difficulty(self.difficulty)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        title = f'{SCREEN_TITLE} ({self.difficulty["name"]})'
        self.screen_box.screen.title(title)

    def start_listening(self):
        self.screen.listen()
        self.screen.getcanvas().bind("<Up>", self.player.up)
        self.screen.getcanvas().bind("<Down>", self.player.up)
        self.screen.onkeypress(self.player.up, UP)
        self.screen.onkeypress(self.player.down, DOWN)

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
            "Get ready",
            "Help the turtle cross the road using <UP> and <DOWN> arrow keys.\n\n"
            "Levels: \n"
            "Choose the difficulty by typing any of the following option letters and click [OK] to start playing: \n"
            "Enter 'e' for Easy mode. \n"
            "Enter 'h' for Hard mode. \n"
            "Enter 'g' for Greta Thunberg mode. This is the default mode, used if nothing is typed below. \n\n"
            "Hints: \n1) Sometimes you need to back up to keep moving forward. \n"
            "2) It's safer to aim for car's rear bumper than the front one. Keep it real ! \n"
            "3) The turtle can stop time and run faster than you run to the WC after eating bad food. \n\n"
            "Close this window whenever you are ready to start playing; "
            "otherwise, type 'q' or 'quit' and click [OK] to exit game.")

        do_play = True
        if player_input is not None:
            player_input = player_input.lower().strip()
            if player_input == "q" or player_input == "quit":
                do_play = False
            else:
                if player_input in Game.DIFFICULTIES:
                    self.set_difficulty(Game.DIFFICULTIES[player_input])
        return do_play

    def validate_results(self, has_won):
        if has_won:
            self.screen.textinput(
                "ALL LEVELS CLEARED !!!", f"You helped the turtle cross the highway {self.scoreboard.score} times."
                                          f"\nClearly natural selection works in mysterious ways. "
                                          f"Thank you for your service! You are a winner :)\n"
                                          f"Close this dialog to continue.")
        else:
            self.screen.textinput(
                "GAME OVER", f"You reached [ Level {self.scoreboard.score} ]. Close this dialog to continue.")

    def finalize_game(self):
        self.player.finalize()
        del self.player
        self.car_manager.finalize()
        del self.car_manager
        self.screen_box.clear_screen()
        gc.collect()

    def play(self):
        has_won = False
        car_length_ratio = car_manager.DEFAULT_CAR_LENGTH_RATIO
        delay = INITIAL_DELAY
        min_delay = DELAY_DECREMENT * car_manager.DEFAULT_CAR_LENGTH_RATIO
        self.screen.tracer(0)
        while True:
            self.car_manager.move_cars(self.player)
            self.screen.update()
            if self.player.is_dead:
                self.stop_listening()
                self.scoreboard.print_end_of_game("GAME OVER", False)
                break
            elif not self.player.is_player_move_enabled:
                self.player.level_cleared_animation()
                self.player.return_to_starting_point()
                self.screen.update()
                if delay > min_delay:
                    self.scoreboard.increase_score()
                    delay = delay - DELAY_DECREMENT
                else:
                    delay = INITIAL_DELAY
                    car_length_ratio += 1
                    min_delay = (DELAY_DECREMENT * car_length_ratio)
                    self.car_manager.set_car_length(car_length_ratio, self.player)
                    if car_length_ratio > self.difficulty["win_phase"]:
                        has_won = True
                        self.car_manager.clear_highway()
                        self.scoreboard.print_end_of_game("JU WEEN!", True)
                        break
            time.sleep(delay / 1000)
        self.validate_results(has_won)
        self.finalize_game()
