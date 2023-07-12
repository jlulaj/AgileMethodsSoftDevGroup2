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
    
    # US15
    def test_us15(self):
        self.assertEqual([], userStories.us15(families, individuals))
    
    # US39
    def test_us39(self):
        self.assertEqual([], userStories.us39(families, individuals))



if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)

