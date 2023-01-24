#importing the relative  layout
from kivy.uix.relativelayout import RelativeLayout

#inheriting the relative layout
class  Start_menu(RelativeLayout):
    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super(RelativeLayout , self).on_touch_down(touch)



