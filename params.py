class FilterParams:
    low_freq: float
    high_freq: float


class DelayEffectParams:
    time: float
    dry: float
    wet: float
    feedback: float
    filter: FilterParams
