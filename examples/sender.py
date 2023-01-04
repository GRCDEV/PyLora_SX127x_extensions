from PyLora_SX127x_extensions.pyLora import pyLora

try:
    pyLora = pyLora(verbose=True, freq=867)
    pyLora.send(b'Hello world!')
except KeyboardInterrupt:
    print("Closing pyLora...")