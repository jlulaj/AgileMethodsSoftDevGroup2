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
def us07(individuals: dict):
    today = datetime.date.today()

    for indiID, indiInfo in individuals.items():
        if "Death Date" in indiInfo:
            death_date = datetime.datetime.strptime(indiInfo["Death Date"], "%d %b %Y").date()
            age_at_death = death_date.year - datetime.datetime.strptime(indiInfo["Birth Date"], "%d %b %Y").date().year

            if age_at_death > 150:
                print(f"ANOMALY: INDIVIDUAL: US07: {indiID}: Age at death is over 150 years ({age_at_death})")
        else:
            birth_date = datetime.datetime.strptime(indiInfo["Birth Date"], "%d %b %Y").date()
            age = today.year - birth_date.year

            if age > 150:
                print(f"ANOMALY: INDIVIDUAL: US07: {indiID}: Current age is over 150 years ({age})")
    

# US08

# US09

# US10

# US11

# US12
def us12(individuals: dict, families: dict):
    for famID, famInfo in families.items():
        children = famInfo.get("Children", [])
        mother_id = famInfo.get("Wife ID")
        father_id = famInfo.get("Husband ID")

        if mother_id and father_id:
            mother_birth_date = individuals[mother_id].get("Birth Date")
            father_birth_date = individuals[father_id].get("Birth Date")

            for child_id in children:
                child_birth_date = individuals[child_id].get("Birth Date")

                if mother_birth_date and child_birth_date:
                    if calculate_age_difference(mother_birth_date, child_birth_date) >= 60:
                        print(f"ANOMALY: FAMILY: US12: {famID}: Mother is 60 or more years older than child ({mother_id} - {child_id})")

                if father_birth_date and child_birth_date:
                    if calculate_age_difference(father_birth_date, child_birth_date) >= 80:
                        print(f"ANOMALY: FAMILY: US12: {famID}: Father is 80 or more years older than child ({father_id} - {child_id})")

def calculate_age_difference(date1: str, date2: str) -> int:
    birth_date = datetime.datetime.strptime(date1, "%d %b %Y").date()
    other_date = datetime.datetime.strptime(date2, "%d %b %Y").date()
    age_difference = (other_date - birth_date).days // 365
    return age_difference

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
def us21(families: dict, individuals: dict) -> list:
    for fid in families.items():
        husband_id = families[fid].get("Husband ID")
        wife_id = families[fid].get("Wife ID")
        if husband_id and wife_id:
            husband_gender = individuals[husband_id].get("SEX")
            wife_gender = individuals[wife_id].get("SEX")

            if husband_gender != "M":
                print(f"Anomaly in family: Incorrect gender role for husband {husband_id}")

            if wife_gender != "F":
                print(f"Anomaly in family: Incorrect gender role for wife {wife_id}")
                
# US22
def us22(individuals: dict, families: dict):
    individual_ids = set()
    family_ids = set()
    passed = True

    for indiID in individuals.keys():
        if indiID in individual_ids:
            passed = False
            print(f"ANOMALY: INDIVIDUAL: US22: {indiID}: Duplicate individual ID found")
        else:
            individual_ids.add(indiID)

    for famID in families.keys():
        if famID in family_ids:
            passed = False
            print(f"ANOMALY: FAMILY: US22: {famID}: Duplicate family ID found")
        else:
            family_ids.add(famID)

    if passed:
        print("PASSED: US22: All individual IDs and family IDs are unique.")

# US23
def us23(individuals: dict):
    passed = True
    unique_individuals = set()

    for indiID, indiInfo in individuals.items():
        name = indiInfo["Name"]
        birth_date = indiInfo["Birth Date"]

        # Concatenate name and birth date to create a unique identifier
        identifier = f"{name}-{birth_date}"

        if identifier in unique_individuals:
            passed = False
            print(f"ANOMALY: INDIVIDUAL: US23: {indiID}: Duplicate individual with the same name and birth date")
        else:
            unique_individuals.add(identifier)

    if passed:
        print("PASSED: US23: No more than one individual with the same name and birth date in the GEDCOM file.")

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
def bdayWithin30Days(birthday):
    today = datetime.date.today()
    next_30_days = today + datetime.timedelta(days=30)
    birthday_this_year = birthday.replace(year=today.year)

    if today <= birthday_this_year <= next_30_days:
        return True
    else:
        return False

def us38(individuals: dict):
    passed = True
    bdayList = []

    
    for indiID, indiInfo in individuals.items():
        if indiInfo.get("Alive", True) and "Birth Date" in indiInfo:
            birth_date = datetime.datetime.strptime(indiInfo["Birth Date"], "%d %b %Y").date()
            if bdayWithin30Days(birth_date):
                bdayList.append(indiInfo["Name"])
        
    if len(bdayList) > 0:
        print("US38: Individuals whose birthdays are coming up in the next 30 days: " + str(bdayList))   
    else: 
        print("PASSED: US38: No upcoming birthdays in the next 30 days")

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
