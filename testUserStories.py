from readGed import extract_families, extract_individuals
import userStories
import unittest

families = userStories.families
individuals = userStories.individuals

# Define test cases
class storyTest(unittest.TestCase):
    
    # Define a test function for each user story here, try to keep in order as we implement

    # US01
    def test_us01(self):
        self.assertEqual([], userStories.us01(families, individuals))
    
    # US02
    def test_us02(self):
        self.assertEqual([], userStories.us02(families, individuals))

    # US03
    def test_us03(self):
        self.assertEqual([], userStories.us02(families, individuals))
    
    # US04
    def test_us04(self):
        self.assertEqual([], userStories.us04(families, individuals))

    # US05
    def test_us05(self):
        self.assertEqual([], userStories.us05(families, individuals))

    # US06
    def test_us02(self):
        self.assertEqual([], userStories.us02(families, individuals))

    # US07
    def test_us07(self):
        self.assertEqual([], userStories.us07(families, individuals))

    # US08
    def test_us08(self):
        self.assertEqual(['I17'], userStories.us08(families, individuals))
        
    # US09
    def test_us09(self):
        self.assertEqual([], userStories.us09(families, individuals))
        
    # US10
    def test_us10(self):
        self.assertEqual([], userStories.us10(families, individuals))

    # US11
    def test_us11(self):
        self.assertEqual([], userStories.us11(families, individuals))

    # US14
    def test_us13(self):
        self.assertEqual([], userStories.us13(families, individuals))
        
    # US14
    def test_us14(self):
        self.assertEqual([], userStories.us14(families, individuals))
        
    # US15
    def test_us15(self):
        self.assertEqual([], userStories.us15(families, individuals))
    
    # US16
    def test_us16(self):
        self.assertEqual([], userStories.us16(families, individuals))
    
    # US17
    def test_us17(self):
        self.assertEqual([], userStories.us17(families, individuals))

    # US18
    def test_us18(self):
        self.assertEqual([], userStories.us18(families, individuals))
    
    # US19
    def test_us19(self):
        self.assertEqual([], userStories.us19(families, individuals))
    
    # US20
    def test_us20(self):
        self.assertEqual([], userStories.us20(families, individuals))
        
    # US24
    def test_us24(self):
        self.assertEqual([], userStories.us24(families, individuals))

    # US25
    def test_us25(self):
        self.assertEqual([], userStories.us25(families, individuals))
    
    # US26
    def test_us26(self):
        self.assertEqual([set(), set()], userStories.us26(families, individuals))

    # US27
    def test_us27(self):
        self.assertEqual([], userStories.us27(families, individuals))
    
    # US28
    def test_us28(self):
        self.assertEqual({'F1': ['I12'], 'F2': ['I1', 'I5'], 'F3': ['I8', 'I9'], 'F4': ['I10', 'I11'], 'F5': ['I19'], 'F6': ['I17', 'I16'], 'F7': ['I15']},
                            userStories.us28(families, individuals))

    # US29
    def test_us29(self):
        self.assertEqual([], userStories.us29(families, individuals))
        
    # US30
    def test_us30(self):
        self.assertEqual([], userStories.us30(families, individuals))

    # US31
    def test_us31(self):
        self.assertEqual([], userStories.us31(families, individuals))
    
    # US33
    def test_us33(self):
        self.assertEqual([], userStories.us33(families, individuals))
    
    # US34
    def test_us34(self):
        self.assertEqual([], userStories.us34(families, individuals))

    # US35
    def test_us35(self):
        self.assertEqual([], userStories.us35(families, individuals))
    
    # US38
    def test_us38(self):
        self.assertEqual([], userStories.us38(families, individuals))

    # US39
    def test_us39(self):
        self.assertEqual(['F6'], userStories.us39(families, individuals))

    # US42
    def test_us42(self):
        self.assertEqual([], userStories.us42(families, individuals))



if __name__ == '__main__':
    # Runs all implemented test functions
    # Write this output to a file (acceptance test results file for submission)
    unittest.main(exit=False, verbosity=2)

