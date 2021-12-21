from mingus.containers import Note
from mingus.extra.fft import find_frequencies, find_notes
from mingus.midi.fluidsynth import init, play_Note, set_instrument, stop_Note
from operator import itemgetter
from pyaudio import PyAudio, paInt16
from struct import unpack
from time import sleep


init('198-JAzz BAzz.sf2')
set_instrument(1, 1)


def play_notes(notes, duration=0.5):
    for note in notes:
        octaved = Note(note)
        octaved.octave_up()
        play_Note(octaved)
        sleep(duration)
        stop_Note(octaved)


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
