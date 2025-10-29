import os
import json
import tempfile
import unittest

from A3 import (
    Stats,
    Bulbasaur, Charmander, BasePokemon,
    Pokedex, 
)

class TestSerialization(unittest.TestCase):
    def setUp(self):
        self.dex = Pokedex.get_instance()
        self.dex.entries = []
        self.dex.json_path = ""
        self.dex.text_path = ""
        self.dex.dirty = False

    # Sample pokemon for testing
        self.bulbasaur = Bulbasaur(
            national_no="0001",
            name="Bulbasaur",
            species="Seed Pokémon",
            height_m=0.7,
            weight_kg=6.9,
            abilities=["Overgrow"],
            stats=Stats(45, 49, 49, 65, 65, 45)
        )

        self.charmander = Charmander(
            national_no="0004",
            name="Charmander",
            species="Lizard Pokémon",
            height_m=0.6,
            weight_kg=8.5,
            abilities=["Blaze"],
            stats=Stats(39, 52, 43, 60, 50, 65)
        )

    def test_to_from_dict(self):
        """Test BasePokemon.to_dict() and from_dict() reconstruct the same data."""
        data = self.bulbasaur.to_dict()
        restored = BasePokemon.from_dict(data)
        self.assertEqual(data["name"], restored.to_dict()["name"])
        self.assertEqual(data["type"], restored.to_dict()["type"])
        self.assertEqual(data["stats"], restored.to_dict()["stats"])
        self.assertAlmostEqual(data["height_m"], restored.get_height(), places=2)
        self.assertAlmostEqual(data["weight_kg"], restored.get_weight(), places=2)
    
    def test_json_save_load(self):
        """Test saving to and loading from JSON file."""
        self.dex.add(self.bulbasaur)
        self.dex.add(self.charmander)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmpfile:
            json_path = tmpfile.name

        try:
            self.dex.save_json(json_path)
            # Clear current entries
            self.dex.entries = []
            self.dex.load_json(json_path)

            self.assertEqual(self.dex.count(), 2)
            names = [p.get_name() for p in self.dex.get_entries()]
            self.assertIn("Bulbasaur", names)
            self.assertIn("Charmander", names)
        finally:
            os.remove(json_path)

if __name__ == "__main__":
    unittest.main()