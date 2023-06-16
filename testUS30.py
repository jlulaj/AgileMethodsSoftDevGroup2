import unittest
from readGed import extract_families, extract_individuals
from userStories import us30
import io
import sys

class TestUS30(unittest.TestCase):
    def test_us30(self):
        individuals = {
            "I1": {"Name": "John Doe", "Death": "10 Jan 2020"},
            "I2": {"Name": "Jane Doe", "Death": None},
            "I3": {"Name": "Michael Johnson", "Death": None}
        }

        families = {
            "F1": {"Husband ID": "I1", "Wife ID": "I2"},
            "F2": {"Husband ID": "I3", "Wife ID": "I2"}
        }

        expected_output = [
            "Living Married: Michael Johnson (ID: I3)"
        ]

        # Create a stream to capture the output of the function
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Execute the function
        us30(families, individuals)

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Get the captured output
        actual_output = captured_output.getvalue().strip().split('\n')

        # Assert the output
        self.assertEqual(actual_output, expected_output)

if __name__ == "__main__":
    unittest.main()