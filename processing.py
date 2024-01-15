from shift_register import ShiftRegister
from params import DelayEffectParams, FilterParams
from scipy import signal
import numpy as np

MAX_DELAY_SAMPLES = 65536
SAMPLE_RATE = 44100


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
        self.register = ShiftRegister(MAX_DELAY_SAMPLES)
        self.set_delay(time)

    def process(self, x: float) -> float:
        self.register.shift(x)
        return self.register.at(self.delay - 1)

    def set_delay(self, time: float) -> None:
        self.delay = max(1, min(MAX_DELAY_SAMPLES, round(self.samplerate * time)))


# TODO: Implement the correct filter block
class FilterBlock:
    def __init__(self, params: FilterParams) -> None:
        self.prev_x = 0
        self.buffer = ShiftRegister(100)
        self.set_params(params)
        self.b, self.a = signal.butter(4, [self.low_freq, self.high_freq], fs=SAMPLE_RATE, btype="band")
        self.sos = signal.tf2sos(self.b, self.a)

    def process(self, x: float) -> float:
        # self.buffer.shift(x)
        # return self.filterness * self.buffer.register[1]
        self.buffer.shift(x)
        a = signal.sosfilt(self.sos, self.buffer.register)
        return a[9]

    def set_params(self, params: FilterParams) -> None:
        self.low_freq = params.low_freq
        self.high_freq = params.high_freq


class DelayEffect:
    def __init__(self, params: DelayEffectParams, samplerate) -> None:
        self.gain1 = GainBlock(params.dry)
        self.gain2 = GainBlock(params.wet)
        self.gain3 = GainBlock(params.feedback)
        self.delay = DelayBlock(params.time, samplerate)
        self.filter = FilterBlock(params.filter)
        self.feedback: float = 0

    # Implementowany układ:
    #
    #   input ----+-------------------- Gain1-------->(+)----> output
    #             |                                    ᐱ
    #             |                                    |
    #             V                                    |
    #            (+)---> Delay ----> Filter ---+---> Gain2
    #             ᐱ                            |
    #             |                            |
    #             |                            |
    #             +----------- Gain3 <---------+
    #
    # 1.Delay – parametr time – wprowadza do sygnału opóźnienie o ustaloną liczbę próbek
    # 2.Filter – parametry brzmienia – filtrowania sygnału
    # 3.Gain2 – parametr wet – kontroluje jak dużo opóźnionego sygnału idzie na output
    # 4.Gain3 – parametr feedback – kontroluje tłumienie każdego kolejnego powtórzenia
    #          danego fragmentu sygnału.
    # 5.Gain1 – parametr dry
    def process(self, x: float) -> float:
        dry_signal = x
        wet_signal = self.filter.process(self.delay.process(dry_signal + self.feedback))
        self.feedback = self.gain3.process(wet_signal)
        y = self.gain1.process(dry_signal) + self.gain2.process(wet_signal)
        return y

    def set_params(self, params: DelayEffectParams):
        self.gain1.set_gain(params.dry)
        self.gain2.set_gain(params.wet)
        self.gain3.set_gain(params.feedback)
        self.delay.set_delay(params.time)
        self.filter.set_params(params.filter)
