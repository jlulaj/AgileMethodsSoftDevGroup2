import unittest
from datetime import datetime
from userStories import us38
import io 
import sys 

class TestUS38(unittest.TestCase):
    def test_us38(self):
        individuals = {
            "I1": {
                "Name": "John Doe",
                "Birth Date": "01 Jan 1990"
            },
            "I2": {
                "Name": "Jane Smith",
                "Birth Date": "15 Jun 1985"
            },
            "I3": {
                "Name": "Michael Johnson",
                "Birth Date": "10 Feb 2000"
            }
        }

        expected_upcoming_birthdays = [
            "John Doe",
            "Jane Smith"
        ]

        # Redirect print statements to capture the output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the function
        us38(individuals)

        # Restore sys.stdout
        sys.stdout = sys.__stdout__

        # Get the captured output
        output = captured_output.getvalue().strip()

        # Split the output into a list of lines
        output_lines = output.split("\n")

        # Extract the names from the output lines
        upcoming_birthdays = [line.split(": ")[1] for line in output_lines]

        self.assertEqual(upcoming_birthdays, expected_upcoming_birthdays)


if __name__ == "__main__":
    unittest.main()
