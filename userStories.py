from datetime import datetime, timedelta
from readGed import extract_families, extract_individuals
from collections import defaultdict
import readGed
import datetime
import calendar


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
    passed = True
    date_list = []
    today = datetime.date.today()

    for fid in families.keys():
        check_list = ["Marriage", "Divorce"]
        for check in check_list:
            temp_key = check + " Date"
            if temp_key in families[fid].keys():
                temp_day = datetime.datetime.strptime(families[fid][temp_key], '%d %b %Y').date()
            else:
                continue
            if temp_day > today:
                date_list.append(families[fid][temp_key])
                passed = False
                print(f"ERROR: FAMILY: US01: {fid}: {temp_key} is after today's date ({families[fid][temp_key]})")
    
    for iid in individuals.keys():
        check_list = ["Birth", "Death"]
        for check in check_list:
            temp_key = check + " Date"
            if temp_key in individuals[iid].keys():
                temp_day = datetime.datetime.strptime(individuals[iid][temp_key], '%d %b %Y').date()
            else:
                continue
            if temp_day > today:
                date_list.append(individuals[iid][temp_key])
                passed = False
                print(f"ERROR: INDIVIDUAL: US01: {iid}: {temp_key} is after today's date ({individuals[iid][temp_key]})")

    if passed:
        print("PASSED: US01: No dates come after today's date")

    return date_list


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
def us03(families: dict, individuals: dict):
    passed = True
    ind_list = []
    
    for indID, indInfo in individuals.items():
        if "Birth Date" in indInfo.keys() and "Death Date" in indInfo.keys():
            birth_date = datetime.datetime.strptime(indInfo["Birth Date"], '%d %b %Y')
            death_date = datetime.datetime.strptime(indInfo["Death Date"], '%d %b %Y')

            if birth_date > death_date:
                ind_list.append(indID)
                passed = False
                print(f"ERROR: INDIVIDUAL: US03: {indID}: Individual's birth date is after death date (Birth: {indInfo['Birth Date']}, Death: {indInfo['Death Date']})")

    if passed:
        print("PASSED: US03: No individuals with birth date after death date")

    return ind_list



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
    return [] 

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
    return [] 

# US06
def us06(families: dict, individuals: dict):
    for famID, famInfo in families.items():
        husband_id = famInfo.get("Husband ID")
        wife_id = famInfo.get("Wife ID")
        divorce_date = famInfo.get("Divorce Date")

        if husband_id and wife_id and divorce_date:
            husband_death_date = individuals.get(husband_id, {}).get("Death Date")
            wife_death_date = individuals.get(wife_id, {}).get("Death Date")

            husband_family = individuals.get(husband_id, {}).get("Families", {}).get(famID, {})
            marriage_date = husband_family.get("Marriage Date")

            if husband_death_date and marriage_date and marriage_date > husband_death_date:
                print(f"ANOMALY: FAMILY: US06: {famID}: Divorce occurred after husband's death")

            wife_family = individuals.get(wife_id, {}).get("Families", {}).get(famID, {})
            marriage_date = wife_family.get("Marriage Date")

            if wife_death_date and marriage_date and marriage_date > wife_death_date:
                print(f"ANOMALY: FAMILY: US06: {famID}: Divorce occurred after wife's death")
    
    return []


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
    return []
# US08
def us08(families: dict, individuals: dict):
    passed = True
    ind_list = []

    for fid in families.keys():
        if "Children" in families[fid].keys() and "Marriage Date" in families[fid].keys():
            temp_marriage = datetime.datetime.strptime(families[fid]["Marriage Date"], '%d %b %Y').date()
            for iid in families[fid]['Children']:
                temp_bday = datetime.datetime.strptime(individuals[iid]["Birth Date"], '%d %b %Y').date()
                if temp_marriage > temp_bday:
                    ind_list.append(iid)
                    passed = False
                    print(f"ANOMALY: INDIVIDUAL: US08: {iid}: Child born before marriage of parents")
                
                if "Divorce Date" in families[fid].keys():
                    temp_divorce = datetime.datetime.strptime(families[fid]["Divorce Date"], '%d %b %Y').date()
                    if temp_bday > temp_divorce + datetime.timedelta(days = 9 * 30):
                        if iid not in ind_list:
                            ind_list.append(iid)
                        passed = False
                        print(f"ANOMALY: INDIVIDUAL: US08: {iid}: Child born before marriage of parents")
    
    if passed:
        print("PASSED: US08: No individuals born before marriage of parents or 9 months after divorce of parents")
    return ind_list

