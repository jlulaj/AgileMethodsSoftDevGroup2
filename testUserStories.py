from readGed import extract_families, extract_individuals
import userStories
import unittest

families = userStories.families
individuals = userStories.individuals

# Define test cases
class storyTest(unittest.TestCase):
    
    # Define a test function for each user story here, try to keep in order as we implement

    # US01
    # def test_us01(self):
        # some self.assert statement
    
    # US02
    def test_us02(self):
        self.assertEqual([], userStories.us02(families, individuals))

    # US15
    def test_us15(self):
        self.assertEqual([], userStories.us15(families, individuals))
    
    # US24
    def test_us24(self):
        self.assertEqual([], userStories.us24(families, individuals))

    # US25
    def test_us25(self):
        self.assertEqual([], userStories.us25(families, individuals))
    
    # US33
    def test_us33(self):
        self.assertEqual([], userStories.us33(families, individuals))
    
    # US34
    def test_us34(self):
        self.assertEqual([], userStories.us34(families, individuals))

    # US35
    def test_us35(self):
        self.assertEqual([], userStories.us35(families, individuals))

    # US39
    def test_us39(self):
        self.assertEqual([], userStories.us39(families, individuals))



if __name__ == '__main__':
    # Runs all implemented test functions
    # Write this output to a file (acceptance test results file for submission)
    unittest.main(exit=False, verbosity=2)

