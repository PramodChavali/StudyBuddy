from tkinter import *
from time import time, sleep
import questions
import random

#set up timer
startTime = time()

global grade, subject, frequency, unit, screen, midScreenX, midScreenY, accuracy, numQuestions, questionsRight

#get initial values from text files
numQuestions = 0
questionsRight = 0
accuracy = "undefined"

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

file = open("unit.txt", "r")
unit = file.read(-1)
file.close()


class response:
    def __init__(self, question, isAnswer):
        self.question = question
        self.isAnswer = isAnswer
        
#starts the timer and the question loop
def startTimer():

    global screen, root, midScreenX, midScreenY
    startTime = time()
    
    while True:
        if int(time() - startTime) >= frequency:

            file = open("stopped.txt", "r")
            stoppedOrNot = file.read(-1)
            break

    if stoppedOrNot == "False": #if timer has ended and it is time to hit the user with a question

        #set up tkinter window but don't display it yet
        stoppedOrNot = ""
        root = Tk()
        root.title("STUDY BUDDY TIME!")
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        screen = Canvas(root, width=screen_width, height=screen_height, bg="#2a243b")

        midScreenX = screen_width // 2
        midScreenY = screen_height // 2

        GenerateQuestions()

    else:
        pass #end studying :(

def GenerateQuestions():

    global grade, subject, unit

    file = open("prevQuestion.txt", "r")
    prevQuestion = file.read(-1)
    file.close()


    while True:

        #prompt to generate the question (its hella long lmao)
        geminiPrompt = f"You are a helpful assistant that creates educational multiple choice questions based on the given prompts. The questions should all be from the ontario curriculum for high school, the grade and subject will be specified in the prompt Here is the prompt to create the question: Create a multiple-choice question for a high school student in grade {grade} studying the course {subject}. The student would like to study the following units in this course: {unit}. The question should be based on the Ontario curriculum and should have three answer choices (Answer A, Answer B and Answer C), do not label them at all as A B and C or 1 2 and 3, etc. Word the answers in a way where they do not go over 100 characters. The 3rd answer should always be the correcet answer (Answer C). Ensure that all the possible answers are different, and make sure the questions properly relate to the subject {subject}. Ensure that the question is not similar to the previous question which is this: {prevQuestion}. Dont be afraid to give word problems, just make the answer multiple choice. Do not include any special unicode characters, subscripts or super scripts, or accents on letters. Produce the response in exactly this format but do not include the brackets: (Question) | (Answer A) | (Answer B) | (Answer C). Here is an example of a good response: A clothing store marks up its items by 30%. If a shirt costs the store $15, what will be the selling price? | $17.50 | $18.00 | $19.50"
        

        try:
            #get the question from gemini over in the questions file
            questionArray = questions.main(geminiPrompt) #generate question

            file = open("prevQuestion.txt", "w")
            file.write(questionArray[0])  # save the question to a file so it can be used for the previous question later on
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
            break  # exit the loop if the question was generated successfully

        except UnicodeEncodeError: #if gemini tries any unicode bullshit we just generate a new question
            print("Unicode error, generating new question...")

    SetUpQuestions(answerA=answerA, answerB=answerB, answerC=answerC, question=question)

def SetUpQuestions(answerA, answerB, answerC, question):

    answers = [answerA, answerB, answerC]
    
    #create a response object for each answer
    response1 = response(answers[0], False)
    response2 = response(answers[1], False)
    response3 = response(answers[2], True)

    #put them in here
    responses = [response1, response2, response3]
    random.shuffle(responses)  # shuffle the responses to randomize their order

    for i in range(len(responses)):
        print("responses", responses[i].question)


    #AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH    

    #if gemini yaps too much when making the question we gotta print it in multiple lines
    #split the question into parts
    questionParts = question.split(" ")
    print(questionParts, "questionParts")
    groups = []
    totalWords = []
    stringHolder = ""

    #the splitting loop
    for i in range(len(questionParts)):
        
        #gets splits into groups of 80ish characters
        if i == len(questionParts) - 1 and len(stringHolder) + len(questionParts[i]) <= 80:
            stringHolder += questionParts[i] + " "
            groups.append(stringHolder)
            stringHolder = ""

        elif len(stringHolder) + len(questionParts[i]) <= 80:
            stringHolder += questionParts[i] + " "

        elif len(stringHolder) + len(questionParts[i]) > 80:
            groups.append(stringHolder)
            stringHolder = questionParts[i] + " "

    if stringHolder.strip():
        groups.append(stringHolder) #put on last little bit

    for i in range(len(totalWords)):
        groups += totalWords[i] #add them all to groups array which is printed

    questionY = 50
    print(groups)
    SetUpScreen(groups, questionY, responses)

