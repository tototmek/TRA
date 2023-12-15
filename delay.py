#!/usr/bin/python

import jack
import threading

client = jack.Client("delay")
inport = client.inports.register("signal_in")
outport = client.outports.register("signal_out")
exit_event = threading.Event()


# Proponowany układ:
#
#   input ----+------------------------5.Gain1-------->(+)---->output
#             |                                         ᐱ
#             |                                         |
#             V                                         |
#            (+)---> 1.Delay ----> 2.Filter ---+---> 3.Gain2
#             ᐱ                                |
#             |                                |
#             |                                |
#             +----------- 4.Gain3 ------------+
#
# 1.Delay – parametr time – wprowadza do sygnału opóźnienie o pewną liczbę próbek
# 2.Filter – parametry brzmienia – moim zdaniem najlepiej jakiś filtr noi,
#            regulowane parametry, konieczne wyliczanie parametrów filtru
#            w locie, być może podział na sekcje bikwadratowe czy coś takiego, idk
#           kolejność delaya i filtru można dowolnie zamieniać
# 3.Gain2 – parametr wet – kontroluje jak dużo opóźnionego sygnału idzie na output
# 4.Gain3 – parametr feedback – kontroluje tłumienie każdego kolejnego powtórzenia
#          danego fragmentu sygnału.
# 5.Gain1 – parametr dry
#                                           ᐱ
#                                           |
@client.set_process_callback  #             |
def process(frames):  #                     |
    # TODO: Tu zaimplementować to: ---------+
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
