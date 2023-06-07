# AgileMethodsSoftDevGroup2

# **test file includes random lines from hw1**

#outputs level, tag, whether it is a valid tag, and any remaining arguments
#checks for tags INDI and FAM and sets them to valid
def open_file(file_path):
    with open(file_path, 'r') as filename:
        for line in filename:
            
            validTag = " "
            
            #gets each line from .ged file
            line = line.strip()
            print("--> " + line)

            #breaking down each line into its components
            lineValuesList = line.split() #creates a list of components
            #print(lineValuesList, " number of values: " + int(lineValuesList))
            lineLevel = int(lineValuesList[0]) #gets the integer value of the level
            #print(lineValuesList, ", Level = ", lineLevel)
            lineTag = lineValuesList[1] #gets the tag
            #print(lineValuesList, ", Level = ", lineLevel, ", Tag = ", lineTag)
 
            #testing output values
            #print(lineValuesList, ", Level = ", lineLevel, ", Tag = ", lineTag, " args: ", arguments)

            #Specical cases: INDI and FAM
            #checks to see if the tag is INDI or FAM and adjusts the output
            if(lineLevel == 0 and len(lineValuesList) > 2 and lineTag != 'NOTE'):
                lineTag = lineValuesList[2]
                #print("NEW TAG = ", lineTag)
                arguments = " ".join(lineValuesList[1:2])
                #print("NEW ARGS = ", arguments)

                #checks if the new tag is in the list of valid tags
                if(validtags(lineTag)):
                   validTag = 'Y'
                else:
                    validTag = 'N'
                #formatted output
                print("<-- {}|{}|{}|{}".format(lineLevel, lineTag, validTag, arguments))
            else:
                #checks if the tag is in the list of valid tags
                if(validtags(lineTag)):
                    validTag = 'Y'
                else:
                    validTag = 'N'
                #appends the remaining arguments to the list of arguments
                arguments = " ".join(lineValuesList[2:])
                #formatted output
                print("<-- {}|{}|{}|{}".format(lineLevel, lineTag, validTag, arguments))

#list of all valid tags for project
def validtags(tag):
    valid_tags = {'INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE'}
    return tag in valid_tags

#path to test file
open_file('/Users/jacquelinelulaj/Desktop/hw2test.ged')
