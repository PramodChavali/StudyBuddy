from tkinter import *

root = Tk()
root.title("START STUDYING")
screen = Canvas(root, width=800, height=600, bg="#2a243b")
screen.pack()

questionStage = 0
global textBox
global response

def getInput():
    response = textBox.get('1.0', 'end-1c')

def showInputButton():
    inputButton = Button(root, text="Submit", command=getInput)
    inputButton.pack()

def showQuestions(question):
    screen.create_text(400, 300, text=question, fill="white", font=("Arial", 50), anchor="center")

if questionStage == 0:

    while True:
        textBox = Text(root, height = 5, width = 40)
        textBox.pack()
        showInputButton()
        showQuestions("what grade are you in? (1-12)")
        
        try:
            grade = int(response)

        except ValueError:
            screen.create_text(400, 350, text="Please enter a valid number.", fill="red", font=("Arial", 20), anchor="center")
        
        else:
            break;



screen.mainloop()