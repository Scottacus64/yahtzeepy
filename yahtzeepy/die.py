import random


class Die(object):
    def __init__(self, _is_clicked):
        self._pip = 0
        self.is_clicked = _is_clicked

    def set_pip(self, pip):
        self._pip = pip

    def get_image(self):
        return ("y" if self.is_clicked else "w") + str(self._pip) + ".jpg"

    def get_pip(self):
        return self._pip

    def roll_die(self):
        self._pip = random.choice(
            [1, 2, 3, 4, 5, 6])  # uses random's .choice method to select a random number from 1 to 6
        self.is_clicked = False  # set to the white unclicked state
