import unittest
from readGed import extract_families, extract_individuals
from userStories import us29

class TestUS29(unittest.TestCase):
    def test_us29(self):
        individuals = {
            "I1": {"Name": "John Smith", "Death": "01 Jan 2022"},
            "I2": {"Name": "Jane Doe", "Death": None},
            "I3": {"Name": "Michael Johnson", "Death": "15 Mar 2023"},
        }

        expected_deceased = [
            "Deceased : John Smith (ID: I1)",
            "Deceased : Michael Johnson (ID: I3)"
        ]

        # Execute the function
        deceased = us29(individuals)

        # Assert the deceased individuals
        self.assertEqual(deceased, expected_deceased)


if __name__ == "__main__":
    unittest.main()