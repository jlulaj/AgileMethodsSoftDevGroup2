from datetime import datetime, timedelta
from readGed import extract_families, extract_individuals
import readGed
import datetime

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
def us07(families: dict, individuals: dict):
    passed = True
    today = datetime.date.today()

    for indiID, indiInfo in individuals.items():
        if "Death Date" in indiInfo:
            death_date = datetime.datetime.strptime(indiInfo["Death Date"], "%d %b %Y").date()
            age_at_death = death_date.year - datetime.datetime.strptime(indiInfo["Birth Date"], "%d %b %Y").date().year

            if age_at_death > 150:
                passed = False
                print(f"ANOMALY: INDIVIDUAL: US07: {indiID}: Age at death is over 150 years ({age_at_death})")
        else:
            birth_date = datetime.datetime.strptime(indiInfo["Birth Date"], "%d %b %Y").date()
            age = today.year - birth_date.year

            if age > 150:
                passed = False
                print(f"ANOMALY: INDIVIDUAL: US07: {indiID}: Current age is over 150 years ({age})")
    
    if passed:
        print("PASSED: US07: No individuals over 150 years old")

# US08

# US09

# US10

# US11

# US12
def us12(families: dict, individuals: dict):
    passed = True
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
                        passed = False
                        print(f"ANOMALY: FAMILY: US12: {famID}: Mother is 60 or more years older than child ({mother_id} - {child_id})")

                if father_birth_date and child_birth_date:
                    if calculate_age_difference(father_birth_date, child_birth_date) >= 80:
                        passed = False
                        print(f"ANOMALY: FAMILY: US12: {famID}: Father is 80 or more years older than child ({father_id} - {child_id})")
    if passed:
        print("PASSED: US12: No mother 60 years older than child or father 80 years older than child")


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
    passed = True
    for fid in families.keys():
        husband_id = families[fid]["Husband ID"]
        wife_id = families[fid]["Wife ID"]
        if husband_id and wife_id:
            husband_gender = individuals[husband_id]["Gender"]
            wife_gender = individuals[wife_id]["Gender"]

            if husband_gender != "M":
                passed = False
                print(f"ANOMALY: FAMILY: US21: {fid}: Incorrect gender role for husband {husband_id}")

            if wife_gender != "F":
                passed = False
                print(f"ANOMALY: FAMILY: US21: {fid}: Incorrect gender role for wife {wife_id}")

    if passed:
        print("PASSED: US21: No incorrect gender roles")   

# US22
def us22(families: dict, individuals: dict):
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
def us23(families: dict, individuals: dict):
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
def us25(families: dict, individuals: dict):
    passed = True

    for famID, famInfo in families.items():
        children = famInfo.get("Children", [])

        first_names = set()
        duplicate_first_names = set()

        for childID in children:
            child_info = individuals.get(childID)
            if child_info is not None:
                first_name = child_info["Name"].split()[0]

                if first_name in first_names:
                    passed = False
                    duplicate_first_names.add(childID)
                else:
                    first_names.add(first_name)

        if duplicate_first_names:
            for childID in duplicate_first_names:
                print(f"ANOMALY: FAMILY: US25: {famID}: Duplicate first name in family: {childID}")

    if passed:
        print("PASSED: US25: All families have unique first names for their children.")

# US26

# US27

# US28

# US29
def us29(families: dict, individuals: dict):
    passed = True
    for indi_id, ind in individuals.items():
            if "Death Date" in ind.keys():
                passed = False
                print(f"US29: Deceased : {ind['Name']} (ID: {indi_id})")
    if passed:
        print("PASSED: US29: No deceased individuals")
   
    #used for unittest     
    #deceased = []
    #for indi_id, indi in individuals.items():
        #if 'DEAT' in indi:
           #deceased.append(indi)
    #return deceased

# US30
def us30(families: dict, individuals: dict):
    passed = True
    for fid in families.keys():
        husband_id = families[fid]["Husband ID"]
        wife_id = families[fid]["Wife ID"]
        husbandName = individuals[husband_id]["Name"]
        wifeName = individuals[wife_id]["Name"]

        if husbandName and "Death Date" not in individuals[husband_id].keys():
            passed = False
            print(f"US30: Living Married: {husbandName} (ID: {husband_id})")

        if wifeName and "Death Date" not in individuals[wife_id]:
            passed = False
            print(f"US30: Living Married: {wifeName} (ID: {wife_id})")

    if passed:
        print("PASSED: US30: No living and married individuals")

# US31

# US32

# US33

# US34

# US35

# US36
def us36(families, individuals):
    today = datetime.date.today()
    thirty_days_ago = today - datetime.timedelta(days=30)
    
    recent_deaths = []
    
    for indiID, indiInfo in individuals.items():
        death_date_str = indiInfo.get("Death Date")
        
        if death_date_str:
            death_date = datetime.datetime.strptime(death_date_str, "%d %b %Y").date()
            
            if death_date >= thirty_days_ago and death_date <= today:
                recent_deaths.append((indiID, indiInfo["Name"]))
    
    if recent_deaths:
        print("US36: Recent Deaths:")
        for indiID, name in recent_deaths:
            print(f"- {indiID}: {name}")
    else:
        print("US36: No recent deaths in the last 30 days.")
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

def us38(families: dict, individuals: dict):
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
                print("FAMILY: US39: " + fid + ": Wedding anniversary within next 30 days (" + families[fid]["Marriage Date"] + ")")
    if passed:
        print("PASSED: US39: No wedding anniversaries in next 30 days")

# US40

# US41

# US42

def main():
    # will call each user story function here

    readGed.main()

    functions = [us01, us07, us12, us15, us21, us22, us23, us25, us29, us30, us36, us38, us39]

    for i in range(len(functions)):
        functions[i](families, individuals)


if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()
