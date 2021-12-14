from blessings import Terminal
from mingus.containers import Note


class FretboardNote(Note):

    """ A note with additional string and fret informations. """

    def __init__(self, note, string, fret):
        super().__init__(note)
        self.string = string
        self.fret = fret


class Fretboard:

    """ A fretboard. """

    def __init__(self, strings=[]):
        self.strings = strings

    @classmethod
    def from_notes(cls, notes, tuning):
        result = []
        min_octave = tuning.tuning[0].octave
        max_octave = tuning.tuning[-1].octave + 2
        for octave in range(min_octave, max_octave + 1):
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
        return cls(list(result))

    def print(self, base=None):
        """ Print the fretboard as ASCII characters.

        Optionally accepts a base note (as string) for highlighting.

        """

        terminal = Terminal()

        def format_note(note):
            result = str(note.fret).rjust(2)
            if base and note.name == base:
                result = f'{terminal.bold}{result}{terminal.normal}'
            return result

        for string in reversed(self.strings):
            line = [' |-'] + 24 * ['------']
            for note in string:
                if note.fret:
                    line[note.fret] = f'- {format_note(note)} -'
                else:
                    line[note.fret] = f'{format_note(note)}-'
            print(''.join(line))
