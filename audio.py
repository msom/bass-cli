from mingus.extra.fft import find_frequencies, find_notes
from operator import itemgetter
from struct import unpack
from pyaudio import PyAudio, paInt16


def find_note(data, freq, bits, treshhold=100000):
    data = find_frequencies(data, freq, bits)
    result = sorted(find_notes(data), key=itemgetter(1))[-1]
    if result[1] >= treshhold:
        return result[0]


def get_note(seconds=1, format=paInt16, channels=1, rate=44100,
             frames_per_buffer=1024):
    audio = PyAudio()
    sample_size = audio.get_sample_size(format)
    frames = int(rate / frames_per_buffer * seconds)
    stream = audio.open(
        format=format,
        channels=channels,
        rate=rate,
        input=True,
        frames_per_buffer=frames_per_buffer
    )
    data = b''
    for i in range(0, frames):
        data += stream.read(frames_per_buffer)
    stream.stop_stream()
    stream.close()
    audio.terminate()

    data = unpack(
        f'{frames * frames_per_buffer * channels}h',
        data
    )
    return find_note(data, rate, sample_size)
