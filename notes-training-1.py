from blessings import Terminal
from fretboard import Fretboard
from getkey import getkey, keys
from mingus.core.notes import int_to_note
from mingus.extra.tunings import get_tuning
from random import choice


tuning = get_tuning('bass', 'standard')
terminal = Terminal()
key = None
show_solution = False
notes = {int_to_note(i) for i in range(12)}
notes |= {int_to_note(i, 'b') for i in range(12)}
notes = list(notes)
note = choice(notes)
while key != 'q':

    if key == keys.RIGHT:
        if show_solution:
            show_solution = False
            note = choice(notes)
        else:
            show_solution = True

    fretboard = Fretboard.from_notes([note], tuning)

    print(terminal.clear())
    print(f'{terminal.bold}{note}{terminal.normal}\n')
    if show_solution:
        fretboard.print(base=note)
    print('\nPress "q" to quit, arrow to progress')

    key = getkey()
