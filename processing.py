class GainBlock:
    def __init__(self, gain: float) -> None:
        self.gain = gain

    def process(self, x: float) -> float:
        return x * self.gain


class DelayBlock:
    def __init__(self, time: float, samplerate: float) -> None:
        self.delay = round(samplerate * time)
        self.samples = [0 for _ in range(self.delay)]

    def process(self, x: float) -> float:
        # za wolne
        for i in range(1, len(self.samples)):
            self.samples[i] = self.samples[i - 1]
        self.samples[0] = x
        return self.samples[self.delay - 1]


class FilterBlock:
    def __init__(self) -> None:
        pass

    def process(self, x: float) -> float:
        # TODO: Implement the correct block behaviour
        return x