# US09
def us09(families: dict, individuals: dict):
    passed = True

    for famID, famInfo in families.items():
        if "Children" in famInfo and "Wife ID" in famInfo and "Husband ID" in famInfo:
            wifeID = famInfo["Wife ID"]
            husbandID = famInfo["Husband ID"]

            if wifeID in individuals and "Death Date" in individuals[wifeID]:
                wife_death_date = datetime.datetime.strptime(individuals[wifeID]["Death Date"], "%d %b %Y").date()

            if husbandID in individuals and "Death Date" in individuals[husbandID]:
                husband_death_date = datetime.datetime.strptime(individuals[husbandID]["Death Date"], "%d %b %Y").date()

            children = famInfo["Children"]

            for childID in children:
                if childID in individuals and "Birthday" in individuals[childID]:
                    child_birth_date = datetime.datetime.strptime(individuals[childID]["Birthday"], "%d %b %Y").date()

                    if "Death Date" in individuals[wifeID] and child_birth_date > wife_death_date:
                        passed = False
                        print(f"ANOMALY: FAMILY: US09: {famID}: Child {childID} born after mother's death")

                    if "Death Date" in individuals[husbandID]:
                        nine_months_after_father_death = husband_death_date + timedelta(days=270)  # 9 months ~ 270 days

                        if child_birth_date > nine_months_after_father_death:
                            passed = False
                            print(f"ANOMALY: FAMILY: US09: {famID}: Child {childID} born more than 9 months after father's death")
    
    if passed:
        print("PASSED: US09: All children are born before the death of the mother and before 9 months after the death of the father")
    
    return []

# US10
def us10(families: dict, individuals: dict):
    passed = True
    for famID, famInfo in families.items():
        if "Marriage Date" in famInfo.keys():
            marriage_date = datetime.datetime.strptime(famInfo["Marriage Date"], '%d %b %Y').date()
            husband_id = famInfo["Husband ID"]
            wife_id = famInfo["Wife ID"]
            if husband_id in individuals and wife_id in individuals:
                husband_birth_date = datetime.datetime.strptime(individuals[husband_id]["Birth Date"], '%d %b %Y').date()
                wife_birth_date = datetime.datetime.strptime(individuals[wife_id]["Birth Date"], '%d %b %Y').date()
                min_birth_date = marriage_date - datetime.timedelta(days=(14 * 365))
                if husband_birth_date > min_birth_date or wife_birth_date > min_birth_date:
                    passed = False
                    print(f"ANOMALY: FAMILY: US10: {famID}: Marriage occurred before both spouses turned 14.")
    if passed:
        print("PASSED: US10: All marriages occurred at least 14 years after birth of both spouses.")
    return []
    
# US11
def get_marriages(individual: dict) -> list:
    return [datetime.datetime.strptime(date, '%d %b %Y').date() for date in individual.get("Marriages", [])]

