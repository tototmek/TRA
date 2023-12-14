#!/usr/bin/python

import jack
import threading

client = jack.Client("delay")
client.inports.register("signal_in")
client.outports.register("signal_out")
exit_event = threading.Event()


@client.set_process_callback
def process(frames):
    client.outports[0].get_buffer()[:] = client.inports[0].get_buffer()


@client.set_shutdown_callback
def shutdown(status, reason):
    print("JACK shutdown!")
    print("status:", status)
    print("reason:", reason)
    exit_event.set()


with client:
    print("Press Ctrl+C to stop")
    try:
        exit_event.wait()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
