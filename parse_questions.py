import re, sys, json

def hasAnAnswer(line):
    temp = re.search('[(][A|B|C|D][)]', line)
    if temp:
        return temp.group(0)[1]
    return None

if (len(sys.argv) < 2):
    sys.exit("Invalid number of parameters")
else:
    filename = sys.argv[1]

inputfile = open(filename)
outputfile = open(filename + '.parsable', 'w')

my_text = inputfile.readlines()

insideAQuestion = False
comma = ""
questionData = ""
outputfile.writelines('[\n')

for line in my_text:
    answer = hasAnAnswer(line)
    if answer:
        questionData = line.split("(")[0].strip() + "---" + answer
        insideAQuestion = True
    else:
        if line[0] == '~' and line[1] == '~':
            splitdata = questionData.split("---")
            jsondata = {
                'identifier': splitdata[0],
                'answer': splitdata[1],
                'question': splitdata[2],
                'option1': splitdata[3],
                'option2': splitdata[4],
                'option3': splitdata[5],
                'option4': splitdata[6]
            }
            print(json.dumps(jsondata, sort_keys=True, indent=4))
            outputfile.writelines(comma + json.dumps(jsondata, sort_keys=True))
            comma = ",\n"
            questionData = ""
            insideAQuestion = False
        else:
            questionData += "---" + line.strip()

outputfile.writelines('\n]')

inputfile.close()
outputfile.close()