def us11(families: dict, individuals: dict):
    passed = True
    for famID, famInfo in families.items():
        if "Marriage Date" in famInfo.keys():
            marriage_date = datetime.datetime.strptime(famInfo["Marriage Date"], '%d %b %Y').date()
            husband_id = famInfo["Husband ID"]
            wife_id = famInfo["Wife ID"]
            if husband_id in individuals and wife_id in individuals:
                husband_marriages = get_marriages(individuals[husband_id])
                wife_marriages = get_marriages(individuals[wife_id])
                for marriage_date_h in husband_marriages:
                    if marriage_date_h != marriage_date and marriage_date_h > marriage_date:
                        passed = False
                        print(f"ANOMALY: FAMILY: US11: {famID}: Husband has another marriage during this marriage (Date: {marriage_date}, Other Marriage: {marriage_date_h})")
                for marriage_date_w in wife_marriages:
                    if marriage_date_w != marriage_date and marriage_date_w > marriage_date:
                        passed = False
                        print(f"ANOMALY: FAMILY: US11: {famID}: Wife has another marriage during this marriage (Date: {marriage_date}, Other Marriage: {marriage_date_w})")
    if passed:
        print("PASSED: US11: No instances of bigamy found in the family relationships.")
    return []


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
def us13(families: dict, individuals: dict):
    def calculate_age_in_days(birth_date1, birth_date2):
        return (birth_date2 - birth_date1).days

    passed = True

    for ind_id, individual in individuals.items():
        if "Families" in individual and "Birth Date" in individual:
            birth_date = datetime.datetime.strptime(individual["Birth Date"], '%d %b %Y').date()
            families = individual["Families"]

            if len(families) > 1:
                sibling_birth_dates = []
                for family_id in families:
                    family = families[family_id]
                    siblings = family["Children"]

                    for sibling_id in siblings:
                        if sibling_id != ind_id and "Birth Date" in individuals[sibling_id]:
                            sibling_birth_date = datetime.datetime.strptime(individuals[sibling_id]["Birth Date"], '%d %b %Y').date()
                            sibling_birth_dates.append(sibling_birth_date)

                for i in range(len(sibling_birth_dates)):
                    for j in range(i + 1, len(sibling_birth_dates)):
                        age_in_days = calculate_age_in_days(sibling_birth_dates[i], sibling_birth_dates[j])
                        if age_in_days < 2 or age_in_days > 8 * 30:
                            passed = False

    if passed:
        print("Passed: US13: Siblings are spaced properly")
    else:
        print("Failed: US13: Siblings are not spaced properly")
    
    return []

# US14
def us14(families: dict, individuals: dict):
    passed = True
    for famID, famInfo in families.items():
        children = famInfo.get("Children", [])

        # Use a defaultdict to group children by birth date
        birth_date_counts = defaultdict(int)

        for childID in children:
            child_info = individuals.get(childID)
            if child_info is not None and "Birth Date" in child_info:
                birth_date_counts[child_info["Birth Date"]] += 1

        # Check if any group of children have more than five with the same birth date
        for birth_date, count in birth_date_counts.items():
            if count > 5:
                passed = False
                print(f"ANOMALY: FAMILY: US14: {famID}: More than five siblings born at the same time ({birth_date}): {count} siblings")

    if passed:
        print("PASSED: US14: No more than five siblings born at the same time in any family.")

    return []

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
def us16(families: dict, individuals: dict):
    passed = True

    for famID, famInfo in families.items():
        if "Husband ID" in famInfo:
            husband_id = famInfo["Husband ID"]
            children = famInfo.get("Children", [])

            if husband_id in individuals:
                husband_last_name = get_last_name(individuals[husband_id]["Name"])

                for child_id in children:
                    if child_id in individuals and individuals[child_id]["Gender"] == "M":
                        child_last_name = get_last_name(individuals[child_id]["Name"])
                        if husband_last_name != child_last_name:
                            passed = False
                            print(f"ANOMALY: FAMILY: US16: {famID}: Husband and male children do not have the same last name")
                            break

    if passed:
        print("PASSED: US16: All male members of each family have the same last name")
    
    return []

def get_last_name(full_name: str) -> str:
    name_parts = full_name.split()
    if len(name_parts) > 1:
        return name_parts[-1]
    return ""

# US17
def us17(families: dict, individuals: dict):
    passed = True

    for fid, famInfo in families.items():
        husband_id = famInfo.get("Husband ID")
        wife_id = famInfo.get("Wife ID")
        children = famInfo.get("Children", [])

        if husband_id and wife_id:
            husband_descendants = set()
            wife_descendants = set()
            find_descendants(husband_id, individuals, husband_descendants)
            find_descendants(wife_id, individuals, wife_descendants)

            if husband_id in wife_descendants or wife_id in husband_descendants:
                passed = False
                print(f"ANOMALY: FAMILY: US17: {fid}: Parent is marrying a descendant")
    
    if passed:
        print("PASSED: US17: No instances of parents marrying their descendants")
    
    return []

def find_descendants(indi_id: str, individuals: dict, descendants: set):
    children = individuals.get(indi_id, {}).get("Children", [])
    for child_id in children:
        descendants.add(child_id)
        find_descendants(child_id, individuals, descendants)

# US18

def us18(families: dict, individuals: dict):
    passed = True

    for fid, famInfo in families.items():
        husband_id = famInfo.get("Husband ID")
        wife_id = famInfo.get("Wife ID")
        children = famInfo.get("Children", [])

        if children:
            siblings = set()
            for child_id in children:
                siblings.update(individuals.get(child_id, {}).get("Children", []))

            if husband_id in siblings or wife_id in siblings:
                passed = False
                print(f"ANOMALY: FAMILY: US18: {fid}: Sibling is marrying another sibling")

    if passed:
        print("PASSED: US18: No instances of siblings marrying each other")

    return []

