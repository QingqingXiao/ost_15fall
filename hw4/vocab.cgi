#!/usr/bin/python
import cgi
import cgitb
import os
import random

cgitb.enable()
form = cgi.FieldStorage()

#Print header
print 'Content-Type: text/html'
print 
print "<html>"
print "<head>"
print "<title>OST Vocabulary Quiz</title>"
print "</head>\n"
print "<br>"
print "<body>\n"

#relative path
dataPath="/home/unixtool/data/vocab.dat"
path="w.cgi"

#generate html code for a single quesiton
def generateQuestionList(index, questions, path):
    questionString="<p><LI><b>" + questions[index][0] + "</b>: <br>"
    questionString += "<input type=hidden name=a" + str(index) + " value=" + str(questions[index][1]) + ">"
    questionString += "<input type=hidden name=w" + str(index) + " value=" + questions[index][0] + ">"
    questionString += "<input type=radio name=q" + str(index) + " value=0 >" + questions[index][2][0] + "<br>"
    questionString += "<input type=radio name=q" + str(index) + " value=1>" + questions[index][2][1] + "<br>"
    questionString += "<input type=radio name=q" + str(index) + " value=2>" + questions[index][2][2] + "<br>"
    questionString += "<input type=radio name=q" + str(index) + " value=3>" + questions[index][2][3] + "<br>"
    return questionString

#generate single question entry for questions list
#data structure of entry is (correctWord, correctOptionPosition, [fourRandomOption])
def generateQuestion(listName, questions, numOfQuestion):
    for i in range(0, numOfQuestion):
    	word=listName[i][0]
        ans=listName[i][1]
        options=[listName[i+4][1],listName[i+8][1],listName[i+12][1]]
        answerPos=random.randint(0,3)
        options.insert(answerPos, ans)
        questions.append((word, answerPos, options))

def readFromFile(dataEnties, dataPath):
    f = open(dataPath, 'rw')
    for each in f.readlines():
        dataEnties.append(each)
    f.close()

#If the page is loaded for the first time, show the questions
if len(form) == 0:
    print "<H1> Vocabulary Quiz </H1>"
    #read vocabulary data from file
    readFromFile(dataEnties, dataPath)
    '''
    dataEnties = []
    f = open(dataPath, 'rw')
    for each in f.readlines():
        dataEnties.append(each)
    f.close()
    '''

    nounList = []
    verbList = []
    adjList = []

    #store each kind of words into specific array
    #data structure is (word, explaination)
    for i in range(0, len(dataEnties)):
        record = dataEnties[i].replace("\n", "").split('|')
        if(record[1] == "n."):
            nounList.append((record[0], record[2]))
        if(record[1] == "v."):
            verbList.append((record[0], record[2]))
        if(record[1] == "adj."):
           adjList.append((record[0], record[2]))

    #shuffle each list
    random.shuffle(nounList)
    random.shuffle(verbList)
    random.shuffle(adjList)

    questions = []
    #generate all questions
    generateQuestion(nounList, questions, 4)
    generateQuestion(verbList, questions, 3)
    generateQuestion(adjList, questions, 3)
    #shuffle the order of questions
    random.shuffle(questions)

    #generate html code for questions
    allQuestionList=""
    print "<form action=%s method=post target=_self><OL>" % path
    for i in range(0,10):
        allQuestionList += generateQuestionList(i, questions, path)
    print allQuestionList
    print "</OL><INPUT TYPE=SUBMIT VALUE=Grade></form>"

#if answers are submitted, show the results
else:
    correctAns=[]
    incorrectAns=[]
    correctCnt=0
    incorrectCnt=0

    #compare the data submitted with the correct ones
    for i in range(0,10):
        ansPosString="a" + str(i)
        ansPos=form.getvalue(ansPosString) #ans value
        ansWordString="w" + str(i)
        ansWord=form.getvalue(ansWordString)
        selectedPosString="q" + str(i)
        selectedPos=form.getvalue(selectedPosString)
        if ansPos == selectedPos:
            correctCnt += 1
            correctAns.append(str(ansWord))
        else:
            incorrectCnt += 1
            incorrectAns.append(str(ansWord))

    #generate html code for result
    resultCntString = "You got <b>" + str(correctCnt) + " of 10 </b> answers correct. <br> <br>"
    print resultCntString

    print """\
    <p>
      <table border=1>
       <tr>
        <th>Correct</th>
        <th>Incorrect</th>
       </tr>
       <tr>
        <td valign=top>
          <font color=green>
    """

    correctAnsString=""
    for i in range(0, len(correctAns)):
        correctAnsString += correctAns[i] + "<br>"

    incorrectAnsString=""
    for i in range(0, len(incorrectAns)):
        incorrectAnsString += incorrectAns[i] + "<br>"

    print correctAnsString

    print """\
          </font>
        </td>
        <td valign=top>
          <font color=red>
    """

    print incorrectAnsString

    print """\
          </font>
        </td>
       </tr>
      </table>
    """

print "</body>"
print "</html>"
