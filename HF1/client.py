import sys
import json

jsonName = sys.argv[-1]
with open(jsonName, "r") as read_file:
    data = json.load(read_file)
    # print(data["simulation"]["demands"][0])


def searchCapacity(start, end):
    for link in data["links"]:
        if link["points"][0] == start and link["points"][1] == end:
            return link["capacity"]


def searchCircuit(start, end, capacity):
    possibleCircuits = []
    for circuit in data["possible-circuits"]:
        if circuit[0] == start and circuit[-1] == end:
            enoughCapacity = True
            for i in range(len(circuit) - 1):
                if searchCapacity(circuit[i], circuit[i + 1]) < capacity:
                    enoughCapacity = False
            if (enoughCapacity):
                possibleCircuits.append(circuit)
    return possibleCircuits


def checkForLink(point):
    possibleWays = []
    for link in data["links"]:
        if link["points"][0] == point:
            possibleWays.append(checkForLink(link["points"][1]))
        elif link["points"][1] == point:
            possibleWays.append(checkForLink(link["points"][0]))
    return possibleWays


busyCircuits = []
onGoingDemands = []
demandCount = 1

for i in range(data["simulation"]["duration"]):

    # check for starting demand
    for demand in data["simulation"]["demands"]:
        if demand["start-time"] == i + 1:
            printString = str(demandCount) + ". igény"
            circuits = searchCircuit(demand["end-points"][0], demand["end-points"][1], demand["demand"])
            if len(circuits) > 0:
                printString += " foglalás: " + demand["end-points"][0] + "<->" + demand["end-points"][
                    1] + " st:" + str(
                    i + 1)
                #print("\nLefoglalas elott")
                #print("found circ:", circuits)
                #print("busy circ:", busyCircuits)

                foundUnusedCircuit = False
                foundUsedLink = False

                for t in circuits:
                    for p in range(len(t) - 1):
                        pair = [t[p], t[p + 1]]

                        for c in busyCircuits:
                            #print(pair, c, pair in c)
                            s = set(x in c for x in pair)
                            #print(list(s)[0])
                            if len(s) == 1 and list(s)[0]:
                                foundUsedLink = True
                                break

                for t in circuits:
                    if t not in busyCircuits:
                        #print("Ez a jo:", t)
                        foundUnusedCircuit = True
                        break

                if not (not foundUnusedCircuit or foundUsedLink):
                    printString += " - sikeres"
                    busyCircuits.append(t)
                    onGoingDemands.append(demand)
                else:
                    printString += " - sikertelen"

            #print(onGoingDemands)
            print(printString)
            demandCount += 1

    # check for ending demand
    for demand in data["simulation"]["demands"]:
        if demand["end-time"] == i + 1 and demand in onGoingDemands:
            printString = str(demandCount) + ". igény"

            onGoingDemands.remove(demand)
            busyCircuits.pop(0)

            printString += " felszabadítás: " + demand["end-points"][0] + "<->" + demand["end-points"][
                1] + " st: " + str(
                i + 1)
            #print("\n felszabb elott")
            #print("found circ:", circuits)
            #print("busy circ:", busyCircuits)
            print(printString)
            demandCount += 1
    # print(onGoingDemands)
    # print(printString)
