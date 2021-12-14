from blessings import Terminal
from fretboard import Fretboard
from getkey import getkey, keys
from mingus.core.chords import determine, from_shorthand
from mingus.core.progressions import numerals, to_chords
from mingus.extra.tunings import get_tuning


def input_chord():
    choice = input('Enter a chord ("Am7") or a base and optional a '
                   'progression ("A", "A I VIIdim7", "A"): ').split(' ')
    choice = [item.strip() for item in choice if item.strip()]
    chord = choice[0] if choice else ''
    notes = from_shorthand(chord)
    base = notes[0]
    progression = choice[1:]
    if not progression and notes == from_shorthand(base):
        progression = numerals
    return chord, notes, base, progression


tuning = get_tuning('bass', 'standard')
terminal = Terminal()
key = None
while key != 'q':
    print(terminal.clear())

    if key in ('r', None):
        chord, notes, base, progression = input_chord()
        index = 0
        print(terminal.clear())

    if key in (keys.LEFT, keys.RIGHT):
        index = (index + (1 if key == keys.RIGHT else -1)) % len(progression)
        new = to_chords([progression[index]], base)[0]
        chord = determine(new, base, True)[0]

    notes = from_shorthand(chord)
    fretboard = Fretboard.from_notes(notes, tuning)

    print(f'{base} {" ".join(progression)}\n')
    if progression:
        print(
            f'{terminal.bold}{chord} {progression[index]} {terminal.normal}\n'
        )
    fretboard.print(base=notes[0])
    print('\nPress "q" to quit, arrow for scale progression, "r" to restart')

    key = getkey()
