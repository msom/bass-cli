from blessings import Terminal
from getkey import getkey, keys
from mingus.containers import Note
from mingus.core.chords import determine, from_shorthand
from mingus.core.progressions import numerals, to_chords
from mingus.extra.tunings import get_tuning


class FretboardNote(Note):
    def __init__(self, note, string, fret):
        super().__init__(note)
        self.string = string
        self.fret = fret


def get_fretboard(notes, tuning):
    def annotate(note, string, fret):
        result = Note(note)
        result.string = string
        result.fret = fret
        return note

    result = []
    for octave in range(1, 5):
        for note in notes:
            note = Note(note, octave)
            frets = tuning.find_frets(note)
            frets = [
                FretboardNote(note, string, fret)
                for string, fret in enumerate(frets)
            ]
            result.append(frets)

    result = zip(*result)
    result = map(lambda x: [y for y in x if y.fret is not None], result)
    result = map(lambda x: sorted(x), result)
    return list(result)


def print_fretboard(terminal, fretboard, base):

    def format_note(note):
        result = str(note.fret).rjust(2)
        if note.name == base:
            result = f'{terminal.bold}{result}{terminal.normal}'
        return result

    for string in reversed(fretboard):
        line = [' |-'] + 24 * ['------']
        for note in string:
            if note.fret:
                line[note.fret] = f'- {format_note(note)} -'
            else:
                line[note.fret] = f'{format_note(note)}-'
        print(''.join(line))


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
    fretboard = get_fretboard(notes, tuning)

    print(f'{base} {" ".join(progression)}\n')
    if progression:
        print(
            f'{terminal.bold}{chord} {progression[index]} {terminal.normal}\n'
        )
    print_fretboard(terminal, fretboard, notes[0])
    print('\nPress "q" to quit, arrow for scale progression, "r" to restart')

    key = getkey()
