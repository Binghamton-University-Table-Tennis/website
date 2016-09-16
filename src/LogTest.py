import math

# Actual table tennis rating system: http://www.teamusa.org/usa-table-tennis/ratings/how-does-the-usatt-rating-system-work

#first paramater is always who won. we calculate the gap based of their difference after the fact
def logRating(winRating, loseRating):
    gap = winRating - loseRating
    oldWinRating = winRating
    #handle expected match turnouts
    if gap >= 0:
        if gap <= 12:
            winRating += 8
            loseRating -= 8
        elif gap > 12 and gap <= 37:
            winRating += 7
            loseRating -= 7
        elif gap > 37 and gap <= 62:
            winRating += 6
            loseRating -= 6
        elif gap > 62 and gap <= 87:
            winRating += 5
            loseRating -= 5
        elif gap > 87 and gap <= 112:
            winRating += 4
            loseRating -= 4
        elif gap > 112 and gap <= 137:
            winRating += 3
            loseRating -= 3
        elif gap > 137 and gap <= 187:
            winRating += 2
            loseRating -= 2
        elif gap > 187 and gap <= 237:
            winRating += 1
            loseRating -= 1
        else:
            winRating += 0
            loseRating += 0
    #handle the upsets         
    else:
        gap = -1*gap;
        if gap <= 12:
            winRating += 8
            loseRating -= 8
        elif gap > 12 and gap <= 37:
            winRating += 10
            loseRating -= 10
        elif gap > 37 and gap <= 62:
            winRating += 13
            loseRating -= 13
        elif gap > 62 and gap <= 87:
            winRating += 16
            loseRating -= 16
        elif gap > 87 and gap <= 112:
            winRating += 20
            loseRating -= 20
        elif gap > 112 and gap <= 137:
            winRating += 25
            loseRating -= 25
        elif gap > 137 and gap <= 162:
            winRating += 30
            loseRating -= 30
        elif gap > 162 and gap <= 187:
            winRating += 35
            loseRating -= 35
        elif gap > 187 and gap <= 212:
            winRating += 40
            loseRating -= 40
        elif gap > 212 and gap <= 237:
            winRating += 45
            loseRating -= 45
        else:
            winRating += 50
            loseRating -= 50
        
        
        
    return winRating, loseRating, abs(winRating - oldWinRating)
    
    
def unitTest1(): # win vs same rating
    personA = 1000
    personB = 1000
    for i in range(100):
        temp1, temp2 = personA, personA
        personA, personB = logRating(personA,personA)
        print temp1, temp2, personA, personB, personA-temp1, personB-temp2, personA-personB
        

# Main------------------------------------------
def unitTest2(): # A wins all against same player
    personA = 1000
    personB = 1000
    for i in range(100):
        temp1 = personA
        temp2 = personB
        personA, personB = logRating(personA, personB)
        print personA, personB, personA-temp1, personB-temp2, personA-personB
        

# Main------------------------------------------
def unitTest3(): # A wins all against same player
    personA = 500
    personB = 1500
    for i in range(100):
        temp1 = personA
        temp2 = personB
        personA, personB = logRating(personA, personB)
        print personA, personB, personA-temp1, personB-temp2, personA-personB
    
#unitTest3()

    
