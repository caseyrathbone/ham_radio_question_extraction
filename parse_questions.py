import re, sys, json

def hasAnAnswer(line):
    temp = re.search('[(][A-D][)]', line)
    if temp:
        return temp.group(0)[1]
    return None

def trimAns(answer):
    return answer[3:]

def getQnA(answer, optA, optB, optC, optD):
    if(answer == 'A'):
        ans = optA;
        opts = "[" + optB + ", " + optC + ", " + optD + "]"
    elif (answer == 'B'):
        ans = optB;
        opts = "[" + optA + ", " + optC + ", " + optD + "]"
    elif (answer == 'C'):
        ans = optC;
        opts = "[" + optA + ", " + optB + ", " + optD + "]"
    elif (answer == 'D'):
        ans = optD;
        opts = "[" + optA + ", " + optB + ", " + optC + "]"
    else:
        print("Unknown answer?!?")
        sys.exit("Error parsing input file")
    return ans, opts

if (len(sys.argv) < 2):
    sys.exit("Invalid number of parameters")
else:
    filename = sys.argv[1]

inputfile = open(filename)
outputfile = open(filename + '.json', 'w')

my_text = inputfile.readlines()

insideAQuestion = False
comma = ""
questionData = ""
outputfile.writelines('[')

for line in my_text:
    answer = hasAnAnswer(line)
    if answer:
        questionData = line.split("(")[0].strip() + "---" + answer
        insideAQuestion = True
    else:
        if line[0] == '~' and line[1] == '~':
            print("Q: " + questionData)
            identifier, answer, question, optionA, optionB, optionC, optionD = questionData.split("---")
            answerVal, optsArray = getQnA(answer, trimAns(optionA), trimAns(optionB), trimAns(optionC), trimAns(optionD))
            jsondata = {
                'identifier': identifier,
                'question': question,
                'answer': answerVal,
                'options': optsArray
            }
            #print(json.dumps(jsondata, sort_keys=True, indent=4))
            outputfile.writelines(comma + json.dumps(jsondata, sort_keys=True, indent=4))
            comma = ",\n"
            questionData = ""
            insideAQuestion = False
        else:
            questionData += "---" + line.strip()

outputfile.writelines(']')

inputfile.close()
outputfile.close()
