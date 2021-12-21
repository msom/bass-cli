from audio import play_notes
from blessings import Terminal
from fretboard import Fretboard
from getkey import getkey, keys
from mingus.containers import Note
from mingus.extra.tunings import get_tuning
from random import sample


tuning = get_tuning('bass', 'standard')
notes = [
    Note(value)
    for value in range(int(tuning.tuning[0]), int(tuning.tuning[-1]) + 25)
]
terminal = Terminal()
print(terminal.clear())
key = None
show = False
length = 3
melody = sample(notes, length)

print(
    '\nPress "q" to quit, left arrow to play again, '
    'right arrow for solution, "r" to restarts'
)

play_notes(melody)

while key != 'q':

    if key == keys.LEFT:
        play_notes(melody)

    if key == keys.RIGHT and not show:
        show = True
        for note in melody:
            print(f'\n{note.name}-{note.octave}')
            fretboard = Fretboard.from_notes([note], tuning)
            fretboard.print()

    if key == 'r':
        print(terminal.clear())
        show = False
        melody = sample(notes, length)
        play_notes(melody)

    key = getkey()
