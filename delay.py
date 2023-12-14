#!/usr/bin/python

import jack
import threading

client = jack.Client("delay")
inport = client.inports.register("signal_in")
outport = client.outports.register("signal_out")
exit_event = threading.Event()


@client.set_process_callback
def process(frames):
    client.outports[0].get_buffer()[:] = client.inports[0].get_buffer()


@client.set_shutdown_callback
def shutdown(status, reason):
    print("JACK shutdown.")
    exit_event.set()


with client:
    # Quality of life auto-connection:
    default_outports = client.get_ports("system:playback*")
    for port in default_outports:
        client.connect(outport, port)

    default_inports = client.get_ports("file_player:out*")
    if not len(default_inports) == 0:
        client.connect(default_inports[0], inport)

    # Wait for termination
    print("Press Ctrl+C to stop.")
    try:
        exit_event.wait()
    except KeyboardInterrupt:
        print(f"\tInterrupted by user.")
