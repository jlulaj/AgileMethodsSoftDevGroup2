import unittest
from readGed import extract_families, extract_individuals
from userStories import us22

class TestUS22(unittest.TestCase):
    def test_us22(self):
        individuals = {
            "I1": {},
            "I2": {},
            "I3": {},
        }

        families = {
            "F1": {},
            "F2": {},
            "F3": {},
        }

        expected_anomalies = [
            "PASSED: US22: All individual IDs and family IDs are unique."
        ]

        # Execute the function
        anomalies = us22(individuals, families)

        # Assert the anomalies
        self.assertEqual(anomalies, expected_anomalies)


if __name__ == "__main__":
    unittest.main()