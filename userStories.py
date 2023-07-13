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
def us02(families: dict, individuals: dict):
    passed = True
    ind_list = []
    
    for fid in families.keys():
        if "Marriage Date" in families[fid].keys():
            temp_marriage = datetime.datetime.strptime(families[fid]["Marriage Date"], '%d %b %Y')
        else:
            continue

        temp_husb_id = families[fid]['Husband ID']
        temp_wife_id = families[fid]['Wife ID']

        temp_husb_bday = datetime.datetime.strptime(individuals[temp_husb_id]['Birth Date'], '%d %b %Y')
        temp_wife_bday = datetime.datetime.strptime(individuals[temp_wife_id]['Birth Date'], '%d %b %Y')

        if temp_husb_bday > temp_marriage:
            ind_list.append(temp_husb_id)
            passed = False
            print(f"ERROR: INDIVIDUAL: US02: {temp_husb_id}: Individual's birth date is after marriage date (Birth: {individuals[temp_husb_id]['Birth Date']}, Marriage: {families[fid]['Marriage Date']})")

        if temp_wife_bday > temp_marriage:
            ind_list.append(temp_wife_id)
            passed = False
            print(f"ERROR: INDIVIDUAL: US02: {temp_wife_id}: Individual's birth date is after marriage date (Birth: {individuals[temp_wife_id]['Birth Date']}, Marriage: {families[fid]['Marriage Date']})")

    if passed:
        print("PASSED: US02: No individuals with birth date after marriage date")

    return ind_list



# US03

# US04
def us04(families: dict, individuals: dict):
    for famID, famInfo in families.items():
        marriage_date = famInfo.get("Marriage Date")
        divorce_date = famInfo.get("Divorce Date")

        if marriage_date and divorce_date:
            marriage_date = datetime.datetime.strptime(marriage_date, "%d %b %Y").date()
            divorce_date = datetime.datetime.strptime(divorce_date, "%d %b %Y").date()

            if divorce_date < marriage_date:
                print(f"ANOMALY: FAMILY: US04: {famID}: Divorce occurred before marriage")

# US05
def us05(families: dict, individuals: dict):
    for famID, famInfo in families.items():
        husband_id = famInfo.get("Husband ID")
        wife_id = famInfo.get("Wife ID")
        marriage_date = famInfo.get("Marriage Date")

        if husband_id and wife_id and marriage_date:
            husband_death_date = individuals.get(husband_id, {}).get("Death Date")
            wife_death_date = individuals.get(wife_id, {}).get("Death Date")

            if husband_death_date and marriage_date > husband_death_date:
                print(f"ANOMALY: FAMILY: US05: {famID}: Marriage occurred after husband's death")

            if wife_death_date and marriage_date > wife_death_date:
                print(f"ANOMALY: FAMILY: US05: {famID}: Marriage occurred after wife's death")

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
    fam_list = []
    for fid in families.keys():
        if len(families[fid]['Children']) >= 15:
            fam_list.append(fid)
            passed = False
            print("ANAMOLY: FAMILY: US15: " + fid + ": Family has more than 15 siblings (" + str(len(families[fid]['Children'])) + ")")
    if passed:
        print("PASSED: US15: No families with more than 15 siblings")
    
    return fam_list

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
def us24(families: dict, individuals: dict):
    passed = True
    fam_list = []
    temp_families = families.copy()
    for fid in families.keys():
        if "Marriage Date" in families[fid].keys():
            temp_marriage = datetime.datetime.strptime(families[fid]["Marriage Date"], '%d %b %Y')
        else:
            continue

        temp_husb_name = individuals[families[fid]['Husband ID']]['Name']
        temp_wife_name = individuals[families[fid]['Wife ID']]['Name']
        temp_families.pop(fid)
        for tfid in temp_families.keys():
            if "Marriage Date" in temp_families[tfid].keys():
                temp_marriage_2 = datetime.datetime.strptime(temp_families[tfid]["Marriage Date"], '%d %b %Y')
            else:
                continue

            temp_husb_name_2 = individuals[temp_families[tfid]['Husband ID']]['Name']
            temp_wife_name_2 = individuals[temp_families[tfid]['Wife ID']]['Name']

            if temp_husb_name == temp_husb_name_2 and temp_wife_name == temp_wife_name_2 and temp_marriage == temp_marriage_2:
                fam_list.append([fid, tfid])
                passed = False
                print(f"ANOMALY: FAMILY: US24: {fid},{tfid}: Two families with same husband name, wife name, and marriage date")
    
    if passed:
        print("PASSED: US24: No two families with same husband name, wife name, and marriage date")

    return fam_list


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
def us34(families: dict, individuals: dict):
    passed = True
    fam_list = []

    for fid in families.keys():
        if "Marriage Date" in families[fid].keys():
            temp_marriage = datetime.datetime.strptime(families[fid]["Marriage Date"], '%d %b %Y')
        else:
            continue
        temp_husb_id = families[fid]['Husband ID']
        temp_wife_id = families[fid]['Wife ID']

        temp_husb_bday = datetime.datetime.strptime(individuals[temp_husb_id]['Birth Date'], '%d %b %Y')
        temp_wife_bday = datetime.datetime.strptime(individuals[temp_wife_id]['Birth Date'], '%d %b %Y')

        temp_husb_age = (temp_marriage - temp_husb_bday).days
        temp_wife_age = (temp_marriage - temp_wife_bday).days

        if temp_husb_age > 2 * temp_wife_age or temp_wife_age > 2 * temp_husb_age:
            fam_list.append(fid)
            passed = False
            print(f"ANOMALY: FAMILY: US34: {fid}: Older spouse more than twice as old as younger spouse when married (Husband: {individuals[temp_husb_id]['Birth Date']}, Wife: {individuals[temp_wife_id]['Birth Date']}, Marriage: {families[fid]['Marriage Date']})")
    
    if passed:
        print("PASSED: US34: No couple with older spouse more than twice as old as younger spouse when married.")

    return fam_list



        



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
    fam_list = []

    for fid in families.keys():
        if "Marriage Date" in families[fid].keys():
            temp_date = datetime.datetime.strptime(families[fid]["Marriage Date"], '%d %b %Y')
            temp_date = datetime.date(today.year, temp_date.month, temp_date.day)
            if temp_date > today and temp_date - today <= datetime.timedelta(30):
                fam_list.append(fid)
                passed = False
                print("FAMILY: US39: " + fid + ": Wedding anniversary within next 30 days (" + families[fid]["Marriage Date"] + ")")
    if passed:
        print("PASSED: US39: No wedding anniversaries in next 30 days")
    
    return fam_list

# US40

# US41

# US42

def main():

    # print ged tabular output
    readGed.main()

    # call each user story function
    functions = [us01, us02, us04, us05, us07, 
                 us12, us15, 
                 us21, us22, us23, us24, us25, us29, us30, 
                 us34, us36, us38, us39]

    for i in range(len(functions)):
        functions[i](families, individuals)


if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()