# US19
def us19(families: dict, individuals: dict):
    passed = True
    new_set = False
    fam_list = []
    cousins = []
    for fid in families.keys():
        if "Children" in families[fid].keys():
            new_set = True
            for cid in families[fid]["Children"]:
                for fid2 in families.keys():
                    if cid == families[fid2]["Husband ID"] or cid == families[fid2]["Wife ID"]:
                        if "Children" in families[fid2].keys():
                            if new_set:
                                cousins.append([families[fid2]["Children"]])
                                new_set = False
                            else:
                                cousins[len(cousins) - 1].append(families[fid2]["Children"])
    
    for cousin_set in cousins:
        if len(cousin_set) == 1:
            continue
        for i in range(len(cousin_set)):
            for j in range(1, len(cousin_set)):
                for fid in families.keys():
                    if (families[fid]["Husband ID"] == cousin_set[i] and families[fid]["Wife ID"] == cousin_set[j]) or \
                        (families[fid]["Husband ID"] == cousin_set[j] and families[fid]["Wife ID"] == cousin_set[i]):
                        passed = False
                        fam_list.append(fid)
                        print(f"ANOMALY: FAMILY: US19: {fid}: First cousins married")
    
    if passed:
        print("PASSED: US19: No first cousins married")

    return fam_list
                            

    
    

# US20
def us20(families: dict, individuals: dict):
    passed = True
    fam_list = []
    for fid in families.keys():
        if "Children" in families[fid].keys():
            for cid in families[fid]["Children"]:
                for cid2 in families[fid]["Children"]:
                    if cid == cid2:
                        continue
                    for fid2 in families.keys():
                        if (families[fid2]["Husband ID"] == cid and families[fid2]["Wife ID"] == cid2) or \
                            (families[fid2]["Husband ID"] == cid2 and families[fid2]["Wife ID"] == cid):
                            print(f"ANOMALY: FAMILY: US20: {fid2}: Aunt or uncle married niece or nephew")
                            passed = False
                            fam_list.append(fid2)

    if passed:
        print("PASSED: US20: No aunts or uncles married niece or nephew")
    
    return fam_list
                            


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
        duplicate_first_names = []

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
    
    return duplicate_first_names 

# US26
def us26(families: dict, individuals: dict):
    passed = True
    return_list = []

    ind_ids = list(individuals.keys())
    fam_ids = []

    for fid in families.keys():
        fam_ids.append(families[fid]["Husband ID"])
        fam_ids.append(families[fid]["Wife ID"])
        if "Children" in families[fid].keys():
            fam_ids += families[fid]["Children"]
    ind_set = set(ind_ids)
    fam_set = set(fam_ids)
    extra_ind = ind_set - fam_set
    extra_fam = fam_set - ind_set
    return_list = [extra_ind, extra_fam]
    if len(extra_ind) > 0:
        passed = False
        print(f"ERROR: US26: Entries in invididual records that do not exist in family records ({extra_ind})")
    if len(extra_fam) > 0:
        passed = False
        print(f"ERROR: US26: Entries in family records that do not exist in individual records ({extra_fam})")
    if passed:
        print("PASSED: US26: Entries between family and individual records are consistent")
    return return_list

# US27
def calculate_age(birth_date):
    today = datetime.now()
    birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def us27(families: dict, individuals: dict):
    for family_id, ind in families.items():
        for ind_id in ind:
            if ind_id in individuals:
                person = individuals[ind_id]
                age = calculate_age(person['birthdate'])
                print(f" - Name: {person['name']}, Age: {age}")
        print()
    return []

# US28
def us28(families: dict, individuals: dict):
    fam_dict = {}
    ordered_sibs = []
    for fid in families.keys():
        if 'Children' in families[fid].keys():
            ordered_sibs = []
            for iid in families[fid]['Children']:
                temp_bday = datetime.datetime.strptime(individuals[iid]["Birth Date"], '%d %b %Y').date()

                for i in range(len(ordered_sibs)):
                    i_bday = datetime.datetime.strptime(individuals[ordered_sibs[i]]['Birth Date'], '%d %b %Y').date()
                    if temp_bday <= i_bday:
                        ordered_sibs.insert(i, iid)

                if iid not in ordered_sibs:
                    ordered_sibs.append(iid)
            fam_dict[fid] = ordered_sibs
            ordered_sibs = []

    print("US28: Siblings ordered by age:", fam_dict)

    return fam_dict


