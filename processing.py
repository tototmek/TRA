from shift_register import ShiftRegister


class GainBlock:
    def __init__(self, gain: float) -> None:
        self.gain = gain

    def process(self, x: float) -> float:
        return x * self.gain


class DelayBlock:
    def __init__(self, time: float, samplerate: float) -> None:
        self.delay = round(samplerate * time)
        self.register = ShiftRegister(self.delay)

    def process(self, x: float) -> float:
        self.register.shift(x)
        return self.register.at(self.delay - 1)


class FilterBlock:
    def __init__(self) -> None:
        pass

    def process(self, x: float) -> float:
        # TODO: Implement the correct block behaviour
        return x
