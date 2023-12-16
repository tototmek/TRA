from shift_register import ShiftRegister

MAX_DELAY_SAMPLES = 65536


class GainBlock:
    def __init__(self, gain: float) -> None:
        self.set_gain(gain)

    def process(self, x: float) -> float:
        return x * self.gain

    def set_gain(self, gain: float) -> None:
        self.gain = gain


class DelayBlock:
    def __init__(self, time: float, samplerate: float) -> None:
        self.samplerate = samplerate
        self.set_delay(time)
        self.register = ShiftRegister(MAX_DELAY_SAMPLES)

    def process(self, x: float) -> float:
        self.register.shift(x)
        return self.register.at(self.delay - 1)

    def set_delay(self, time: float) -> None:
        self.delay = max(1, min(MAX_DELAY_SAMPLES, round(self.samplerate * time)))


class FilterBlock:
    def __init__(self) -> None:
        self.prev_x = 0

    def process(self, x: float) -> float:
        # TODO: Implement the correct block behaviour
        return 0.8 * self.prev_x + 0.2 * x
