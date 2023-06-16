#Kayli Gregory
#I pledge my honor that I have abided by the Stevens Honor System.
import unittest
from readGed import extract_families, extract_individuals
from userStories import us07

class UserStoriesTestCase(unittest.TestCase):
    def test_us07_1(self):
        individuals = {
            "I1": {
                "Birth Date": "26 OCT 1675",
                # Add more individual information as needed
            }
        }
        resultsList = us07(individuals)
        self.maxDiff = None
        self.assertEqual(resultsList, ['ANOMALY: INDIVIDUAL: US07: I1: Current age is over 150 years (348)'])

    def test_us07_2(self):
        individuals = {
            "I1": {
                "Birth Date": "26 OCT 1850",
                "Death Date": "30 SEP 2003" 
               
            }
        }
        resultsList = us07(individuals)
        self.maxDiff = None
        self.assertEqual(resultsList, ['ANOMALY: INDIVIDUAL: US07: I1: Age at death is over 150 years (153)'])

    def test_us07_3(self):
            individuals = {
                "I1": {
                    "Birth Date": "26 OCT 1950",
                    "Death Date": "30 SEP 2003" 
                 }
            }
            resultsList = us07(individuals)
            self.maxDiff = None
            self.assertEqual(resultsList,[])

    def test_us07_4(self):
        individuals = {
            "I1": {
                "Birth Date": "26 OCT 1950",
                "Death Date": "30 SEP 2003" 
              }
        }
        resultsList = us07(individuals)
        self.maxDiff = None
        self.assertEqual(resultsList, [])

    def test_us07_5(self):
        individuals = {
            "I1": {
                "Birth Date": "26 OCT 2200",
            }
        }
        resultsList = us07(individuals)
        self.maxDiff = None
        self.assertEqual(resultsList, [])

# Run the tests
if __name__ == "__main__":
    unittest.main()
