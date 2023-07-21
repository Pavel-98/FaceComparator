from Base import loadingBase, creatingBase, updatingBase, removingBase

loadingText="завантаження бази"
creatingText="створення бази"
updatingText="оновлення бази"
deletingText="видалення бази"
exitingText="виходу"
exitFromBaseWorkerKey="0"
loadingKey="1"
updatingKey="3"
creatingKey="2"
deletingKey="4"
notRightInstructionText="Не вірна інструкція"
toInputStartText="Увести початкову позицію запису"
toInputEndText="Увести останню позицію запису"
notRightInformationToInput="Не вірно введено дані"

def toInputNumber(text):
    print(text)
    number=int(input())
    return number


def toUpdate():
    try:
        start = toInputNumber(toInputStartText)
        end = toInputNumber(toInputEndText)
        updatingBase(start, end)
    except Exception as e:
        print(notRightInformationToInput)

def doingInstruction(whatToDo):
    if whatToDo==loadingKey:
        loadingBase()
    elif whatToDo==creatingKey:
        creatingBase()
    elif whatToDo==updatingKey:
        toUpdate()
    elif whatToDo==deletingKey:
        removingBase()
    else:
        print(notRightInstructionText)

setting={loadingKey: loadingText, creatingKey: creatingText, updatingKey: updatingText, deletingKey: deletingText, exitFromBaseWorkerKey:exitingText}
def showingInstruction():
    instruction=""
    for key in setting.keys():
        instruction+= " "+ key+" для " + setting[key]
    print(instruction)

def startingWork():
    while True:
        showingInstruction()
        whatToDo=input()
        if whatToDo==exitFromBaseWorkerKey:
            return
        doingInstruction(whatToDo)
