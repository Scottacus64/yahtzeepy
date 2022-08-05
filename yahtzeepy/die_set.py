from yahtzeepy.die import Die


class DieSet(object):
    def __init__(self):
        self._die_set = []
        for i in range(5):
            self._die_set.append(Die(False))

    def get_at(self, index):
        return self._die_set[index]

    def copy(self):
        return self._die_set.copy()
