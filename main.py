import arcade
from GameofWar import GameofWar

def main():
    valley_window = GameofWar()
    arcade.set_background_color(arcade.color.BLACK)
    valley_window.setup()
    arcade.run()

main()