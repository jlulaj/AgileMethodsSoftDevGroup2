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
        self.assertEqual([], userStories.us03(families, individuals))
    
    # US04
    def test_us04(self):
        self.assertEqual([], userStories.us04(families, individuals))

    # US05
    def test_us05(self):
        self.assertEqual([], userStories.us05(families, individuals))

    # US06
    def test_us06(self):
        self.assertEqual([], userStories.us06(families, individuals))

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

    # US12
    def test_us12(self):
        self.assertEqual([], userStories.us12(families, individuals))
    
    # US13
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

    # US21
    def test_us21(self):
        self.assertEqual([], userStories.us21(families, individuals))

    # US22
    def test_us22(self):
        self.assertEqual([], userStories.us22(families, individuals))

    # US23
    def test_us23(self):
        self.assertEqual([], userStories.us23(families, individuals))
    
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
    
    # US32
    def test_us32(self):
        individuals = {"IND1": {"Birth Date": "2000-01-01"}, "IND2": {"Birth Date": "2000-01-01"}, "IND3": {"Birth Date": "2005-05-15"}, "IND4": {"Birth Date": "1995-03-20"}, "IND5": {"Birth Date": "2000-01-01"}}
    
    # US33
    def test_us33(self):
        self.assertEqual([], userStories.us33(families, individuals))
    
    # US34
    def test_us34(self):
        self.assertEqual([], userStories.us34(families, individuals))

    # US35
    def test_us35(self):
        self.assertEqual([], userStories.us35(families, individuals))

    # US36
    def test_us36(self):
        self.assertEqual([], userStories.us36(families, individuals))
    
    # US37
    def test_us37(self):
        self.assertEqual({}, userStories.us37(individuals, families))

    # US38
    def test_us38(self):
        self.assertEqual([], userStories.us38(families, individuals))

    # US39
    def test_us39(self):
        self.assertEqual(['F6'], userStories.us39(families, individuals))
    
    # US40
    def test_us40(self):
           errors = {10: "Invalid date format", 25: "Date out of range", 30: "Incorrect date value"}

    # US41
    def test_us41(self):
        dates = {"DATE1": "1990 15", "DATE2": "20 2005", "DATE3": "3000 2022", "DATE4": "12345 2023", "DATE5": "FEB 2021", "DATE6": "05 DEC 1998"}

        corrected_dates = userStories.us41(dates)

    # US42
    def test_us42(self):
        self.assertEqual([], userStories.us42(families, individuals))



if __name__ == '__main__':
    # Runs all implemented test functions
    # Write this output to a file (acceptance test results file for submission)
    unittest.main(exit=False, verbosity=2)

