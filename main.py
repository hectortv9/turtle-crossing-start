from game import Game


if __name__ == '__main__':

    while True:
        game = Game()
        if game.do_start_game():
            game.play()
        else:
            break
