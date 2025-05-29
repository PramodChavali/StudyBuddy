from tkinter import *
from time import time, sleep
import questions
import random

#set up timer

root = Tk()
root.title("STUDDY BUDDY")
screen = Canvas(root, width=1920, height=1080, bg="#2a243b")
screen.pack()

startTime = time()

global grade, subject, frequency

file = open("frequency.txt", "r")
frequency = int(file.read(-1))
file.close()

frequency = frequency * 60  # convert minutes to seconds

file = open("subjects.txt", "r")
subject = file.read(-1)
file.close()

file = open("grade.txt", "r")
grade = int(file.read(-1))
file.close()

class response:
    def __init__(self, question, isAnswer):
        self.question = question
        self.isAnswer = isAnswer
        


def startTimer():
    startTime = time()
    while True:
        if int(time() - startTime) >= frequency:
            break

    GenerateQuestions()

def GenerateQuestions():

    global grade, subject

    geminiPrompt = f"You are a helpful assistant that creates educational multiple choice questions based on the given prompts. The questions should all be from the ontario curriculum for high school, the grade and subject will be specified in the prompt Here is the prompt to create the question: Create a multiple-choice question for a high school student in grade {grade} studying the course {subject}. The question should be based on the Ontario curriculum and should have three answer choices labeled A, B, and C. The 3rd answer should always be the correcet answer (Answer C). Make sure that there are no duplicate answers. Dont be afraid to give word problems, just make the answer multiple choice. Do not include any special unicode characters, like subscripts or super scripts. Produce the response in exactly this format: (Question) | (Answer A) | (Answer B) | (Answer C)"


    questions.main(geminiPrompt) #generate question

    #get answers
    file = open("questions/question.txt", "r")
    question = file.read(-1)
    file.close()

    print(question)

    file = open("questions/answerA.txt", "r")
    answerA = file.read(-1)
    file.close()

    file = open("questions/answerB.txt", "r")
    answerB = file.read(-1)
    file.close()

    file = open("questions/answerC.txt", "r") #correct answer
    answerC = file.read(-1)
    file.close()

    SetUpQuestions(answerA=answerA, answerB=answerB, answerC=answerC, question=question)

def SetUpQuestions(answerA, answerB, answerC, question):

    #shuffle answers
    answers = [answerA, answerB, answerC]

    response1 = response(random.choice(answers), False)
    response2 = response(random.choice(answers), False)
    response3 = response(random.choice(answers), False)

    responses = [response1, response2, response3]

    for i in range(3):
        if responses[i].question == answerC:
            responses[i].isAnswer = True
            

    questionParts = question.split(" ")
    prevIndex = 0
    print(questionParts)
    groups = []
    stringHolder = ""

    for i in range(len(questionParts)):
        
        try:
            if i == len(questionParts) - 1 and len(stringHolder) + len(questionParts[i]) <= 80:
                stringHolder += questionParts[i] + " "
                groups.append(stringHolder)
                stringHolder = ""

            elif len(stringHolder) + len(questionParts[i]) <= 80:
                stringHolder += questionParts[i] + " "

            elif len(stringHolder) + len(questionParts[i]) > 80:
                groups.append(stringHolder)
                stringHolder = ""


        except IndexError:
            
            if len(groups[-1]) + len(questionParts[i]) <= 80:
                stringHolder += questionParts[i] + " "

            else:
                groups.append(stringHolder)
                stringHolder = questionParts[i] + " "
        

    questionY = 100
    print(groups)
    SetUpScreen(groups, questionY, responses)

def SetUpScreen(groups, questionY, responses):

    print("Setting up screen...")

    global screen, root


    for i in range(len(groups)):
        screen.create_text(960, questionY, text=groups[i], font="Arial 30", fill="white")
        questionY += 60

    screen.create_text(960, questionY + 100, text=f"A: {responses[0].question}", font="Arial 20", fill="white")
    screen.create_text(960, questionY + 200, text=f"B: {responses[1].question}", font="Arial 20", fill="white")
    screen.create_text(960, questionY + 300, text=f"C: {responses[2].question}", font="Arial 20", fill="white")


    buttonA = Button(root, text="A", font="arial 20", command=lambda: onButtonClick(responses[0]))
    screen.create_window(960, questionY + 450, window=buttonA)

    buttonB = Button(root, text="B", font="arial 20", command=lambda: onButtonClick(responses[1]))
    screen.create_window(960, questionY + 550, window=buttonB)

    buttonC = Button(root, text="C", font="arial 20", command=lambda: onButtonClick(responses[2]))
    screen.create_window(960, questionY + 650, window=buttonC)

    
    root.attributes("-fullscreen", True)
    screen.mainloop()

def onButtonClick(response):
        
        global screen, root

        if response.isAnswer:

            screen.delete("all")
            screen.create_text(960, 540, text="Correct!", font="Arial 50", fill="green")
            screen.update()
            sleep(1)
            root.destroy()
            startTimer()

        else:
            screen.delete("all")
            screen.create_text(960, 540, text="Incorrect!", font="Arial 50", fill="red")
            screen.update()
            sleep(1)
            screen.delete("all")
            GenerateQuestions()


if __name__ == "__main__":
    startTimer()


