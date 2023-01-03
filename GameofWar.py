import arcade
import random


class GameofWar(arcade.Window):
    def __init__(self):
        super().__init__(800, 800, "Game Of War")
        self.player = None
        self.targets = arcade.SpriteList()
        self.shootList = arcade.SpriteList()
        self.score = 0  # stores the amount of points the player earns
        self.sound = None
        self.shoot_sound = None
        self.player_dx = 0

        #  for laser reference
        self.shipposx = 400
        self.shipposy = 50

        self.counter = 0  # counts the number of enemy ships destroyed
        self.write = ""  # stores "You Lose!" or "You Win!" outputs
        self.ender = 0  # checks to see if u got hit

    def setup(self):
        self.sound = arcade.load_sound(":resources:sounds/hit2.wav")
        self.player = arcade.Sprite(":resources:images/space_shooter/playerShip1_blue.png")
        for number in range(6):
            enemy = arcade.Sprite(":resources:images/space_shooter/playerShip3_orange.png")
            self.targets.append(enemy)
            enemy.center_x = random.randint(15, 745)
            enemy.center_y = random.randint(750, 800)
        self.player.center_x = 400
        self.player.center_y = 20

    def on_update(self, delta_time):
        for enemy in self.targets:
            enemy.center_y -= 5
            hit_list2 = arcade.check_for_collision_with_list(self.player,
                                                             self.targets)  # checks for collision with player
            if len(hit_list2) > 0:  # checks to see if u got hit
                self.ender += 1
            if enemy.center_y < 0:  # checks for y position of enemy ships
                if self.score < 20 and self.ender < 1:
                    enemy.center_y = 745
                    for number in range(self.counter):  # regenerates enemy ships when they reach the bottom
                        enemy = arcade.Sprite(":resources:images/space_shooter/playerShip3_orange.png")
                        self.targets.append(enemy)
                        enemy.center_x = random.randint(10, 750)
                        enemy.center_y = random.randint(750, 800)
                    for enemy2 in self.targets:  # changes enemies positions
                        enemy2.center_x = random.randint(10, 750)
                        enemy2.center_y = random.randint(750, 800)
                    self.counter = 0  # resets counter variable
                elif self.ender > 0:  # stops short, implement way to delete ships after lose
                    sound1 = arcade.load_sound(":resources:sounds/lose5.wav")
                    arcade.play_sound(sound1)
                    self.write = "You Lose!"
                else:  # stops short, implement way to delete ships after win
                    sound2 = arcade.load_sound(":resources:sounds/coin1.wav")
                    arcade.play_sound(sound2)
                    self.write = "You Win!"
        for attack in self.shootList:
            hit_list = arcade.check_for_collision_with_list(attack, self.targets)  # checks for collision
            if len(hit_list) > 0:  # when you hit a ship, hit_list increases
                attack.remove_from_sprite_lists()  # removes laser
            for tar in hit_list:  # runs for every ship you have hit
                tar.remove_from_sprite_lists()  # removes enemy ship
                self.score += 1  # adds 1 everytime you hit an enemy ship to score
                self.counter += 1  # increases counter variable for each ship destroyed
            attack.center_y += 5  # laser speed
            if attack.center_x < 0:
                attack.center_x = 745
        self.player.center_x += self.player_dx
        if self.player.center_x > 800:
            self.player.center_x = 0
        if self.player.center_x < 0:
            self.player.center_x = 800

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, 14)
        arcade.draw_text(self.write, 300, 400, arcade.color.WHITE, 30)
        self.player.draw()
        self.shootList.draw()
        self.targets.draw()
        arcade.finish_render()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.D:
            self.player_dx = 2
            self.shipposx = 2
        if symbol == arcade.key.A:
            self.player_dx = -2
            self.shipposy = 2

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.A or symbol == arcade.key.D:
            self.player_dx = 0

    def on_mouse_press(self, x, y, button, modifiers):
        self.shoot_sound = arcade.load_sound(":resources:sounds/fall4.wav")
        # self.player = arcade.Sprite(":resources:images/space_shooter/playerShip1_blue.png")

        attack = arcade.Sprite(":resources:images/space_shooter/laserRed01.png")
        self.shootList.append(attack)
        arcade.play_sound(self.shoot_sound)
        attack.center_x = self.player.center_x
        attack.center_y = self.shipposy
