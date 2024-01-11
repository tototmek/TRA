import jack
import threading


class AudioClient:
    def __init__(self, name) -> None:
        self.jack_client = jack.Client(name)
        self.inport = self.jack_client.inports.register("input")
        self.outport = self.jack_client.outports.register("output")
        self.exit_event = threading.Event()
        self.jack_client.set_shutdown_callback(lambda: self.exit_event.set())

    def main_loop(self):
        with self.jack_client:
            self.autoconnect_ports()
            print("Press Ctrl+C to stop.")
            try:
                self.exit_event.wait()
            except KeyboardInterrupt:
                print(f"\tInterrupted by user.")

    def set_process_callback(self, function):
        def process_callback(_):
            input_buffer = self.inport.get_array()
            output_buffer = self.outport.get_array()
            for i in range(len(input_buffer)):
                output_buffer[i] = function(input_buffer[i])

        self.jack_client.set_process_callback(process_callback)

    def autoconnect_ports(self):
        default_outports = self.jack_client.get_ports("system:playback*")
        for port in default_outports:
            self.jack_client.connect(self.outport, port)
        default_inports = self.jack_client.get_ports("file_player:out*")
        if not len(default_inports) == 0:
            self.jack_client.connect(default_inports[0], self.inport)
        else:
            default_inports = self.jack_client.get_ports("system:capture_2")
            if not len(default_inports) == 0:
                self.jack_client.connect(default_inports[0], self.inport)

    def get_samplerate(self):
        return self.jack_client.samplerate
