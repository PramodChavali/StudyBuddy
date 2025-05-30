from tkinter import *
from time import time, sleep
import questions
import random

#set up timer



startTime = time()

global grade, subject, frequency, screen, midScreenX, midScreenY

file = open("frequency.txt", "r")
frequency = float(file.read(-1))
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

    global screen, root, midScreenX, midScreenY
    startTime = time()
    
    while True:
        if int(time() - startTime) >= frequency:

            file = open("stopped.txt", "r")
            stoppedOrNot = file.read(-1)
            break

    if stoppedOrNot == "False":

        stoppedOrNot = ""
        root = Tk()
        root.title("ANSWER OR DIE")
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        screen = Canvas(root, width=screen_width, height=screen_height, bg="#2a243b")

        midScreenX = screen_width // 2
        midScreenY = screen_height // 2

        GenerateQuestions()

    else:
        pass #end studying :(

def GenerateQuestions():

    global grade, subject

    file = open("prevQuestion.txt", "r")
    prevQuestion = file.read(-1)
    file.close()


    while True:

        geminiPrompt = f"You are a helpful assistant that creates educational multiple choice questions based on the given prompts. The questions should all be from the ontario curriculum for high school, the grade and subject will be specified in the prompt Here is the prompt to create the question: Create a multiple-choice question for a high school student in grade {grade} studying the course {subject}. The question should be based on the Ontario curriculum and should have three answer choices (Answer A, Answer B and Answer C), do not label them at all as A B and C or 1 2 and 3, etc. The 3rd answer should always be the correcet answer (Answer C). Ensure that all the possible answers are different, and make sure the questions properly relate to the subject {subject}. Ensure that the question is not similar to the previous question which is this: {prevQuestion}. Dont be afraid to give word problems, just make the answer multiple choice. Do not include any special unicode characters, subscripts or super scripts, or accents on letters. Produce the response in exactly this format but do not include the brackets: (Question) | (Answer A) | (Answer B) | (Answer C)"
        

        try:
            questionArray = questions.main(geminiPrompt) #generate question

            file = open("prevQuestion.txt", "w")
            file.write(questionArray[0])  # save the question to a file
            file.close()

            print(questionArray)

            answerA = questionArray[1]
            answerB = questionArray[2]
            answerC = questionArray[3]
            question = questionArray[0]

            print("NOW IN GENERATE QUESTIONS")
            print(question, "question")
            print(answerA, "answerA")
            print(answerB, "answerB")
            print(answerC, "answerC")
            
            if answerA == answerB or answerA == answerC or answerB == answerC:
                print()

            else:
                break
            

        except UnicodeEncodeError:
            print("Unicode error, generating new question...")

    SetUpQuestions(answerA=answerA, answerB=answerB, answerC=answerC, question=question)

def SetUpQuestions(answerA, answerB, answerC, question):

    answers = [answerA, answerB, answerC]
    

    response1 = response(answers[0], False)
    #answers.remove(answerA)  # remove the chosen answer from the list
    response2 = response(answers[1], False)
    #answers.remove(answerB)
    response3 = response(answers[2], True)
    #answers.remove(answerC)

    responses = [response1, response2, response3]
    random.shuffle(responses)  # shuffle the responses to randomize their order

    for i in range(len(responses)):
        print("responses", responses[i].question)


    #AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH    

    questionParts = question.split(" ")
    prevIndex = 0
    print(questionParts, "questionParts")
    groups = []
    totalWords = []
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


    for i in range(len(totalWords)):
        groups += totalWords[i]
    questionY = 50
    print(groups)
    SetUpScreen(groups, questionY, responses)

def SetUpScreen(groups, questionY, responses):

    print("Setting up screen...")

    global screen, root, midScreenX, midScreenY
    

    for i in range(len(groups)):
        screen.create_text(midScreenX, questionY, text=groups[i], font="Arial 30", fill="white")
        questionY += 60

    print(responses[0].question, "response1 question")
    print(responses[1].question, "response2 question")
    print(responses[2].question, "response3 question")
    

    screen.create_text(midScreenX, questionY + 100, text=f"A: {responses[0].question}", font="Arial 20", fill="white")
    screen.create_text(midScreenX, questionY + 200, text=f"B: {responses[1].question}", font="Arial 20", fill="white")
    screen.create_text(midScreenX, questionY + 300, text=f"C: {responses[2].question}", font="Arial 20", fill="white")


    buttonA = Button(root, text="A", font="arial 20", command=lambda: onButtonClick(responses[0]))
    screen.create_window(midScreenX - 100, questionY + 450, window=buttonA)

    buttonB = Button(root, text="B", font="arial 20", command=lambda: onButtonClick(responses[1]))
    screen.create_window(midScreenX, questionY + 450, window=buttonB)

    buttonC = Button(root, text="C", font="arial 20", command=lambda: onButtonClick(responses[2]))
    screen.create_window(midScreenX + 100, questionY + 450, window=buttonC)

    screen.pack()
    root.attributes("-fullscreen", True)
    root.bind("<Key>", KeyPressHandler)
    screen.mainloop()
    
def onButtonClick(response):
        
        global screen, root, midScreenX, midScreenY

        if response.isAnswer:

            screen.delete("all")
            screen.create_text(midScreenX, midScreenY, text="Correct!", font="Arial 50", fill="green")
            screen.update()
            sleep(1)
            root.destroy()
            startTimer()

        else:
            screen.delete("all")
            screen.create_text(midScreenX, midScreenY, text="Incorrect!", font="Arial 50", fill="red")
            screen.update()
            sleep(1)
            screen.delete("all")
            GenerateQuestions()

def KeyPressHandler(event):
    global screen, root
    print("key pressed")
    sleep(2)
    root.attributes("-fullscreen", True)

if __name__ == "__main__":
    startTimer()


