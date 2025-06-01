from tkinter import *
from subprocess import Popen
import popup

#set up tkinter
root = Tk()
root.title("Study Buddy!")
screen = Canvas(root, width=800, height=600, bg="#2a243b")
screen.pack()

#set up for dropdown menu
questionStage = 0
selectedOption = StringVar()
selectedOption.set("")

#tells the question timer that program is still going
file = open("stopped.txt", "w")
file.write("False")
file.close()

#show the first question
def showGradeQuestion():
    #get the grade of the user
    screen.delete("all")
    showQuestions("what grade are you in?", "", "")

    #dropwdown menu
    dropdownOptions = ["9", "10", "11", "12"]
    selectedOption.set(dropdownOptions[0])
    dropdown = OptionMenu(root, selectedOption, *dropdownOptions)
    screen.create_window(400, 400, window=dropdown)

    #submit button
    submitButton = Button(root, text="Submit", font="arial 20", command=onGradeSubmit)
    screen.create_window(400, 500, window=submitButton)

def showFrequencyQuestion():
    #get how often we can troll the user with questions
    screen.delete("all")
    showQuestions("How often would you", "like to get questions?", " (in minutes)")

    #dropdown menu
    dropdownOptions = ["0.1", "0.5", "2", "5", "10", "15", "20"]
    selectedOption.set(dropdownOptions[0])
    dropdown = OptionMenu(root, selectedOption, *dropdownOptions)
    screen.create_window(400, 400, window=dropdown)
    

    #submit button
    submitButton = Button(root, text="Submit", font="arial 20", command=onFrequencySubmit)
    screen.create_window(400, 500, window=submitButton)

def showSubjectQuestion():

    #depnding on the grade, give different subjects
    #get the grade

    file = open("grade.txt", "r")
    grade = int(file.read(-1))
    file.close()

    #subjects for each grade
    if grade == 9:
        dropdownOptions = ["Math", "Science", "Geography", "French"]

    elif grade == 10:
        dropdownOptions = ["Math", "Science", "Buisiness", "Careers", "Civics", "French"]

    elif grade == 11:
        dropdownOptions = ["Functions", "Functions and Applications", "Foundations for College Math", "Intro to Anth, Soch, and Psych", "Physics", "Chemistry", "Biology", "Earth and Space Science", "French", "Natural Disasters", "Crimes against Humanity", "World History to the 15th Century", "Law","Marketing", "Accounting", "Entrepreneurship"]

    elif grade == 12:
        dropdownOptions = ["Calc and Vectors", "Foundations for College Math", "Advanced Functions", "Data Management", "Earth and Space Science", "Medical Sciences", "Physics", "Chemistry", "Biology", "French", "International Buisness", "Accounting", "Buisiness Leadership", "Politics", "Law", "Canadian and World Issues", "History since the 15th century"]


    #what subjects they want to study
    screen.delete("all")
    showQuestions("What subjects would you", "like to study?", "")
    
    #dropdown menu
    
    selectedOption.set(dropdownOptions[0])
    dropdown = OptionMenu(root, selectedOption, *dropdownOptions)
    screen.create_window(400, 400, window=dropdown)

    #submit button
    submitButton = Button(root, text="Submit", font="arial 20", command=onSubjectSubmit)
    screen.create_window(400, 500, window=submitButton)

def showUnitQuestion():
    #get the unit of the subject
    screen.delete("all")
    showQuestions("What unit do you", "want to study?", "")

    
    unitBox = Entry(root, font = "arial 20")
    screen.create_window(400, 400, window=unitBox)

    #submit button
    submitButton = Button(root, text="Submit", font="arial 20", command=lambda: onUnitSubmit(unitBox))
    screen.create_window(400, 500, window=submitButton)

def endSetup():
    #start the popup questions timer and file
    screen.delete("all")
    showQuestions("Setup Complete!", "Press here to", "stop studying")
    stopStudyingButton = Button(root, text="Stop Studying", font="arial 15", command=stopStudying)
    screen.create_window(400, 550, window=stopStudyingButton)
    Popen(["python", "popup.py"])

def showQuestions(question, question2, question3):

    #makes showing questions easier
    screen.create_text(400, 100, text=question, fill="white", font=("Arial", 50), anchor="center")
    screen.create_text(400, 200, text=question2, fill="white", font=("Arial", 50), anchor="center")
    screen.create_text(400, 300, text=question3, fill="white", font=("Arial", 50), anchor="center")

def saveToFile(filepath, answer):
    #saves the answer to a file
    file = open(filepath, "w")
    file.write(str(answer))
    file.close()

def onGradeSubmit():
    #save the grade and show the next question
    print("selected grade: ", selectedOption.get())
    saveToFile("grade.txt", selectedOption.get())
    showFrequencyQuestion()

def onFrequencySubmit():
    #save the frequency and show the next question
    print("selected frequency: ", selectedOption.get())
    saveToFile("frequency.txt", selectedOption.get())
    showSubjectQuestion()

def onSubjectSubmit():
    #save the subjects and end the setup
    print("selected subjects: ", selectedOption.get())
    saveToFile("subjects.txt", selectedOption.get())
    showUnitQuestion()

def onUnitSubmit(textBox):
    #save the unit and end the setup
    print("selected unit: ", textBox.get())
    saveToFile("unit.txt", textBox.get())
    endSetup()

def stopStudying():
    #stop the program
    file = open("stopped.txt", "w")
    file.write("True")
    file.close()
    root.destroy()  # Close the setup window
    print("end of program")

showGradeQuestion()
root.mainloop()