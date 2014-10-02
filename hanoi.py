fileStr="""\
--{ RES }--
V;200
--{ CFG }--
999;207;32;
14;-1;30;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;12;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;
998;0;
998;3;Cleaner shallow, 8 Pos.;Waste;Cleaner deep, 8 Pos.;
998;;;;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;3;384 Well, landscape;;;
998;cs1;;;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
998;0;
--{ RPG }--
Vector("HOME1","1","1",0,0,2,2,0,0);
"""

diskCount = 7
pegCount = 3

#initialize everything
state = []

for peg in xrange(0,pegCount):
	state.append([])

for disk in xrange(0,diskCount):
	state[0].append(disk)

def topNum(col):
	c = state[col]
	if len(c)==0:
		return -1

	return c[-1]

def printState():
	
	result="\n";
	for disk in xrange(diskCount-1,-1,-1):
		for peg in xrange(0,pegCount):
			if disk<len(state[peg]):
				result = result + str(state[peg][disk])
			else:
				result = result + "."
		result = result +"\n"
	print result

def doMove(a,b):
	pFrom = [a,len(state[a])-1]
	pTo = [b,len(state[b])]
	print ("move from ("+str(pFrom[0])+","+str(pFrom[1])+") to ("+str(pTo[0])+","+str(pTo[1])+").")
	state[b].append(state[a].pop())
	printState()
	pickPlateAt(pFrom[0],pFrom[1])
	dropPlateAt(pTo[0],pTo[1])

def doAction(colA,colB):
	nA=topNum(colA)
	nB=topNum(colB)
	if (nA==-1) and (nB==-1):
		return
	if (nA>nB):
		doMove(colA,colB)
	else:
		doMove(colB,colA)

def solved():
	for colN in xrange(1,pegCount):
		if len(state[colN])==diskCount:
			return True	
	return False

homePos=[1016.5,0,0]
curPos=homePos[:]

plateBasePositions = [
	[638.9,91.2,136.3],
	[638.9,190.3,136.3],
	[638.9,289.5,136.3]
]

heightOffset = 12.5

#go to home
#Vector("HOME1","1","1",0,0,2,2,0,0);
#move to X,Y,Z
#ROMA(3,80,75,X,Y,Z,150,1,0);
#open gripper to X
#ROMA(0,X,75,4,5,6,150,1,0);
#close gripper to X
#ROMA(1,X,12,4,5,6,150,1,0);

def pickPlateAt(x,y):
	pos = plateCoord(x,y)
	print "pos = " + str(pos)
	cmdMoveAbove(pos)
	cmdMoveTo(pos)
	pickPlate()
	cmdMoveAbove(pos)

def dropPlateAt(x,y):
	pos = plateCoord(x,y)
	cmdMoveAbove(pos)
	cmdMoveTo(pos)
	dropPlate()
	cmdMoveAbove(pos)

def pickPlate():
	global fileStr
	pickVal = 78
	fileStr=fileStr+"ROMA(1,"+str(pickVal)+",125,4,5,6,150,1,0);\n"

def dropPlate():
	global fileStr
	pickVal = 86
	fileStr=fileStr+"ROMA(0,"+str(pickVal)+",75,4,5,6,150,1,0);\n"

def plateCoord(x,y):
	basePos = plateBasePositions[x][:]
	basePos[2]=basePos[2]-heightOffset*y;
	return basePos

def cmdMoveTo(newPos):
	global curPos, fileStr
	diff =[ newPos[0]-curPos[0], newPos[1]-curPos[1],newPos[2]-curPos[2]]
	print str(curPos)+" + " +str(diff) +" = "+str(newPos)
	curPos=newPos[:]
	fileStr = fileStr+"ROMA(3,80,75,"+str(-diff[1])+","+str(-diff[0])+","+str(diff[2])+",150,1,0);\n"


def cmdMoveAbove(newPos):
	newPos = newPos[:]
	newPos[2]=plateBasePositions[0][2]-heightOffset*(3+diskCount)
	cmdMoveTo(newPos)



#move to z=0
def cmdMoveUp():
	fileStr = fileStr+"ROMA(3,80,75,0,0,"++str(-curPos[2])+",150,1,0);\n"
	curPos[2]=0

#open the hand at the start of each file
dropPlate()


printState()

#algorithm

if diskCount%2==0:
	while True:
		doAction(0,1)
		if solved():
			break;
		doAction(0,2)
		if solved():
			break;
		doAction(1,2)
		if solved():
			break;
else:	
	while True:
		doAction(0,2)
		if solved():
			break;
		doAction(0,1)
		if solved():
			break;
		doAction(2,1)
		if solved():
			break;


text_file = open("hanoi.gem", "w")
fileStr=fileStr.replace('\n','\r\n')
text_file.write(fileStr)
text_file.close()
