# Created by Caleb Owens
# last updated 2020/12/16
# matplotlib version 3.3.3
# numpy version 1.19.4

import random
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as colorKey
import numpy as np


# ----Global Variables. Altered throughout many functions-----
deathChance = 0.5        # default rate of 2 percent. high risk factor multiplies by 3 plus randomization
debugMode = 0           # activates debug mode, prints out MUCH more person information and variable statuses
defaultActive = 3       # the base level amount of encounters a person will have per day
# encounterZone = 5     # a halted feature, would've divided people up into smaller encounter zones
infectionChance = 0       # default rate of 100. the chance is calculated as 100/10000 --- in float terms 5%
#                           infectionGenRand holds variances of infectionChance.
initialInfected = 20    # the initial infected population
riskFactorPop = 20.0     # changeable variable risk as a percentage of total population
safePeoplePercent = 50  # amount of population percentage using safety precautions like going out less and masks
totalPeoplePop = 1000    # total population
totalDays = 30          # total amount of days run. there are multiple encounter per day
totalInfected = 0       # changed in createEncounter. adds the initial infected in main function
personList = []
currentInfectedPerDay = []
totalInfectedPerDay = []
totalDeathList = []


class Person:
    def __init__(self, riskFactor, condition, life, activeness, safety, infectChance, infectionTick, deathChance):
        self.riskFactor = riskFactor            # higher health risk. used to represent older population or sick
        self.condition = condition              # condition 0- uninfected / condition 1- infected / condition 2- immune
        self.life = life                        # status of being alive or dead. dead are removed and put into dead list
        self.activeness = activeness            # amount of encounters a person will do daily---affected by safety
        self.safety = safety                    # 0 = using safety  1 = not being safe  affects infectChance & activity
        self.infectChance = infectChance        # a semi randomized measure of infection chance
        self.infectionTick = infectionTick      # counts how long person is infected. 14 days will make a person immune
        self.deathChance = deathChance          # chance a person will die. affected by riskFactor

    # used to print out each person object's information
    def __str__(self):
        return "Person: \nRisk Factor: %s, " \
               "\nCondition: %s \nLife: %s \nActiveness: %s \nSafety: %s \nInfect Chance: %s " \
         "\nInfection Tick: %s \nDeath Chance: %s" \
         % (self.riskFactor, self.condition, self.life, self.activeness, self.safety,
            self.infectChance, self.infectionTick, self.deathChance)


# used to input user data and customizations
def userInputs():
    global debugMode
    global infectionChance
    global totalPeoplePop
    global safePeoplePercent
    global defaultActive
    # global encounterZone
    global riskFactorPop
    global deathChance
    global initialInfected
    global totalDays

    debugMode = \
        (input("\nif using debug mode enter '1', otherwise 'enter' ") or "0")
    totalPeoplePop = \
        int(input("Insert the total population for the simulation, default 1000") or "1000")
    totalDays = \
        int(input("Insert the total number of days the simulation will run, default is 30 days.") or "30")
    safePeoplePercent = \
        int(input("Insert a number between 0-100 for percent of people using safety precautions, default 50 ") or "50")
    if safePeoplePercent > 100 or safePeoplePercent < 0:
        sys.exit("The number of people using safety precautions cannot be less than 0 or more than 100")
    defaultActive = \
        int(input("Insert an average number of active encounters people will have per day. default is 3 ") or "3")
    # encounterZone = \
    #  int(input("insert a number for the total zones people will visit and travel around in ") or "5")
    riskFactorPop = \
        float(input("Insert a percent of population at higher risk of death. default 30 percent ") or 30.0)
    if riskFactorPop > 100 or riskFactorPop < 0:
        sys.exit("The population at high risk of death cannot be more than 100 or less than 0")
    deathChance = \
        float(input("Insert the percent chance of higher risk patients dying. default is 1 percent ") or 1.0)
    if deathChance >= 100 or deathChance <= 0:
        sys.exit("Death chance chance must be more than 0 and less than 100 percent death")
    initialInfected = \
        int(input("Insert the initial number of infected people. default is 20 people ") or "20")
    if initialInfected >= totalPeoplePop:
        sys.exit("Initial infected is equal or greater than the entire population ")