# US29
def us29(families: dict, individuals: dict):
    passed = True
    for indi_id, ind in individuals.items():
            if "Death Date" in ind.keys():
                passed = False
                print(f"US29: Deceased : {ind['Name']} (ID: {indi_id})")
    if passed:
        print("PASSED: US29: No deceased individuals")

    return []
   
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

    return []

# US31
def us31(families: dict, individuals: dict):
    single_ind = []
    today = datetime.date.today()
    
    for indiID, indiInfo in individuals.items():
        if indiInfo.get("Alive", True) and "Birth Date" in indiInfo:
            birth_date = datetime.datetime.strptime(indiInfo["Birth Date"], "%d %b %Y").date()
            age = today.year - birth_date.year

            if age >= 30:
                for famID, famInfo in families.items():
                    if famInfo.get("Married", False):
                        single_ind.append(indiInfo["Name"])
    
    if len(single_ind) > 0:
        print("US31: Single Individuals, 30 years or older: " + str(single_ind))   
    else: 
        print("PASSED: US31: No single individuals over 30")

    return []

# US32
def us32(individuals):
    multiple_births = []

    birth_dates = {}
    for ind_id, ind_data in individuals.items():
        if "Birth Date" in ind_data:
            birth_date = ind_data["Birth Date"]
            if birth_date in birth_dates:
                birth_dates[birth_date].append(ind_id)
            else:
                birth_dates[birth_date] = [ind_id]

    for birth_date, ind_ids in birth_dates.items():
        if len(ind_ids) > 1:
            multiple_births.append((birth_date, ind_ids))

    if multiple_births:
        for birth_date, ind_ids in multiple_births:
            print(f"ANOMALY: US32: Multiple births on {birth_date}: Individuals {', '.join(ind_ids)}")
    else:
        print("PASSED: US32: No multiple births found.")

    return multiple_births


# US33
def us33(families, individuals):
    orphaned_children = []
    today = datetime.date.today()

    for famID, famInfo in families.items():
        if 'Children' in famInfo:
            children_ids = famInfo['Children']
            for child_id in children_ids:
                if child_id in individuals:
                    child_info = individuals[child_id]
                    if 'Death Date' not in child_info or child_info['Death Date'] == 'NA':
                        if 'Birth Date' in child_info:
                            birth_date = datetime.datetime.strptime(child_info['Birth Date'], "%d %b %Y").date()
                            age = today.year - birth_date.year

                            if age < 18:
                                # Check if both parents are dead
                                if 'Husband ID' in famInfo and 'Wife ID' in famInfo:
                                    husband_id = famInfo['Husband ID']
                                    wife_id = famInfo['Wife ID']

                                    if husband_id in individuals and wife_id in individuals:
                                        husband_info = individuals[husband_id]
                                        wife_info = individuals[wife_id]

                                        if ('Death Date' in husband_info and husband_info['Death Date'] != 'NA') and ('Death Date' in wife_info and wife_info['Death Date'] != 'NA'):
                                            orphaned_children.append((child_id, child_info['Name']))

    if orphaned_children:
        print("US33: Orphaned Children (both parents dead and child < 18 years old):")
        for child_id, name in orphaned_children:
            print(f"- {child_id}: {name}")
    else:
        print("US33: No orphaned children found in the GEDCOM file.")
    
    return orphaned_children

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
def us35(families: dict, individuals:dict):
    today = datetime.date.today()
    thirty_days_ago = today - datetime.timedelta(days=30)
    
    recent_births = []
    
    for indiID, indiInfo in individuals.items():
        birth_date_str = indiInfo.get("Birth Date")
        
        if birth_date_str:
            birth_date = datetime.datetime.strptime(birth_date_str, "%d %b %Y").date()
            
            if birth_date >= thirty_days_ago and birth_date <= today:
                recent_births.append((indiID, indiInfo["Name"]))
    
    if recent_births:
        print("US35: Recent Births:")
        for indiID, name in recent_births:
            print(f"- {indiID}: {name}")
    else:
        print("US35: No recent births in the last 30 days.")
    
    return recent_births


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
def us37(individuals: dict, families: dict):
    from datetime import datetime, timedelta

    today = datetime.today()
    last_30_days = today - timedelta(days=30)

    living_spouses_descendants = {}

    for ind_id, ind_data in individuals.items():
        if "Death Date" in ind_data:
            death_date = datetime.strptime(ind_data["Death Date"], '%d %b %Y')
            if last_30_days <= death_date <= today:
                spouse_fam_id = ind_data.get("Spouse Family")
                if spouse_fam_id:
                    spouse_fam = families.get(spouse_fam_id)
                    if spouse_fam:
                        spouse_ids = [spouse_fam["Husband ID"], spouse_fam["Wife ID"]]
                        descendants = [ind_id]
                        for descendant_id in individuals.keys():
                            if individuals[descendant_id].get("Child Family") == spouse_fam_id:
                                descendants.append(descendant_id)
                        living_spouses_descendants[ind_id] = (spouse_ids, descendants)

    if living_spouses_descendants:
        for ind_id, (spouse_ids, descendants) in living_spouses_descendants.items():
            spouse_names = [individuals[spouse_id]["Name"] for spouse_id in spouse_ids if spouse_id in individuals]
            descendant_names = [individuals[descendant_id]["Name"] for descendant_id in descendants if descendant_id in individuals]
            print(f"ANOMALY: US37: Living spouses and descendants of {individuals[ind_id]['Name']} (ID: {ind_id}), who died in the last 30 days: Spouses: {', '.join(spouse_names)}, Descendants: {', '.join(descendant_names)}")
    else:
        print("PASSED: US37: No living spouses and descendants found for individuals who died in the last 30 days.")

    return living_spouses_descendants

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

    return []

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
def us40(errors: dict):
    if errors:
        for line_number, error_message in errors.items():
            print(f"ERROR: Line {line_number}: {error_message}")
    else:
        print("PASSED: No errors found in the GEDCOM file.")

