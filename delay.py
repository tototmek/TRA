#!/usr/bin/python

import os
import jack
import threading
from processing import DelayEffect
from cli import parse_args

client = jack.Client(os.path.basename(__file__))
inport = client.inports.register("input")
outport = client.outports.register("output")
exit_event = threading.Event()

args = parse_args()
delay_effect = DelayEffect(args, client.samplerate)


def autoconnect_ports():
    default_outports = client.get_ports("system:playback*")
    for port in default_outports:
        client.connect(outport, port)

    default_inports = client.get_ports("file_player:out*")
    if not len(default_inports) == 0:
        client.connect(default_inports[0], inport)
    else:
        default_inports = client.get_ports("system:capture_2")
        if not len(default_inports) == 0:
            client.connect(default_inports[0], inport)


@client.set_process_callback
def process(frames):
    input_buffer = inport.get_array()
    output_buffer = outport.get_array()
    for i in range(len(input_buffer)):
        output_buffer[i] = delay_effect.process(input_buffer[i])


@client.set_shutdown_callback
def shutdown(status, reason):
    print("JACK shutdown.")
    exit_event.set()


with client:
    autoconnect_ports()
    # Wait for termination
    print("Press Ctrl+C to stop.")
    try:
        exit_event.wait()
    except KeyboardInterrupt:
        print(f"\tInterrupted by user.")
