import hashlib
import json
import os
import shutil

from pygame import Surface
from pygame.image import save

from utils import Kana, Settings, Theme


class AssetsPreparation:
    cache_dir = "assets/.cache"
    cache_config_file = f"{cache_dir}/cache_config.json"

    def __init__(self):
        # make sure that the cache dir exists
        os.makedirs(self.cache_dir, exist_ok=True)
        # get the files for which the cache has been generated
        self._read_asset_hash()

    def delete_cache(self):
        try:
            shutil.rmtree(self.cache_dir)
        except:
            pass

        # refresh the cached file hashes as the cache has been deleted
        self._read_asset_hash()

    def run(self):
        if self._asset_hash == self._generate_asset_hash():
            print("cache is up to date, no asset preparation needed")
            return

        self.delete_cache()
        # make sure that the cache dir exists
        os.makedirs(self.cache_dir, exist_ok=True)
        self._prepare_asset("hiragana")
        self._prepare_asset("katakana")

        # generate and store the asset hash
        self._asset_hash = self._generate_asset_hash()
        self._write_asset_hash()

    def _read_asset_hash(self):
        try:
            with open(self.cache_config_file) as f:
                cache_config: dict = json.load(f)
                self._asset_hash = cache_config.get("asset_hash", [])
        except:
            self._asset_hash = ""

    def _write_asset_hash(self):
        try:
            with open(self.cache_config_file) as f:
                cache_config = json.load(f)
        except:
            cache_config = {}
        cache_config["asset_hash"] = self._asset_hash
        with open(self.cache_config_file, "w") as f:
            json.dump(cache_config, f)

    def _prepare_asset(self, table_name: str):
        print(f"preparing asset: {table_name}")
        caching_kana = Kana(table_name)
        surface_size = (caching_kana.img_width, caching_kana.img_height)
        caching_surface = Surface(surface_size)
        background_color = Theme.get_color("background")
        for character in caching_kana.characters:
            caching_surface.fill(background_color)
            rect = caching_kana.table[character]["rect"]
            caching_surface.blit(caching_kana.asset, (0, 0), rect)
            filename = f"{self.cache_dir}/{table_name}-{character}.png"
            save(caching_surface, filename)
            print(rect)

    def _generate_asset_hash(self):
        sha1 = hashlib.sha1()
        themes = Settings.get("themes")
        theme = Settings.get("theme")
        background = themes[theme]["background"]
        sha1.update(str(theme).encode("utf-8"))
        sha1.update(str(background).encode("utf-8"))
        return sha1.hexdigest()
