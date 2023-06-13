import datetime
from readGed import extract_families, extract_individuals

# Read the GEDCOM file
with open("Family_Tree_GEDCOM.ged", "r") as file:
    gedcom_data = file.readlines()

# Convert gedcom_data into an iterator
gedcom_iterator = iter(gedcom_data)
individuals = extract_individuals(gedcom_iterator)
gedcom_iterator = iter(gedcom_data)
families = extract_families(gedcom_iterator)

#print(families)
#print(individuals)

# US01
def us01(families: dict, individuals: dict):
    pass

# US02

# US03

# US04

# US05

# US06

# US07

# US08

# US09

# US10

# US11

# US12

# US13

# US14

# US15
def us15(families: dict, individuals: dict):
    passed = True
    for fid in families.keys():
        if len(families[fid]['Children']) >= 15:
            passed = False
            print("ANAMOLY: FAMILY: US15: " + fid + ": Family has more than 15 siblings (" + str(len(families[fid]['Children'])) + ")")
    if passed:
        print("PASSED: US15: No families with more than 15 siblings")

# US16

# US17

# US18

# US19

# US20

# US21

# US22

# US23

# US24

# US25

# US26

# US27

# US28

# US29

# US30

# US31

# US32

# US33

# US34

# US35

# US36

# US37

# US38

# US39
def us39(families: dict, individuals: dict):
    passed = True
    today = datetime.date.today()

    for fid in families.keys():
        if "Marriage Date" in families[fid].keys():
            temp_date = datetime.datetime.strptime(families[fid]["Marriage Date"], '%d %b %Y')
            temp_date = datetime.date(today.year, temp_date.month, temp_date.day)
            if temp_date - today <= datetime.timedelta(30):
                passed = False
                print("FAMILY: US15: " + fid + ": Wedding anniversary within next 30 days (" + families[fid]["Marriage Date"] + ")")
    if passed:
        print("PASSED: US39: No wedding anniversaries in next 30 days")

# US40

# US41

# US42

def main():
    # will call each user story function here
    pass