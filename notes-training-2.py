from audio import get_note
from blessings import Terminal
from mingus.core.notes import int_to_note, note_to_int
from mingus.extra.tunings import get_tuning
from random import choice
from time import sleep


tuning = get_tuning('bass', 'standard')
terminal = Terminal()
notes = {int_to_note(i) for i in range(12)}
notes |= {int_to_note(i, 'b') for i in range(12)}
notes = list(notes)
note = choice(notes)
while True:
    print(terminal.clear())
    print(f'{terminal.bold}{note}{terminal.normal}\n')
    while True:
        input_note = get_note(1)
        if input_note:
            print(f'\r{input_note.name}', end=' ', flush=True)
            if note_to_int(note) == note_to_int(input_note.name):
                print(f'{terminal.green_bold}✓{terminal.normal}')
                sleep(2)
                note = choice(notes)
                break
