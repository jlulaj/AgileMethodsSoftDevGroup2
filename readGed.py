import datetime
from prettytable import PrettyTable

# Function to calculate age based on birth date
def calculate_age(birth_date):
    today = datetime.date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# Function to extract individual information
# Function to extract individual information
def extract_individuals(gedcom):
    individuals = {}
    indi_id = None  # Initialize indi_id with None
    for line in gedcom:
        if line.startswith("0 @I"):
            indi_id = line.split('@')[1]
            individuals[indi_id] = {}
        elif line.startswith("1 NAME"):
            name = line.split("NAME")[1].strip()
            individuals[indi_id]["Name"] = name
        elif line.startswith("1 SEX"):
            gender = line.split("SEX")[1].strip()
            individuals[indi_id]["Gender"] = gender
        elif line.startswith("1 BIRT"):
            birth_date = next(gedcom).split("DATE")[1].strip()
            individuals[indi_id]["Birth Date"] = birth_date
        elif line.startswith("1 DEAT"):
            individuals[indi_id]["Alive"] = False
            death_date = next(gedcom).split("DATE")[1].strip()
            individuals[indi_id]["Death Date"] = death_date
        elif indi_id is not None:  # Check if indi_id has a value
            if "Alive" not in individuals[indi_id]:
                individuals[indi_id]["Alive"] = True
    return individuals

# Function to extract family information
# Function to extract family information
def extract_families(gedcom):
    families = {}
    fam_id = None  # Initialize fam_id with None
    for line in gedcom:
        if line.startswith("0 @F"):
            fam_id = line.split('@')[1]
            families[fam_id] = {}
        elif line.startswith("1 HUSB"):
            husband_id = line.split('@')[1]
            families[fam_id]["Husband ID"] = husband_id
        elif line.startswith("1 WIFE"):
            wife_id = line.split('@')[1]
            families[fam_id]["Wife ID"] = wife_id
        elif line.startswith("1 CHIL"):
            children = families[fam_id].get("Children", [])
            child_id = line.split('@')[1]
            children.append(child_id)
            families[fam_id]["Children"] = children
        elif line.startswith("1 MARR"):
            families[fam_id]["Married"] = True
            marriage_date = next(gedcom).split("DATE")[1].strip()
            families[fam_id]["Marriage Date"] = marriage_date
        elif line.startswith("1 DIV"):
            families[fam_id]["Divorced"] = True
            divorce_date = next(gedcom).split("DATE")[1].strip()
            families[fam_id]["Divorce Date"] = divorce_date
    return families


def main():
    # Read the GEDCOM file
    with open("Family_Tree_GEDCOM.ged", "r") as file:
        gedcom_data = file.readlines()

    # Convert gedcom_data into an iterator
    gedcom_iterator = iter(gedcom_data)

    individuals = extract_individuals(gedcom_iterator)

    gedcom_iterator = iter(gedcom_data)
    families = extract_families(gedcom_iterator)

    # Display individual information in a table
    individual_table = PrettyTable()
    individual_table.field_names = ["ID", "Name", "Gender","Birth Date", "Age", "Alive", "Death", "Child", "Spouse"]

    for indi_id, indi_info in individuals.items():
        indi_table_row = [indi_id, indi_info["Name"], indi_info["Gender"], indi_info.get("Birth Date", "-")]
        if "Birth Date" in indi_info:
            birth_date = datetime.datetime.strptime(indi_info["Birth Date"], "%d %b %Y")
            age = calculate_age(birth_date)
            indi_table_row.append(age)
        else:
            indi_table_row.append("N/A")
        if indi_info["Alive"]:
            indi_table_row.append("Yes")
            indi_table_row.append("-")
        else:
            indi_table_row.append("No")
            indi_table_row.append(indi_info["Death Date"])
        child = next((fam_id for fam_id, fam_info in families.items() if indi_id in fam_info.get("Children", [])), "-")
        indi_table_row.append(child)
        spouse = next((fam_id for fam_id, fam_info in families.items() if indi_id == fam_info.get("Husband ID") or indi_id == fam_info.get("Wife ID")), "-")
        indi_table_row.append(spouse)
        individual_table.add_row(indi_table_row)

    # Display family information in a table
    family_table = PrettyTable()
    family_table.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]

    for fam_id, fam_info in families.items():
        fam_table_row = [fam_id]
        if fam_info.get("Married"):
            fam_table_row.append(fam_info.get("Marriage Date"))
        else:
            fam_table_row.append("No")
        if fam_info.get("Divorced"):
            fam_table_row.append(fam_info.get("Divorce Date"))
        else:
            fam_table_row.append("No")
        husband_name = individuals.get(fam_info["Husband ID"], {}).get("Name", "-")
        wife_name = individuals.get(fam_info["Wife ID"], {}).get("Name", "-")
        fam_table_row.append(fam_info["Husband ID"])
        fam_table_row.append(husband_name)
        fam_table_row.append(fam_info["Wife ID"])
        fam_table_row.append(wife_name)
        children = ", ".join(individuals.get(child_id, {}).get("Name", "-") for child_id in fam_info.get("Children", []))
        fam_table_row.append(children)
        family_table.add_row(fam_table_row)

    # Print the tables
    print("Individuals:")
    print(individual_table)

    print("\nFamilies:")
    print(family_table)

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()