# runs all functions, passes variables, runs debug mode tests if applicable, and prints various final data
def main():
    global debugMode
    global infectionChance
    global totalPeoplePop
    global safePeoplePercent
    global defaultActive
    # global encounterZone
    global riskFactorPop
    global deathChance
    global initialInfected
    global personList
    global totalDays
    global totalInfected
    global totalDeathList

    userInputs()
    totalInfected += initialInfected
    safePeoplePop = (int(totalPeoplePop) * (int(safePeoplePercent) * 0.01))
    safePeoplePop = round(safePeoplePop)

    # unsafe and safe people are given a 0 health risk factor; riskFactor is added via createRiskFactor
    createSafePeople(personList, totalPeoplePop, safePeoplePop, 0, defaultActive, infectionChance)
    createUnsafePeople(personList, totalPeoplePop, safePeoplePop, 0, defaultActive, infectionChance)
    createRiskFactor(personList, totalPeoplePop, riskFactorPop)
    infectionDeathChanceGen(personList, deathChance)
    createInitialInfected(personList, initialInfected)
    simulateTime(personList, debugMode, totalDays, totalDeathList)
    print("\nTotal amount of people infected with COVID-19:", totalInfected)
    plotGraph(currentInfectedPerDay, totalInfectedPerDay, totalDays, totalDeathList)

    if debugMode == '1':
        print("\nTotal people population: ", totalPeoplePop)
        print("Safe people percent: ", safePeoplePercent)
        # print("Encounter zone amount: ", encounterZone)
        print("safe people population: ", safePeoplePop)
        print("risk factor population: ", riskFactorPop)
        print("death chance: ", deathChance)
        print("initial infected: ", initialInfected)

        infectTest = infectGenRand(infectionChance, 1)         # infectChance, safety
        print("infect test ", infectTest)
        activeGenTest = activenessGen(1, 1)                         # safety, activeness
        print("activeness generation test: ", activeGenTest)
        activeRandTest = activenessRandomization(1, activeGenTest)  # safety, activeness
        print("active random test ", activeRandTest)

        # print full person list. recommended to make population smaller
        for a in range(len(personList)):
            print("\n", personList[a])


# regular python shuffle does not allow shuffling portions of a list, without making copies. No copied lists
def shuffleZone(personList, i, stop):
    start = i
    while start < stop - 1:
        randNum = random.randrange(start, stop)
        personList[start], personList[randNum] = personList[randNum], personList[start]
        start += 1


# the main infection encounters. multiple encounters per day. Chance to infect adjacent people.
# the people still active and not 'atHome' are shuffled around each time in the createDay function
def createEncounter(personList, debugMode, atHomeTick):  #encounterZone
    global totalInfected

    # partitionList = []        # old code intended to be used for encounter zone feature that was never implemented
    # personListBegin = 0       # partitionList would hold beginning and ends of encounter Zones
    personListEnd = len(personList)
    maxInfectChance = 10000                          # lower = more chance of infect  larger = less chane of infection

    if debugMode == '1':
        print("\n at home tick: ", atHomeTick)
        print("personListEnd: ", personListEnd)

    for person in range(personListEnd - atHomeTick):        # only counts the population still active, not at Home
        if person == 0:                                     # used for beginning index where only right side can infect
            personInfect = getattr(personList[person], 'infectChance')
            if getattr(personList[person + 1], 'condition') == 1:   # if person to right is infected
                infect = random.randrange(1, maxInfectChance, 1)    # make a random infection number
                if getattr(personList[person], 'condition') != 2:   # if not immune
                    if debugMode == '1':
                        print('infection encounter occurred: ', person)
                    if infect <= personInfect:                      # if the random infect number <= person infect num
                        if getattr(personList[person], 'condition') == 0:
                            totalInfected += 1                             # new infected person
                        setattr(personList[person], 'condition', 1)

        elif person == (personListEnd - 1) - atHomeTick:        # used for last index where only left side can infect
            personInfect = getattr(personList[person], 'infectChance')
            if getattr(personList[person - 1], 'condition') == 1:
                infect = random.randrange(1, maxInfectChance, 1)
                if getattr(personList[person], 'condition') != 2:
                    if debugMode == '1':
                        print('infection encounter occurred: ', person)
                    if infect <= personInfect:
                        if getattr(personList[person], 'condition') == 0:
                            totalInfected += 1
                        setattr(personList[person], 'condition', 1)

        elif atHomeTick >= personListEnd:                  # all people are at home, end encounter
            break
        else:                                               # used for middle indexes where left and right can infect
            personInfect = getattr(personList[person], 'infectChance')
            if getattr(personList[person - 1], 'condition') == 1 or getattr(personList[person + 1], 'condition') == 1:
                infect = random.randrange(1, maxInfectChance, 1)
                if getattr(personList[person], 'condition') != 2:
                    if debugMode == '1':
                        print('infection encounter occurred: ', person)
                    if infect <= personInfect:
                        if getattr(personList[person], 'condition') == 0:
                            totalInfected += 1
                        setattr(personList[person], 'condition', 1)


