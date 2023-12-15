from collections import deque


class ShiftRegister:
    def __init__(self, size):
        self.size = size
        self.register = deque([0] * size)

    def shift(self, data_in):
        """Shift the register to the right and insert new data at the leftmost position."""
        self.register.rotate(1)
        self.register[0] = data_in

    def at(self, index):
        """Get element in shift register at given index."""
        return self.register[index]
