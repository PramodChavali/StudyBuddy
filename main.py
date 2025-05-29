from tkinter import *
from subprocess import Popen

root = Tk()
root.title("START STUDYING SETUP")
screen = Canvas(root, width=800, height=600, bg="#2a243b")
screen.pack()

questionStage = 0
selectedOption = StringVar()
selectedOption.set("")

file = open("stopped.txt", "w")
file.write("False")
file.close()

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
    #get how often we can troll the user
    screen.delete("all")
    showQuestions("How often would you", "like to get questions?", " (in minutes)")

    #dropdown menu
    dropdownOptions = ["0.1", "5", "10", "15", "20"]
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

def endSetup():
    screen.delete("all")
    showQuestions("Setup Complete!", "Press here to", "stop studying")
    #root.after(2000, root.destroy)  # Close the window after 2 seconds
    stopStudyingButton = Button(root, text="Stop Studying", font="arial 15", command=stopStudying)
    screen.create_window(400, 550, window=stopStudyingButton)
    Popen(["python", "popup.py"])

def showQuestions(question, question2, question3):
    screen.create_text(400, 100, text=question, fill="white", font=("Arial", 50), anchor="center")
    screen.create_text(400, 200, text=question2, fill="white", font=("Arial", 50), anchor="center")
    screen.create_text(400, 300, text=question3, fill="white", font=("Arial", 50), anchor="center")

def saveToFile(filepath, answer):
    with open(filepath, "w") as file:
        file.write(str(answer))

def onGradeSubmit():
    print("selected grade: ", selectedOption.get())
    saveToFile("grade.txt", selectedOption.get())
    showFrequencyQuestion()

def onFrequencySubmit():
    print("selected frequency: ", selectedOption.get())
    saveToFile("frequency.txt", selectedOption.get())
    showSubjectQuestion()


def onSubjectSubmit():
    print("selected subjects: ", selectedOption.get())
    saveToFile("subjects.txt", selectedOption.get())
    endSetup()

def stopStudying():
    file = open("stopped.txt", "w")
    file.write("True")
    file.close()
    root.destroy()  # Close the setup window
    print("end of program")

showGradeQuestion()
root.mainloop()