# Zachary Wibowanto

# Import the required modules.
import tkinter
import tkinter.messagebox
import json
import random


def inputSomething(prompt):#XXX
    while True:
        entry = input(prompt)#multiple entries not allowed for input function?
        try:
            stringput = entry.strip().upper() #remove whitespace at the beginning and end, then sets to uppercase
            return stringput
        except:
            print("Please try something else, you're not doing it right")
            continue

class ProgramGUI:

    def __init__(self):

        self.QuestionsToPlay = 5#number of questions to play XXX
        self.answeredYN = False
        self.score = 0
        self.maxscorepossible = 0
        self.startupDone = False

        try:
            file = open("data.json","r")
            data = json.load(file)
            file.close()
            if len(data) < self.QuestionsToPlay:#Quiz requires 5 questions.
                tkinter.messagebox.showinfo("Error","There are not enough questions to complete this quiz.\n\nThere are only "  + str(len(data)) + " questions available. and you need " + str(self.QuestionsToPlay) +" questions to use Quizle.")
                print("Error: There are not enough questions to complete this quiz. There are only "  + str(len(data)) + " questions available.")
                quit()#force exit, though user is given an option with risk
            #else load schite normally
            print("data.json loaded successfully, there are", len(data), "questions available, loaded " + str(self.QuestionsToPlay))
        except:#no file present, crash program prematurely
            print("Error: No data.json file was found or was corrupted. Please set up some questions using admin.py before using this program")
            tkinter.messagebox.showerror("Error", "No data.json file was found or was corrupted.\n\nPlease set up some questions using admin.py before using this program")
            quit()#force exit, though user is given an option with risk

        # This is the constructor of the class.
        # It is responsible for loading and reading the data file and creating the user interface.
        # See Points 1 to 6 "Constructor of the GUI Class of quizle.py" section of the assignment brief.
        self.main = tkinter.Tk()
        #self.main.geometry("720x128")
        self.main.title("Quizle the Quizzer")
        self.main.resizable(width=False, height=False)

        #Get the list of questions to be used
        self.questAvail = random.sample(list(data), self.QuestionsToPlay)
        for stuff in self.questAvail:
            self.maxscorepossible += stuff["difficulty"]

        self.questplays = int(0)#keeps track of te number of questions played, used for data[]status
        #rand.sample(range, number of samples)

        #self.questionsList = rand.randsample(data[]["question"])
        self.questioncurrent = tkinter.StringVar()
        self.questioncurrent.set(self.loadQuestion)#trace("w", self.loadQuestion)
        self.answer = tkinter.StringVar()


        self.scoremsg = tkinter.Label(self.main, fg = "Grey", text="Welcome to Quizle.")
        self.scoremsg.grid(row=0)

        self.quizquestion = tkinter.Label(self.main, text="Press 'Start Quiz' to start the quiz!")
        self.quizquestion.grid(row=1, column=0)

        self.inputbox = tkinter.Entry(self.main, width=50, textvariable=self.answer)
        self.inputbox.grid(row=2, column=0)#TODO fetch for checkanswer
        #self.inputbox.pack(side = 'left')#side='bottom')


        #Button functions call a command
        self.buttonGo = tkinter.Button(self.main, text="Start Quiz", command=self.loadQuestion, fg="Green")#NextQuestionPlz() )#
        self.buttonGo.grid(row=0, column=1)
        self.buttonCheckAnswer = tkinter.Button(self.main, text="CheckAnswer", command=self.checkAnswer, state="disabled")
        self.buttonCheckAnswer.grid(row=1, column=1)
        #we don't need to modify the quit button later, so it can be done in one line
        self.buttonQuit = tkinter.Button(self.main, text="Quizle Sucks!", command=self.quit).grid(row=2, column=1)

        #Pack dat button!
        #self.buttonQuit.pack(side='right')
        #self.buttonGo.pack(side='right')
        #self.buttonCheckAnswer.pack(side='right')

        tkinter.mainloop()

    def loadQuestion(self):
        # This method is responsible for displaying a question in the GUI,
        # as well as showing the special message for difficult questions and showing the user's current progress
        # See Point 1 of the "Methods in the GUI Class of quizle.py" section of the assignment brief.

        if self.startupDone == False:#skip.
            self.buttonCheckAnswer.config(state="active")
            self.buttonGo.config(text="New Question", fg="Black")
            self.startupDone = True
        else:
            if str(self.answer.get()) == "": #nothing there? admin.py is proofed against non-existant entries
                tkinter.messagebox.showinfo("WAIT A SEC...", "You entered nothing!")
                return

        self.possiblescoreincrement = self.questAvail[self.questplays]["difficulty"]
        self.answeredYN = False

        #if self.questplays != 0:#don't know how to refresh the field, so delete and replace
            #self.quizquestion.grid_forget()

        if self.questplays < self.QuestionsToPlay:
            self.inputbox.delete(0, 'end')#clear entry
            self.scoremsg.config(text="Your score is: " + str(self.score) + " out of a maximum of " + str(self.maxscorepossible) )

            #draw question
            self.quizquestion.config(text=str(self.questplays + 1) + "/" + str(self.QuestionsToPlay) + ": " + str(self.questAvail[self.questplays]["question"]) + "\nDifficulty: " + str(self.questAvail[self.questplays]["difficulty"]) )
            #increment question number
            self.questplays += 1
        else:
            self.scoremsg.config(fg="red", text="Game Over!")
            self.quizquestion.config(fg="green", text="Your final score is: " + str(self.score) + " out of a maximum of " + str(self.maxscorepossible) + " possible points.")



    def checkAnswer(self):
        # This method is responsible for determining whether the user's answer is correct and showing a Correct/Incorrect messagebox.
        # It also checks how many questions have been asked to determine whether or not to end the game.
        # See Point 2 of the "Methods in the GUI Class of quizle.py" section of the assignment brief.
        #self.wrongimg = tkinter.Photoimage(file="nooooooo_luke_skywalker.gif")#XXX
        correct = False#Unless corrected, you are always wrong.

        #strip contents to its bare nakedness
        self.compare = str(self.answer.get()).upper().strip()

        #Are they the same?
        if self.compare in self.questAvail[self.questplays -1]["answers"]:
            correct = True

        #dailogue boxes
        if correct == True:
            tkinter.messagebox.showinfo("Result:", "Well done, you are correct!\nYou earnt " + str(self.possiblescoreincrement) + " point(s)!")
            self.score += self.possiblescoreincrement
            self.scoremsg.config(text="Your score is: " + str(self.score) + " out of a maximum of " + str(self.maxscorepossible) + " possible points. Press 'New Question' to continue." )
            self.possiblescoreincrement = 0 #prevent re-entering question exploit
        else:#every time they get te question wrong they lose one point in each attempt
            if self.possiblescoreincrement > 0:
                self.possiblescoreincrement -= 1
                tkinter.messagebox.showerror("Result:", "Wrong!\nDon't forget to check your spelling!")
            else:
                tkinter.messagebox.showerror("Result:", "Wrong!\nYou might as well go onto the next question as answering this one will no longer earn you points.")


            #self.imgbutton = tkinter.Button(self.checkAnswer,self.wrongimg, command=self.showBox)
            #self.imgbutton.pack()

    def quit(self):
        quit()#quit ye stupid program

# Create an object of the ProgramGUI class to begin the program.
gui = ProgramGUI()
