from SX127x.LoRa import *
from SX127x.board_config import BOARD
from time import sleep

BOARD.setup()


class GobernantBerry(LoRa):
    n_data_recieved = 0

    def __init__(self, verbose=True, do_calibration=True, calibration_freq=868, sf=7, cr=CODING_RATE.CR4_5, freq=869):
        super(GobernantBerry, self).__init__(verbose, do_calibration, calibration_freq, sf, cr, freq)

    def on_rx_done(self):
        super(GobernantBerry, self).on_rx_done()
        print(bytes(self.payload).decode())

    def start(self):
        sys.stdout.write("\rstart\n")
        self.send("I")
        sleep(0.1)
        self.recv()
        while True:
            sleep(1)


lora = GobernantBerry(verbose=False)
print(lora)

lora.set_pa_config(pa_select=1)
lora.start()
