from blessings import Terminal
from getkey import getkey, keys
from mingus.containers import Note
from mingus.core.chords import from_shorthand, determine
from mingus.core.progressions import skip, to_chords
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
        # todo: use color
        line = [' |-'] + 24 * ['------']
        for note in string:
            if note.fret:
                line[note.fret] = f'- {format_note(note)} -'
            else:
                line[note.fret] = f'{format_note(note)}-'
        print(''.join(line))


tuning = get_tuning('bass', 'standard')
terminal = Terminal()
chord = input('Enter chord: ')
base = chord
progression = 'I'
key = None
while key != 'q':
    notes = from_shorthand(chord)
    fretboard = get_fretboard(notes, tuning)

    print(terminal.clear())
    print(f'{chord} {progression}\n')
    print_fretboard(terminal, fretboard, notes[0])
    print('')
    print('Press "q" to quit, arrow up/down for scale progression')

    key = getkey()
    if key in (keys.LEFT, keys.RIGHT):
        progression = skip(progression, 1 if key == keys.RIGHT else -1)
        new = to_chords([progression], base)[0]
        chord = determine(new, base, True)[0]
