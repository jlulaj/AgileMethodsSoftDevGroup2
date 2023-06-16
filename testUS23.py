import unittest
from readGed import extract_families, extract_individuals
from userStories import us23


class TestUS23(unittest.TestCase):
    def test_us23(self):
        individuals = {
            "I1": {"Name": "John Smith", "Birth Date": "01 Jan 1990"},
            "I2": {"Name": "Jane Doe", "Birth Date": "02 Feb 1985"},
            "I3": {"Name": "John Smith", "Birth Date": "01 Jan 1990"},
        }

        expected_anomalies = [
            "ANOMALY: INDIVIDUAL: US23: I3: Duplicate individual with the same name and birth date"
        ]

        # Execute the function
        anomalies = us23(individuals)

        # Assert the anomalies
        self.assertEqual(anomalies, expected_anomalies)


if __name__ == "__main__":
    unittest.main()