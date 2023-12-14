#!/usr/bin/python

import jack

clientname = "delay"
client = jack.Client(clientname)
client.inports.register(f"signal_in")
client.outports.register(f"signal_out")
inport = client.inports[0]
outport = client.outports[0]


@client.set_process_callback
def process(frames):
    outport.get_buffer()[:] = inport.get_buffer()
    pass


with client:
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print(" Terminated by user")
