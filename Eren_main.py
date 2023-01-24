# importing  libraries
import random

from  kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, Clock
from kivy import platform
from kivy.uix.relativelayout import RelativeLayout

#creating class and inheriting the relative layout
class MainWidget(RelativeLayout):

    #creating variables
    game_start = False
    score_1 = StringProperty("0")
    score_2 = StringProperty("0")
    my_score = 0
    op_score = 0
    start_menu = ObjectProperty()
    game_text = StringProperty("E   R   E   N")
    button_text = StringProperty("PLAY")
    rec_move = 4
    ball_pos_x = NumericProperty(500)
    ball_pos_y = NumericProperty(200)
    pos_x = 0
    pos_y = 0
    rec_pos_x = NumericProperty(0)
    rec_pos_y = NumericProperty(240)
    rec_2_pos_y = NumericProperty(200)
    constant_velocity = 5
    player_speed = 8
    velocity_x = constant_velocity
    velocity_y = constant_velocity
    ball_speed_x = 500
    ball_speed_y = 200
    i = 0
    j = 0

    def __init__(self , **kwargs):
        super(MainWidget , self).__init__(**kwargs)
        #self.ball takes in the position of the ball from the function
        self.on_game_start()
        self.on_size()
        self.rectangle_1_pos()
        self.rec_pos_x  = self.rectangle_1_pos()
        Clock.schedule_interval(self.Update , 0.01)

        #function that gets access to the keyboard
        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)
            self._keyboard.bind(on_key_up=self._on_keyboard_up)

    #function that loads the first window when the app starts
    def on_game_start(self):
        Builder.load_file("Start_menu.kv")

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    #does nothing when there is no input from the keyboard
    def _on_keyboard_up(self, keyboard, keycode):
        pass

    #controls the balls movement along the x-axis
    def move_ball_x(self, ball_velocity):
        self.ball_speed_x = self.ball_speed_x + ball_velocity
        return self.ball_speed_x

    #controls the balls movement along the y-axis
    def move_ball_y(self , ball_velocity):
        self.ball_speed_y =  self.ball_speed_y  + ball_velocity
        return self.ball_speed_y

    #when the button in the first window is pressed this executes
    def on_button_press(self):
        #making the window dissapear
        self.start_menu.opacity = 0
        #game has started
        self.game_start = True
        #setting all game scores to zero
        self.op_score  = 0
        self.score_1 = str("0")
        self.score_2 = str("0")
        self.my_score = 0

    #controls the position of the first rectangle
    def rectangle_1_pos(self):
        width , height = self.on_size()
        self.pos_x =  width  * .4
        return  self.pos_x

    #executes when the game ends
    def game_end(self , c1 , c2):
        #if either players score reaches 5 then the game ends and a message is displayed
        if c1 == 5 :
            self.start_menu.opacity  = 1
            self.button_text = "Retry"
            self.game_text = "You'll do better next time"
        if c2 == 5:
            self.start_menu.opacity = 1
            self.button_text = "Play again"
            self.game_text = "Well played "

    def on_touch_move(self, touch):
        width , height = self.on_size()
        if self.rec_pos_y < touch.y :
            if self.rec_pos_y < height - 139:
                self.rec_pos_y += self.player_speed
                return self.rec_pos_y
            else:
                self.rec_pos_y += -self.player_speed
                return self.rec_pos_y
        else:
            if 0 + 20  < self.rec_pos_y :
                self.rec_pos_y += -self.player_speed
                return self.rec_pos_y
            else:
                self.rec_pos_y += self.player_speed
                return self.rec_pos_y

    #this is for if  you use the keyboard
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        width, height = self.on_size()
        if keycode[1] == 'left':
            if self.rec_pos_y < height - 139:
                self.rec_pos_y += self.player_speed
                return self.rec_pos_y
            else:
                self.rec_pos_y += -self.player_speed
                return self.rec_pos_y
        elif keycode[1] == 'right':
            if 0 + 20  < self.rec_pos_y :
                self.rec_pos_y += -self.player_speed
                return self.rec_pos_y
            else:
                self.rec_pos_y += self.player_speed
                return self.rec_pos_y

    #update function is called every 0.01 seconds
    def Update(self , dt):
        width , height = self.on_size()
        x = self.rectangle_1_pos()

        #while the game is being played
        if self.game_start == True:
            #check for the y-position of the ball
            if self.ball_pos_y > height - 85:
                #ball bounce
                self.velocity_y = -self.constant_velocity
            elif self.ball_pos_y < 0 + 15:
                self.velocity_y = self.constant_velocity
                #check for the x-position of the ball
            if self.ball_pos_x > width - 85:
                #if the ball hits the boundary then goal
                self.my_score = self.my_score + 1
                print("my score: " + str(self.my_score))
                self.score_2 = str(self.my_score)
                self.velocity_x = -self.constant_velocity
            if self.ball_pos_x < 0 + 10:
                #if the ball hits the boundary then goal
                self.op_score = self.op_score + 1
                self.score_1 = str(self.op_score)
                print("his score: " + str(self.op_score))
                self.velocity_x = self.constant_velocity
            #checks if the ball has hit the pads
            if self.ball_pos_x > 0 + 15:
                for i in range(self.rec_2_pos_y - 60, self.rec_2_pos_y + 80):
                    if self.ball_pos_x > width - 160 and self.ball_pos_y == i:
                        self.velocity_x = -self.constant_velocity
                for i in range(self.rec_pos_y - 60, self.rec_pos_y + 80):
                    if self.ball_pos_x < 0 + 85 and self.ball_pos_y == i:
                        self.velocity_x = self.constant_velocity

            #controls the y position of the second put .
            #makes it follow tne balls y position
            if self.rec_2_pos_y < self.ball_pos_y:
                if self.rec_2_pos_y > height - 135:
                    self.rec_2_pos_y += -self.rec_move
                else:
                    self.rec_2_pos_y += self.rec_move
            if self.rec_2_pos_y > self.ball_pos_y:
                if self.rec_2_pos_y < 0 + 15:
                    self.rec_2_pos_y += self.rec_move
                else:
                    self.rec_2_pos_y += -self.rec_move

            self.game_end(self.op_score, self.my_score)

            self.ball_pos_y = self.move_ball_y(self.velocity_y)
            self.ball_pos_x = self.move_ball_x(self.velocity_x)
        else:
            pass

    #function that returns the size of the window
    def on_size(self , *args):
        # print(str(self.width)  + " "  + str(self.height))
        x = self.width
        y = self.height
        return x , y


    #checks the platform of the game is being played on
    def is_desktop(self):
        if platform  in ('linux', 'win', 'macosx'):
            return  True
        return False

class ErenApp(App):
    pass

ErenApp().run()
# TODO: "fix up the app and add images and edit your code "