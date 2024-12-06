import math


chord_dictionary = {
    "C": {"C", "E", "G"},
    "Cm": {"C", "D♯", "G"},
    "C7": {"C", "E", "G", "A♯"},
    "Cm7": {"C", "D♯", "G", "A♯"},
    "Cmaj7": {"C", "E", "G", "B"},
    "Cdim": {"C", "D♯", "F♯"},
    "Caug": {"C", "E", "G♯"},
    "C6": {"C", "E", "G", "A"},
    "C9": {"C", "E", "G", "A♯", "D"},
    "D": {"D", "F♯", "A"},
    "Dm": {"D", "F", "A"},
    "D7": {"D", "F♯", "A", "C"},
    "Dm7": {"D", "F", "A", "C"},
    "Dmaj7": {"D", "F♯", "A", "C♯"},
    "Ddim": {"D", "F", "G♯"},
    "Daug": {"D", "F♯", "A♯"},
    "D6": {"D", "F♯", "A", "B"},
    "D9": {"D", "F♯", "A", "C", "E"},
    "E": {"E", "G♯", "B"},
    "Em": {"E", "G", "B"},
    "E7": {"E", "G♯", "B", "D"},
    "Em7": {"E", "G", "B", "D"},
    "Emaj7": {"E", "G♯", "B", "D♯"},
    "Edim": {"E", "G", "A♯"},
    "Eaug": {"E", "G♯", "C"},
    "E6": {"E", "G♯", "B", "C♯"},
    "E9": {"E", "G♯", "B", "D", "F♯"},
    "F": {"F", "A", "C"},
    "Fm": {"F", "G♯", "C"},
    "F7": {"F", "A", "C", "D♯"},
    "Fm7": {"F", "G♯", "C", "D♯"},
    "Fmaj7": {"F", "A", "C", "E"},
    "Fdim": {"F", "G♯", "B"},
    "Faug": {"F", "A", "C♯"},
    "F6": {"F", "A", "C", "D"},
    "F9": {"F", "A", "C", "D♯", "G"},
    "G": {"G", "B", "D"},
    "Gm": {"G", "A♯", "D"},
    "G7": {"G", "B", "D", "F"},
    "Gm7": {"G", "A♯", "D", "F"},
    "Gmaj7": {"G", "B", "D", "F♯"},
    "Gdim": {"G", "A♯", "C♯"},
    "Gaug": {"G", "B", "D♯"},
    "G6": {"G", "B", "D", "E"},
    "G9": {"G", "B", "D", "F", "A"},
    "A": {"A", "C♯", "E"},
    "Am": {"A", "C", "E"},
    "A7": {"A", "C♯", "E", "G"},
    "Am7": {"A", "C", "E", "G"},
    "Amaj7": {"A", "C♯", "E", "G♯"},
    "Adim": {"A", "C", "D♯"},
    "Aaug": {"A", "C♯", "F"},
    "A6": {"A", "C♯", "E", "F♯"},
    "A9": {"A", "C♯", "E", "G", "B"},
    "B": {"B", "D♯", "F♯"},
    "Bm": {"B", "D", "F♯"},
    "B7": {"B", "D♯", "F♯", "A"},
    "Bm7": {"B", "D", "F♯", "A"},
    "Bmaj7": {"B", "D♯", "F♯", "A♯"},
    "Bdim": {"B", "D", "F"},
    "Baug": {"B", "D♯", "G"},
    "B6": {"B", "D♯", "F♯", "G♯"},
    "B9": {"B", "D♯", "F♯", "A", "C♯"},
}

notation_dictionary = {
    "C": "До",
    "D": "Ре",
    "E": "Ми",
    "F": "Фа",
    "G": "Соль",
    "A": "Ля",
    "B": "Си",
}


class Octave:
    def __init__(self, number: int = 4):
        self.number = number

    def __str__(self):
        return str(self.number)

    @classmethod
    def from_notation(cls, notation: str) -> "Octave":
        try:
            return cls(int(notation))
        except ValueError:
            return cls()


class Note:
    alteration_mapping = {"♯": "диез", "b": "бемоль", "": ""}
    reference_note = 440.0
    semitone_ratio = 2 ** (1 / 12)
    note_names = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]

    def __init__(self, name: str, octave: Octave = Octave(), alteration: str = ""):
        self.name = name
        self.octave = octave
        self.alteration = alteration

    def __str__(self):
        return f"{self.name}{self.alteration}{self.octave}"

    def to_notation(self) -> str:
        return f"{self.name}{self.alteration}{self.octave}"

    def to_human_readable(self) -> str:
        human_alteration = self.alteration_mapping.get(self.alteration, self.alteration)
        human_name = notation_dictionary.get(self.name, self.name)
        return f"{human_name} {human_alteration} {self.octave}".strip()

    @classmethod
    def from_notation(cls, note: str) -> "Note":
        base = note.rstrip("0123456789")
        octave_part = note[len(base) :]
        octave = Octave.from_notation(octave_part) if octave_part else Octave()

        if len(base) > 1 and base[1] in "♯b":
            name, alteration = base[0], base[1]
        else:
            name, alteration = base, ""

        return cls(name=name, octave=octave, alteration=alteration)

    @classmethod
    def from_hz(cls, frequency: float) -> "Note":
        if frequency <= 0:
            raise ValueError("Frequency must be greater than zero.")

        semitones_from_a4 = round(12 * math.log2(frequency / cls.reference_note))
        note_index = (semitones_from_a4 + 9) % 12
        octave = 4 + (semitones_from_a4 + 9) // 12
        note_name = cls.note_names[note_index]

        return cls(name=note_name, octave=Octave(octave))

    def __eq__(self, other):
        return (
            isinstance(other, Note)
            and self.name == other.name
            and self.octave == other.octave
            and self.alteration == other.alteration
        )


class Chord:
    suffix_mapping = {
        "m": "минор",
        "": "мажор",
        "dim": "уменьшённый",
        "aug": "увеличенный",
        "7": "септаккорд",
        "6": "секстаккорд",
        "9": "нон-аккорд",
    }

    def __init__(self, name: str, notes: list[Note]):
        self.name = name
        self.notes = notes

    def __str__(self):
        return f"{self.name}: {', '.join(str(note) for note in self.notes)}"

    def to_human_readable(self) -> str:
        tonic = ""
        suffix = ""

        for i, char in enumerate(self.name):
            if char.isdigit() or char in "maugdim":
                tonic = self.name[:i]
                suffix = self.name[i:]
                break
        else:
            tonic = self.name

        human_tonic = notation_dictionary.get(tonic, tonic)
        human_suffix = self.suffix_mapping.get(suffix, suffix)
        notes_readable = ", ".join(note.to_human_readable() for note in self.notes)

        return f"{human_tonic} {human_suffix}: {notes_readable}"

    def contains_notes(self, notes: list[Note]) -> int:
        return sum(1 for note in notes if note in self.notes)

    @classmethod
    def from_notation(cls, name: str) -> "Chord":
        chord_notes = chord_dictionary.get(name, [])
        notes = [Note.from_notation(note) for note in chord_notes]
        return cls(name=name, notes=notes)