# runs multiple encounters until all people are 'at home'
def createDay(personList, debugMode):
    global totalInfected
    global currentInfectedPerDay
    global totalInfectedPerDay

    atHomeTick = 0                  # count how many people are at home until everyone is
    activenessTick = 0              # do encounters until highest active people are done
    conditionTally = 0              # count how many are CURRENTLY infected

    while atHomeTick < len(personList) - 1:
        activenessTick += 1
        for person in range(len(personList) - atHomeTick):
            if getattr(personList[person], 'activeness') < activenessTick:
                personList.append(personList.pop(person))                   # pop to the end of personList
                atHomeTick += 1                                         # the end of personList represents those at home
        shuffleZone(personList, 0, (len(personList) - 1) - atHomeTick)      # shuffle active persons each encounter
        createEncounter(personList, debugMode, atHomeTick)

    for person in range(len(personList)):
        personInfectTick = getattr(personList[person], 'infectionTick')
        if getattr(personList[person], 'condition') == 1:
            setattr(personList[person], 'infectionTick', (personInfectTick + 1))    # increase person's infectTick
            conditionTally += 1                                                 # if infectTick hits 14, immune no death
    print("currently infected:", conditionTally)
    currentInfectedPerDay.append(conditionTally)
    totalInfectedPerDay.append(totalInfected)


# runs multiple days, inflicts death, creates immunity, holds total deaths, day count and a list of dead persons
def simulateTime(personList, debugMode, totalDays, totalDeathList):
    totalDeath = 0
    deadPerson = []
    dayCount = 0

    print("\ntotalDays: ", totalDays, "\n")
    for day in range(totalDays):                    # run for total amount of days
        person = 0
        currentDeath = 0
        personListSize = len(personList)

        while person < personListSize:
            personInfectTick = getattr(personList[person], 'infectionTick')
            if 0 < personInfectTick < 14:                               # 14 representing 2 week infection period
                personDeathChance = getattr(personList[person], 'deathChance')
                personDeath = random.uniform(0.00000, 100.00000)        # number between 0-100 with decimals
                if debugMode == 1:
                    print("\n person Death variable\n", personDeath)
                if personDeath <= personDeathChance:                    # if random death number is less than person's
                    totalDeath += 1
                    currentDeath += 1                            # person is now dead
                    setattr(personList[person], 'life', 'dead')
                    deadPerson.append(personList[person])
                    personList.remove(personList[person])
                    person -= 1                             # person is dead/removed from list, must re-run that spot
                    personListSize -= 1                     # lower the person list size, if someone dies

            elif getattr(personList[person], 'infectionTick') >= 14:    # apply immunity if person infected for 14 days
                setattr(personList[person], 'condition', 2)
            person += 1                                                 # the basic while increment
        totalDeathList.append(currentDeath)
        createDay(personList, debugMode)                            # create new day, which creates new encounters
        dayCount += 1
        print("Day: ", dayCount)

    print("\nTotal dead people: ", totalDeath)                         # print list of dead people
    for a in range(len(deadPerson)):
        print("\n", (a + 1), deadPerson[a])


# generate the population using safety precautions
def createSafePeople(personList, totalPeoplePop, safePeoplePop, riskFactor, defaultActive, infectChance):
    for person in range(int(safePeoplePop)):
        personList.append(Person(riskFactor, 0, "alive", activenessGen(0, defaultActive), 0,
                                 infectGenRand(infectChance, 0), 0, 0))


# generate the population not using safety precautions
def createUnsafePeople(personList, totalPeoplePop, safePeoplePop, riskFactor, defaultActive, infectChance):
    unsafePeoplePop = totalPeoplePop - safePeoplePop

    for person in range(int(unsafePeoplePop)):
        personList.append(Person(riskFactor, 0, "alive", activenessGen(1, defaultActive), 1,
                                 infectGenRand(infectChance, 1), 0, 0))

    random.shuffle(personList)          # unsafe people are appended all in one spot of personList, shuffle them up


# generate high risk factors in population
def createRiskFactor(personList, totalPeoplePop, riskFactorPop):
    riskFactorTick = 0
    totalRiskPop = totalPeoplePop * (riskFactorPop * 0.01)

    # print("\nrisk factor pop", totalRiskPop)
    for person in range(int(totalRiskPop)):
        setattr(personList[person], 'riskFactor', 1)
        riskFactorTick += 1
    random.shuffle(personList)       # all high risk factor people are at beginning of list, shuffle.


# infect a starting amount of the population at day 0
def createInitialInfected(personList, initialInfected):
    initialInfectedTick = 0

    for person in personList:
        person.condition = 1
        initialInfectedTick += 1
        if initialInfectedTick >= initialInfected:
            break
    random.shuffle(personList)   # all infected people are at beginning of list, shuffle.


# used in person generation to make activity levels. Affected by person safety. safety = 2 is not used
def activenessGen(safety, activeness):
    if safety == 0:
        personActiveness = activeness / 3
        personActiveness = activenessRandomization(safety, personActiveness)
        return personActiveness
    elif safety == 1:
        personActiveness = activeness
        personActiveness = activenessRandomization(safety, personActiveness)
        return personActiveness
    elif safety == 2:
        personActiveness = 0
        return personActiveness
    else:
        sys.exit("Error at ActivenessGen ")


