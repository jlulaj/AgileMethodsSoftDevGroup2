import sys

# Individual class to store information about individuals
class Individual:
    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

# Family class to store information about families
class Family:
    def __init__(self, fid, husband, wife):
        self.fid = fid
        self.husband = husband
        self.wife = wife

# Initialize lists to store individuals and families
individuals = []
families = []

# Open the GEDCOM file for reading
with open('hw2test.ged', 'r') as file:
    current_individual = None
    current_family = None

    # Iterate through each line in the file
    for line in file:
        parts = line.split()

        # Check for new individual or family entries
        if line.startswith('0 @'):
            if len(parts) > 2:
                if parts[2] == 'INDI':  # New individual entry
                    uid = parts[1]
                    current_individual = Individual(uid, '')
                    individuals.append(current_individual)
                elif parts[2] == 'FAM':  # New family entry
                    fid = parts[1]
                    current_family = Family(fid, '', '')
                    families.append(current_family)
        # Update individual's name
        elif line.startswith('1 NAME') and current_individual is not None:
            current_individual.name = ' '.join(parts[2:])
        # Update family's husband
        elif line.startswith('1 HUSB') and current_family is not None:
            current_family.husband = parts[2].replace('@', '')
        # Update family's wife
        elif line.startswith('1 WIFE') and current_family is not None:
            current_family.wife = parts[2].replace('@', '')

# Save the output to an output file
output_filename = 'output.txt'
with open(output_filename, 'w') as output_file:
    # Redirect the standard output to the file
    sys.stdout = output_file

    # Print individuals in order of unique identifiers
    print("Individuals:")
    for individual in sorted(individuals, key=lambda x: x.uid):
        print(f"UID: {individual.uid}, Name: {individual.name}")

    # Print families in order of unique identifiers
    print("\nFamilies:")
    for family in sorted(families, key=lambda x: x.fid):
        print(f"FID: {family.fid}, Husband: {family.husband}, Wife: {family.wife}")

# Reset the standard output
sys.stdout = sys.__stdout__

print(f"Output saved to {output_filename}.")
