from pygame.image import load


class Kana:
    def __init__(self, table_name):
        self.tables = {
            "hiragana": "assets/hiragana.png",
            "katakana": "assets/katakana.png",
        }
        # store the table_name
        self.table_name = table_name
        # load the selected asset
        self.asset = load(self.tables[table_name]).convert_alpha()
        # generate the kana table and properties
        self._generate_kana()

    def _generate_kana(self):
        # generate the kana table
        # character: row offset, column offset
        self.table = {
            "a": {"x": 10, "y": 1},
            "i": {"x": 10, "y": 2},
            "u": {"x": 10, "y": 3},
            "e": {"x": 10, "y": 4},
            "o": {"x": 10, "y": 5},
            "ka": {"x": 9, "y": 1},
            "ki": {"x": 9, "y": 2},
            "ku": {"x": 9, "y": 3},
            "ke": {"x": 9, "y": 4},
            "ko": {"x": 9, "y": 5},
            "sa": {"x": 8, "y": 1},
            "shi": {"x": 8, "y": 2},
            "su": {"x": 8, "y": 3},
            "se": {"x": 8, "y": 4},
            "so": {"x": 8, "y": 5},
            "ta": {"x": 7, "y": 1},
            "chi": {"x": 7, "y": 2},
            "tsu": {"x": 7, "y": 3},
            "te": {"x": 7, "y": 4},
            "to": {"x": 7, "y": 5},
            "na": {"x": 6, "y": 1},
            "ni": {"x": 6, "y": 2},
            "nu": {"x": 6, "y": 3},
            "ne": {"x": 6, "y": 4},
            "no": {"x": 6, "y": 5},
            "ha": {"x": 5, "y": 1},
            "hi": {"x": 5, "y": 2},
            "fu": {"x": 5, "y": 3},
            "he": {"x": 5, "y": 4},
            "ho": {"x": 5, "y": 5},
            "ma": {"x": 4, "y": 1},
            "mi": {"x": 4, "y": 2},
            "mu": {"x": 4, "y": 3},
            "me": {"x": 4, "y": 4},
            "mo": {"x": 4, "y": 5},
            "ya": {"x": 3, "y": 1},
            "yu": {"x": 3, "y": 3},
            "yo": {"x": 3, "y": 5},
            "ra": {"x": 2, "y": 1},
            "ri": {"x": 2, "y": 2},
            "ru": {"x": 2, "y": 3},
            "re": {"x": 2, "y": 4},
            "ro": {"x": 2, "y": 5},
            "wa": {"x": 1, "y": 1},
            "wi": {"x": 1, "y": 2},
            "we": {"x": 1, "y": 4},
            "wo": {"x": 1, "y": 5},
            "n": {"x": 0, "y": 1},
        }
        self.characters = list(self.table.keys())

        # set kana offsets within picture
        self.size_x = 500
        self.size_y = 625

        # reset the kana table to default (all selected and add table_name)
        self._reset_kana()

    def _reset_kana(self):
        for character in self.characters:
            self.table[character]["x"] *= self.size_x
            self.table[character]["y"] *= self.size_y
            self.table[character]["table_name"] = self.table_name
            self.table[character]["selected"] = True  # TODO: settings file
