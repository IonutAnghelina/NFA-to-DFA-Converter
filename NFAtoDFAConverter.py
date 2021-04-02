import sys

######Reading the NFA
import sys

fin = open("data.in", "r")

while (1):  # We read the comments and the "Sigma:" line
    line = fin.readline()
    if (line == "Sigma:\n"):
        break

alphabet = []  # We will keep our alphabet in this list

while 1:
    line = fin.readline()  # We read the alphabet
    if line == "End\n":  # We stop when we reach the "End" line
        break
    alphabet.append(line.strip())

D = dict()  # This dictionary will be used to tell if a state is initial or final
states = []  # We will keep our states in this list

while (1):
    line = fin.readline()  # We read the comments and the "States:" line
    if (line == "States:\n"):
        break

while (1):
    line = fin.readline()  # We read the states

    if line == "End\n":  # We stop when we reach the "End" line
        break
    l = line.split(",")

    states.append(l[0].strip())
    initial, final = 0, 0

    for el in l:
        if el.strip() == 'F':
            final = 1
        elif el.strip() == 'S':
            initial = 1

    # D[l[0]].extend([0,0])
    # print(l[0])
    # print(l)
    D[l[0].strip()] = [0, 0]
    # print(l)
    if initial:
        D[l[0].strip()][0] = 1
    else:
        D[l[0].strip()][0] = 0

    if final:
        D[l[0].strip()][1] = 1
    else:
        D[l[0].strip()][1] = 0

while (1):
    line = fin.readline()  # We read the comments and the "Transitions:" line
    if (line == "Transitions:\n"):
        break

transitions = []  # We will keep our transitions in this list

# print(states)

while (1):
    line = fin.readline()  # We read the transitions

    if line == "End\n":  # We stop when we reach the "End" line
        break

    l = line.split(",")

    # print(l[0].strip())

    if l[0].strip() not in states:
        print("The input is not correct")
        exit(0)

    elif l[1].strip() not in alphabet:
        print("The input is not correct")
        exit(0)

    elif l[2].strip() not in states:
        print("The input is not correct")
        exit(0)

    else:
        transitions.append([el.strip() for el in l])

print(alphabet)
print(states)
print(transitions)

alphabetSize = len(alphabet)
statesSize = len(states)

alphabetMapping = dict()
statesMapping = dict()

# print(alphabet)
revStatesMapping = dict()

for (index, word) in enumerate(alphabet):
    alphabetMapping[word] = index

for (index, state) in enumerate(states):
    statesMapping[state] = index
    revStatesMapping[index] = state
# print(statesMapping)
# print(alphabetMapping["word1"])

# print(statesMapping[1])
transitionMatrix = [[set() for i in range(200 * alphabetSize)] for j in range(200 * statesSize)]

for trans in transitions:
    transitionMatrix[statesMapping[trans[0]]][alphabetMapping[trans[1]]].add(statesMapping[trans[2]])
# print(transitionMatrix[2][1])
# from pprint import pprint
# pprint(transitionMatrix)
fin.close()
initialState = 0
for state in states:
    if D[state][0]:
        initialState = state
        break
###########
cnt = 0
fout = open("data.out", "w")

currentStates = set()
currentStates.add(initialState)

newStatesMap = dict()
revNewStatesMap = dict()
# print(transitionMatrix[0][0])
# states=[states[0]]
for state in states:
    if state in revNewStatesMap.keys():  # So it's a new state which is yet undefined
        newStates = revNewStatesMap[state]
        for letter2 in alphabet:
            for state2 in newStates:
                for state3 in transitionMatrix[statesMapping[state2]][alphabetMapping[letter2]]:
                    transitionMatrix[statesMapping[state]][alphabetMapping[letter2]].add(state3)

    for letter in alphabet:
        newStates = frozenset(
            [revStatesMapping[x] for x in transitionMatrix[statesMapping[state]][alphabetMapping[letter]]])

        if len(newStates) > 1:
            if newStates not in newStatesMap.keys():
                stateName = "newState" + str(cnt)
                cnt += 1
                states.append(stateName)
                # print(stateName)
                statesMapping[stateName] = len(states) - 1
                revStatesMapping[len(states) - 1] = stateName
                # transitionMatrix[statesMapping[state]][alphabetMapping[letter]]=set()
                # transitionMatrix[statesMapping[state]][alphabetMapping[letter]].add(statesMapping[stateName])

                #####

                newStatesMap[newStates] = stateName
                revNewStatesMap[stateName] = newStates
                ###
            else:
                # states.append(list(newStates)[0])
                # stateName=newStatesMap[newStates]
                transitionMatrix[statesMapping[state]][alphabetMapping[letter]] = set(
                    [statesMapping[x] for x in newStates])
    #  elif len(newStates)==1:
    # states.append(list(newStates)[0])

# print(states)
newtransitionMatrix = [["-" for i in range(200 * alphabetSize)] for j in range(200 * statesSize)]

for state in states:
    for letter in alphabet:
        NFAstates = transitionMatrix[statesMapping[state]][alphabetMapping[letter]]
        if len(NFAstates) == 1:  # it's an original state
            newtransitionMatrix[statesMapping[state]][alphabetMapping[letter]] = revStatesMapping[list(NFAstates)[0]]
        # print(newtransitionMatrix[statesMapping[state]][alphabetMapping[letter]])
        elif len(NFAstates) > 1:
            newStates = frozenset([revStatesMapping[x] for x in NFAstates])
            newtransitionMatrix[statesMapping[state]][alphabetMapping[letter]] = newStatesMap[newStates]
            # print(newtransitionMatrix[statesMapping[state]][alphabetMapping[letter]])
        # print(NFAstates)
        # if len(NFAstates)>1:
        # transitionMatrix[statesMapping[state]][alphabetMapping[letter]]=newStatesMap[NFAstates]

Q = [initialState]
finalStates = [initialState]
while len(Q) > 0:
    fr = Q[0]
    # print(fr)
    Q = Q[1:]
    for letter in alphabet:
        state = newtransitionMatrix[statesMapping[fr]][alphabetMapping[letter]]
        if state == "-":
            continue

        if state not in finalStates:
            finalStates.append(state)
            Q.append(state)

states = finalStates

print("Sigma:", file=fout)
for letter in alphabet:
    print(letter, file=fout)
print("End", file=fout)

print("States:", file=fout)

# print(revNewStatesMap["newState0"])
# exit(0)
for state in states:
    print(state, end="", file=fout)
    if state not in revNewStatesMap.keys():
        if D[state][0]:
            print(", S", end="", file=fout)
        if D[state][1]:
            print(", F", end="", file=fout)
    else:
        isInitial, isFinal = 0, 0
        for initialState in revNewStatesMap[state]:
            isFinal |= D[initialState][1]

        if isFinal:
            print(", F", end="", file=fout)
    print("", file=fout)

print("End", file=fout)

for state in states:
    for letter in alphabet:
        print("{}, {}, {}".format(state, letter, newtransitionMatrix[statesMapping[state]][alphabetMapping[letter]]),
              file=fout)
fout.close()
