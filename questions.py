from tkinter import *
from time import time, sleep
from google import genai as gemini
from random import uniform
import os
from dotenv import load_dotenv

load_dotenv()
apiKey = os.getenv("API_KEY")



####################################################################################

#subject and grade
file = open("subjects.txt", "r")
subject = file.read(-1)
file.close()

file = open("grade.txt", "r")
grade = int(file.read(-1))
file.close()

####################################################################################




def SetUpQuestion(prompt):
    client = gemini.Client(api_key=apiKey)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents= (prompt),

    )

    return response.text

def main(prompt):
    geminiResponse = SetUpQuestion(prompt)
    print(geminiResponse)

    question = geminiResponse.split("|")[0].strip()
    answerA = geminiResponse.split("|")[1].strip()
    answerB = geminiResponse.split("|")[2].strip()
    answerC = geminiResponse.split("|")[3].strip()

    print(question)
    print(answerA)
    print(answerB)
    print(answerC)

    file = open("questions/question.txt", "w")
    file.write(question)   
    file.close()

    file = open("questions/answerA.txt", "w")
    file.write(answerA)
    file.close()

    file = open("questions/answerB.txt", "w")
    file.write(answerB)
    file.close()

    file = open("questions/answerC.txt", "w")
    file.write(answerC)
    file.close()