# US41
def us41(dates: dict):
    corrected_dates = {}

    for tag, date_value in dates.items():
        parts = date_value.split()
        if len(parts) == 2:
            day_or_month, year = parts
            if day_or_month.isdigit() and year.isdigit():
                if len(day_or_month) == 4:  # If year is provided and no day or month
                    corrected_date = f"01 JAN {year}"
                    corrected_dates[tag] = corrected_date
                else:
                    corrected_date = f"01 {day_or_month} {year}"
                    corrected_dates[tag] = corrected_date

    if corrected_dates:
        for tag, corrected_date in corrected_dates.items():
            print(f"ANOMALY: US41: Accepted date format for {tag}: {corrected_date}")
    else:
        print("PASSED: US41: No date anomalies found.")

    return corrected_dates

# US42
def is_legitimate_date(date_str):
    try:
        year, month, day = map(int, date_str.split(' '))
        return 1 <= month <= 12 and 1 <= day <= calendar.monthrange(year, month)[1]
    except ValueError:
        return False

def us42(families, individuals):
    passed = True
    for family_id, family in families.items():
        if not is_legitimate_date(family.get('marriage_date', '')) or \
           'divorce_date' in family and not is_legitimate_date(family['divorce_date']):
            print(f"Invalid dates in family: {family_id}")
            passed = False

        for child in family.get('children', []):
            if child not in individuals:
                print(f"Child {child} not found in individuals for family: {family_id}")
                passed = False

    for individual_name, individual in individuals.items():
        if not is_legitimate_date(individual.get('birth_date', '')) or \
           'death_date' in individual and not is_legitimate_date(individual['death_date']):
            print(f"Invalid dates for individual: {individual_name}")
            passed = False

    if passed:
        print("All dates are valid and legitimate.")
    else:
        print("Dates validation failed.")

    return []

def main():

    # print ged tabular output
    readGed.main()

    # call each user story function
    functions = [us01, us02, us03, us04, us05, us06, us07, us08, us09, us10, us11,
                 us12, us13, us14, us15, us16, us17, us18, us19, us20,
                 us21, us22, us23, us24, us25, us26, us27, us28, us29, us30, us31, us33, 
                 us34, us35, us36, us37, us38, us39, us42] 
    for i in range(len(functions)):
        functions[i](families, individuals)   


if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   
   main()
