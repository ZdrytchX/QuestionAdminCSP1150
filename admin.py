# ZdrytchX de Frisquilous

import json

# Accepts only integers
def inputInt(prompt): #finishmeTODO
    while True:
        entry = input(prompt)#custom input message
        try:
            intput = int(entry.strip())#remove whitespace
            return intput
        except:#if failed it is likely a string
            print("Please enter in an integer")
            continue



# This function repeatedly prompts for input until something other than whitespace is entered.
# See Point 2 of the "Functions in admin.py" section of the assignment brief.\
def inputSomething(prompt):
    while True:
        entry = input(prompt)#multiple entries not allowed for input function?
        if entry == "":
            print("Please enter an answer.")
            continue
        try:
            stringput = entry.strip().upper() #remove whitespace at the beginning and end, then sets to uppercase
            return stringput
        except:#obligatory backup exception for re-input
            print("Please try something else, you're not doing it right")
            continue

# Asks the user if they want to save changes upon quitting or upon choosing to backup
def saveChanges(dataList):
    continYN = inputSomething("Would you like to save changes? [Y]es or Continue without saving:\n> ")
    if continYN == "Y":
        file = open("data.json", "w")
        json.dump(dataList, file)
        file.close()#let the user know that it was successful
        print("Changes Saved to data.json...\n")
        return
    else:#if they chose not to save their undesired changes etc.
        print("Changes have not been saved...")

try:
    file = open("data.json","r")
    data = json.load(file)
    file.close()
    print("data.json loaded successfully")
except:#no file present, file gets created when we save later
    print("No data.json file was found or was corrupted.")
    data = []

#_______________________________________________________________#
print('Welcome to the Quizle Admin Program. This program was made as an assignment for ECU as an assignment for CSP1150 (172) by ZdrytchX')
#_______________________________________________________________#

###main loop###
while True:
    choice = inputSomething('=====\nChoose [A]dd, [B]ackup, [L]ist, [S]earch, [V]iew, [D]elete or [Q]uit.\n> ')


    if choice == 'A':
        quest = inputSomething("Enter the question you would like to add:\n> ")
        ans = []
        while True:
            answa = inputSomething("Please add the answer you would like to add:\n> ")
            ans.append(answa)#Aooend answers to the answer list
            continYN = inputSomething("Would you like to add more answers? [Y]es or Continue\n> ")
            if continYN == "Y":
                continue
            else:#assume no more answers
                break
        diff = inputInt("Enter in the difficulty setting you want for this question\n> ")
        if diff not in range(1, 6):
            print("Please enter an integer between 1 and 5\n")
            continue#reject user input
        addme = {"question": quest, "answers": ans, "difficulty": diff}#compile data into a dict
        data.append(addme)#save dictionary to the data list
        pass

    elif choice == 'B':
        saveChanges(data)#too annoyoing to spam, seperate save option


    elif choice == 'L':
        if data == []:
            print("You have no questions")
            continue
        print("Your current questions are:\n")
        for indexy, entry in enumerate(data, start = 1):
            print(str(indexy) + ": " + str(entry["question"]))
        continue


    elif choice == 'S':
        # Search the current questions.
        # for string in data
        searchme = inputSomething("Enter your search term\n> ")
        foundsomething = False
        for questn in data:
            indx = data.index(questn)#why python why
            indxnum = indx + 1
            if searchme in questn["question"]:
                print(str(indxnum) + ": " + str(data[indx]["question"]) + "\nValid Answers: " + str(data[indx]["answers"] ).strip("[]") + "\nDifficulty: " + str(data[indx]["difficulty"]) + "\n")
                foundsomething = True
        if foundsomething == False:
            print("Sorry but we found nothing containing:", searchme)



    elif choice == 'V':
        # View a question.
        showme = inputInt("Enter in the question number you would like to view:\n> ") - 1
        if data == []:
            print("There is no data")
            continue
        try:
            print(str(showme + 1) + ": " + str(data[showme]["question"]) + "\nValid Answers: " + str(data[showme]["answers"] ).strip("[]") + "\nDifficulty: " + str(data[showme]["difficulty"]) + "\n")
        except:
            print("There is no question number", showme + 1)
            continue



    elif choice == 'D':
        # Delete a question.
        deleteme = inputInt("Enter in the question number you would like to delete:\n> ") - 1
        try:
            if data[deleteme]:
                del data[deleteme]
                print("Entry", str(deleteme + 1), "deleted.")
                continue
        except:
            print("Sorry but that question number is not available")
            continue


    elif choice == 'Q':
        saveChanges(data)
        print('Leaving quizle... Goodbye!')
        break

    else:
        print("invalid choice\n")
        continue#do we evne need this?