def SetUpScreen(groups, questionY, responses):

    questionY = 50
    print("Setting up screen...")

    global screen, root, midScreenX, midScreenY, accuracy
    
    #prints the quesion in all its parts
    for i in range(len(groups)):
        screen.create_text(midScreenX, questionY, text=groups[i], font="Arial 30", fill="white")
        questionY += 60

    print(responses[0].question, "response1 question")
    print(responses[1].question, "response2 question")
    print(responses[2].question, "response3 question")
    
    #put the answers on the screen
    screen.create_text(midScreenX, questionY + 100, text=f"A: {responses[0].question}", font="Arial 20", fill="white")
    screen.create_text(midScreenX, questionY + 200, text=f"B: {responses[1].question}", font="Arial 20", fill="white")
    screen.create_text(midScreenX, questionY + 300, text=f"C: {responses[2].question}", font="Arial 20", fill="white")

    #put accuracy on the screen
    screen.create_text(midScreenX, questionY + 550, text=f"Accuracy: {accuracy}", font="Arial 20", fill="white")

    #buttons for each answer
    buttonA = Button(root, text="A", font="arial 20", command=lambda: onButtonClick(responses[0]))
    screen.create_window(midScreenX - 100, questionY + 450, window=buttonA)

    buttonB = Button(root, text="B", font="arial 20", command=lambda: onButtonClick(responses[1]))
    screen.create_window(midScreenX, questionY + 450, window=buttonB)

    buttonC = Button(root, text="C", font="arial 20", command=lambda: onButtonClick(responses[2]))
    screen.create_window(midScreenX + 100, questionY + 450, window=buttonC)

    #screen is finally displayed
    screen.pack()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True) #even if the user tries to alt + tab it stays on top MWAHAHAHAHAHAHHAHAHAHAHAH i love tkinter if only i could override alt + f4
    root.protocol("WM_DELETE_WINDOW", lambda: onAltF4(groups, questionY, responses)) #if they try to alt f$ THEY CANT MWAHHAHAHAHAHAHAHAHAHAH
    screen.mainloop()
    
def onButtonClick(response):
        
        global screen, root, midScreenX, midScreenY, accuracy, numQuestions, questionsRight

        numQuestions += 1

        if response.isAnswer: #if the answer is correct
            
            #accuracy calculation
            questionsRight += 1
            accuracy = str(round((questionsRight / numQuestions), 2) * 100) + "%"

            #delete everything and close the window, start the timer again
            screen.delete("all")
            screen.create_text(midScreenX, midScreenY, text="Correct!", font="Arial 50", fill="green")
            screen.update()
            sleep(1)
            root.destroy()
            startTimer()

            

        else:
            
            #accuracy calculation
            accuracy = str(round((questionsRight / numQuestions), 2) * 100) + "%"

            #delete everything and close the window, but this time generate a new question
            screen.delete("all")
            screen.create_text(midScreenX, midScreenY, text="Incorrect!", font="Arial 50", fill="red")
            screen.create_text(midScreenX, midScreenY + 100, text="Generating new question...", font="Arial 30", fill="red")
            screen.update()
            sleep(1)
            screen.delete("all")
            GenerateQuestions()


def onAltF4(groups, questionY, responses):

    screen.delete("all")
    SetUpScreen(groups, questionY, responses) #they cant leave lmao

if __name__ == "__main__":
    startTimer()


