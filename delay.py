#!/usr/bin/python

from audio_client import AudioClient
from processing import DelayEffect
from cli import parse_args

args = parse_args()
client = AudioClient("delay")
delay_effect = DelayEffect(args, client.get_samplerate())


@client.set_process_callback
def process(x: float) -> float:
    return delay_effect.process(x)


client.main_loop()