# take generated activity levels and add randomization
def activenessRandomization(safety, activeness):
    if safety == 0:
        activenessRand = random.randrange(0, 20, 1)
        activenessRand = activenessRand / 10
        activeness += activenessRand
        return activeness
    elif safety == 1:
        activenessRand = random.randrange(5, 50, 1)
        activenessRand = activenessRand / 10
        activeness += activenessRand
        return activeness
    elif safety == 2:
        return activeness
    else:
        sys.exit("Error at ActivenessRandomization ")


# add difference gap between safe and non-safe persons infection rates
# add a level of variance to the infection rate
def infectGenRand(infectChance, safety):
    # change this to make fluctuations in infection rate vary greater or less
    if safety == 0:
        infectRand = random.randrange(100, 200, 1)    # rate of infect in safe users out of 10,000 max
        infectChance += infectRand                    # would represent 100/10,000    1% chance
        return infectChance
    elif safety == 1:
        infectRand = random.randrange(100, 300, 1)  # change the rate of infection variance for non-safety users
        infectChance += infectRand
        return infectChance
    elif safety == 2:                   # safety = 2 was never implemented in program's design
        return infectChance
    else:
        sys.exit("Error with infectGenRand")


# set deathChance based on assigned deathChance percent and risk factor of individual
def infectionDeathChanceGen(personList, deathChance):
    for person in range(len(personList)):

        if getattr(personList[person], 'riskFactor') == 0:
            setattr(personList[person], 'deathChance', ((deathChance / 4) / 14))
            # change to make low risk persons less/more likely to die
            # 14 representing a 2 week period the infection may kill
        elif getattr(personList[person], 'riskFactor') == 1:
            setattr(personList[person], 'deathChance', (deathChance / 14))
            # change to make high risk person less/more likely to die when infected
        else:
            sys.exit("Error at infectionDeathChanceGen")
    # 3rd risk factor removed. there are 2 categories, low and high--- no middle risk factor included

def plotGraph(currentInfectList, totalInfectList, days, death):

    currentInfectArray = np.array(currentInfectList)
    totalInfectArray = np.array(totalInfectList)
    deathArray = np.array(death)
    daysList = []
    greenLine = colorKey.Patch(color='green', label='Presently infected')
    redLine = colorKey.Patch(color='red', label='Death each day')
    blueLine = colorKey.Patch(color='blue', label='Total infected')

    for day in range(days):
        daysList.append(day)
    daysArray = np.array(daysList)

    plt.legend(handles=[greenLine, blueLine, redLine])
    plt.plot(daysArray, currentInfectArray, 'go-')
    plt.plot(daysArray, totalInfectArray, 'b*-')
    plt.plot(daysArray, deathArray, 'rx-')
    plt.axis([0, days, 0, (totalInfectArray[-1] + 10)])

    for a in range(len(deathArray)):
        if a % 5 == 0:
            plt.annotate(deathArray[a],
                         (a, deathArray[a]),
                         textcoords='offset points',
                         xytext=(0, 5),
                         ha='center')
    for b in range(len(currentInfectArray)):
        if b % 5 == 0:
            plt.annotate(currentInfectArray[b],
                         (b, currentInfectArray[b]),
                         textcoords='offset points',
                         xytext=(0, 10),
                         ha='center')
    for c in range(len(totalInfectArray)):
        if c % 5 == 0:
            plt.annotate(totalInfectArray[c],
                         (c, totalInfectArray[c]),
                         textcoords='offset points',
                         xytext=(0, 25),
                         ha='center')
    plt.xlabel('Days')
    plt.ylabel('Infections')
    plt.grid()
    plt.show()


main()


# old code originally intended to make a 3rd risk factor group
''' elif riskFactor == 2:
personDeathChance = ((deathChance * 3) / 14)
return personDeathChance
'''

# old code meant to for non-implemented Encounter Zone feature
# used to create partitions for zones while ignoring the people that are deemed at home and no longer in encounters
# this would belong in the createDay function, and passed to encounter. encounterZone partitions would remain
# constant for a full Day and have new partitions created on a new Day.
# people would shuffle within said zones for the day--- making infection sites grow faster within infected zones
'''for partition in range(encounterZone - 1):
    if atHomeTick < personListEnd - 1:
        partitionList.append(random.randrange(personListBegin, ((personListEnd - 1) - atHomeTick), 1))

print("Partition List\n", partitionList)
'''
# printing each individual person, as effects are being done to them
'''
for person in range(len(personList)):
    print("\n", personList[person])

print("\n after\n\n")
'''