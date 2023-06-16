import unittest
from readGed import extract_families, extract_individuals
from userStories import us12
 
class TestUS12(unittest.TestCase):
    def test_us12(self):
        individuals = {
            "I1": {"Birth Date": "01 Jan 1980"},
            "I2": {"Birth Date": "01 Jan 1990"},
            "I3": {"Birth Date": "01 Jan 1960"},
        }

        families = {
            "F1": {
                "Wife ID": "I3",
                "Husband ID": "I1",
                "Children": ["I2"],
            }
        }

        expected_anomalies = [
            "ANOMALY: FAMILY: US12: F1: Mother is 60 or more years older than child (I3 - I2)"
        ]

        # Execute the function
        anomalies = us12(individuals, families)

        # Assert the anomalies
        self.assertEqual(expected_anomalies,anomalies)


if __name__ == "__main__":
    unittest.main()
