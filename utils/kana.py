from pygame.image import load

from .settings import Settings


class Kana:
    def __init__(self, table_name):
        self.tables = {
            "hiragana": "assets/hiragana-{}.png",
            "katakana": "assets/katakana-{}.png",
        }
        # store the table_name
        self.table_name = table_name
        # (re)load the kana tables
        self.reload_kana()

    def reload_kana(self):
        # see if we need to use the dark or light kana table
        themes = Settings.get("themes")
        theme = Settings.get("theme")
        background = themes[theme]["background"]
        dark = all(color < 127 for color in background)
        img = self.tables[self.table_name].format("dark" if dark else "light")
        # load the selected asset
        self.asset = load(img).convert_alpha()
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
        # table with all rows in the table
        self.row_table = {
            "-a": {"x": 11, "y": 1},
            "-i": {"x": 11, "y": 2},
            "-u": {"x": 11, "y": 3},
            "-e": {"x": 11, "y": 4},
            "-o": {"x": 11, "y": 5},
        }
        # table with all columns in the table
        self.col_table = {
            "-": {"x": 10, "y": 0},
            "k-": {"x": 9, "y": 0},
            "s-": {"x": 8, "y": 0},
            "t-": {"x": 7, "y": 0},
            "n-": {"x": 6, "y": 0},
            "h-": {"x": 5, "y": 0},
            "m-": {"x": 4, "y": 0},
            "y-": {"x": 3, "y": 0},
            "r-": {"x": 2, "y": 0},
            "w-": {"x": 1, "y": 0},
            "n": {"x": 0, "y": 0},
        }
        self.characters = list(self.table.keys())

        # set kana image size, within the asset, in pixels
        self.size_x = 500
        self.size_y = 625

        # reset the kana table to default and precalculate some properties
        self._reset_kana()

    def _reset_kana(self):
        for character in self.characters:
            self._reset_character(self.table, character)
        for character in list(self.row_table.keys()):
            self._reset_character(self.row_table, character)
        for character in list(self.col_table.keys()):
            self._reset_character(self.col_table, character)

    def _reset_character(self, table, name):
        table[name]["x"] *= self.size_x
        table[name]["y"] *= self.size_y
        table[name]["table_name"] = self.table_name

        # calculate rect; the +/- 10 offsets remove the kana-table borders
        table[name]["rect"] = (
            table[name]["x"] + 10,
            table[name]["y"],
            self.size_x - 10,
            self.size_y - 10,
        )
