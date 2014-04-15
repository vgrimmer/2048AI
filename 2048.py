import random

# Simple 2048 
#  TODO - Create Board class, better print
#   Fix EvaluateBoard[] so that overall smoothness is used not just identical neighbors

# Globals
RowSize = 4;
GameBoardSize = 16
GameBoard = [64, 2, 2, 2, 8, 128, 16, 16, 4, 16, 32, 4, 2, 2, 2, 2]
CombinedFlags = range(GameBoardSize)
# Test boards used for predicting moves
TestBoard0 = range(GameBoardSize)
TestBoard1 = range(GameBoardSize)
TestBoard2 = range(GameBoardSize)
TestBoard3 = range(GameBoardSize)
    
    
def InitializeBoard(Board):
    for i in xrange(GameBoardSize):
        Board[i] = 0;
        CombinedFlags[i] = 0;
    Board[5] = 2;

         
def PrintBoard(Board):
    print Board
    for i in xrange(4):
        for j in xrange(4):
            print ("%04d, " % Board[i * RowSize + j]),
            
        print ""
    
# Directions
class Direction:
    UP    = 0
    RIGHT = 1
    DOWN  = 2
    LEFT  = 3

# Returns a zero if no move is possible!
def MakeMove(MMBoard, Move, Print):
    
    IsMovePossible = 0
    StartX = 0;
    StartY = 0;
    SourceIndex = 0;
    NextSpot = 0;
    NextRow = 4;
    
    if(Move == Direction.UP):
        NextSpot = RowSize;
        NextRow = 1;
    if(Move == Direction.RIGHT):
        StartX = 3;
        NextSpot = -1;
        NextRow = RowSize;
    if(Move == Direction.LEFT):
        NextSpot = 1;
        NextRow = RowSize;
    if(Move == Direction.DOWN):
        StartY = 3;
        NextSpot = -RowSize;
        NextRow = 1;

    # Track if a combination has happened or not
    for i in xrange(GameBoardSize):
        CombinedFlags[i] = 0;
        
    # Takes 3 times through to get everything
    for x in xrange(3):
        #Iterate through rows/columns
        for j in xrange(RowSize):
            # Iterate through 4 spaces in each row
            for i in xrange(1, RowSize):
                SourceIndex = (StartY*4 + StartX) + (j*NextRow) + i*NextSpot
                DestIndex = SourceIndex - NextSpot;
                #print("At %d looking at %d" % (SourceIndex, DestIndex))

                if((DestIndex >= 0) and (DestIndex < GameBoardSize) and (MMBoard[SourceIndex] != 0)):
                    if(MMBoard[DestIndex] == 0):
                        # Shift!
                        if(Print):
                            print("Shift %d from %d to %d" % (MMBoard[SourceIndex], SourceIndex, DestIndex));
                        IsMovePossible = 1
                        MMBoard[DestIndex] = MMBoard[SourceIndex]
                        MMBoard[SourceIndex] = 0
                
                    elif((MMBoard[DestIndex] == MMBoard[SourceIndex]) and (CombinedFlags[DestIndex] == 0) and CombinedFlags[SourceIndex] == 0): 
                        # Combine!
                        if(Print):
                            print("Combine from %d to %d" % (SourceIndex, DestIndex));
                        IsMovePossible = 1
                        MMBoard[DestIndex] *= 2
                        MMBoard[SourceIndex] = 0
                        CombinedFlags[DestIndex] = 1
     
    if(IsMovePossible):
        InsertNewValue(MMBoard);     
        
    return IsMovePossible
    
def GetEmptySpaces(Board):
    EmptySpaces = []
    
    # Get a list of empty spaces
    for x in xrange(GameBoardSize):
        if(Board[x] == 0):
            EmptySpaces.append(x);

    return EmptySpaces

# Give the board a score
def EvaluateBoard(Board):
        
    NewList = GetEmptySpaces(Board);
    NumEmtpySpots = len(NewList)    
    #return NumEmtpySpots
    
    NumSimilarNeighbors = 0;
    for i in xrange(4):
        for j in xrange(4):
            TestI = i+1
            if(TestI < 4):
                if(Board[i*4+j] == Board[TestI*4+j]) and (Board[i*4+j] != 0):
                    #print("Not Game Over %d %d and %d %d" % (i, j, TestI, j))
                    NumSimilarNeighbors += 1
            TestI = i-1
            if(TestI >= 0):
                if(Board[i*4+j] == Board[TestI*4+j]) and (Board[i*4+j] != 0):
                    #print("Not Game Over %d %d and %d %d" % (i, j, TestI, j))
                    NumSimilarNeighbors += 1     
            TestJ = j+1
            if(TestJ < 4):
                if(Board[i*4+j] == Board[i*4+TestJ]) and (Board[i*4+j] != 0):
                    #print("Not Game Over %d %d and %d %d" % (i, j, i, TestJ))
                    NumSimilarNeighbors += 1
            TestJ = j-1
            if(TestJ >= 0):
                if(Board[i*4+j] == Board[i*4+TestJ]) and (Board[i*4+j] != 0):
                    #print("Not Game Over %d %d and %d %d" % (i, j, i, TestJ))
                    NumSimilarNeighbors += 1  
                    
    return NumSimilarNeighbors + (NumEmtpySpots * 3)

# Insert a new 2 or 4 into a random spot
#  roughly 20% of the time should be a '4'
def InsertNewValue(Board):
    EmptySpaces = GetEmptySpaces(Board)
    if(len(EmptySpaces) == 0):
        return;
        
    Spot = random.randrange(0,len(EmptySpaces));
    if(random.randrange(0,10) < 2):
        Board[EmptySpaces[Spot]] = 4
    else:
        Board[EmptySpaces[Spot]] = 2
    
def IsGameOver(Board):
    
    # Any empty spots means not game over    
    for x in Board:
        if(x == 0):
            #print("Found a zero!")
            return 0
            
    # Any duplicate numbers side by side means
    #  not game over
    for i in xrange(4):
        for j in xrange(4):
            TestI = i+1
            if(TestI < 4):
                if(Board[i*4+j] == Board[TestI*4+j]):
                    #print("Not Game Over %d %d and %d %d" % (i, j, TestI, j))
                    return 0
            TestI = i-1
            if(TestI >= 0):
                if(Board[i*4+j] == Board[TestI*4+j]):
                    #print("Not Game Over %d %d and %d %d" % (i, j, TestI, j))
                    return 0      
            TestJ = j+1
            if(TestJ < 4):
                if(Board[i*4+j] == Board[i*4+TestJ]):
                    #print("Not Game Over %d %d and %d %d" % (i, j, i, TestJ))
                    return 0
            TestJ = j-1
            if(TestJ >= 0):
                if(Board[i*4+j] == Board[i*4+TestJ]):
                    #print("Not Game Over %d %d and %d %d" % (i, j, i, TestJ))
                    return 0    
 
    return 1
            

def IsWin(Board):
    for x in Board:
        if(x >= 2048):
            return 1;

    return 0;
            
def GetMove(Move):
    if(Move == Direction.UP):
        return "UP"
    elif(Move == Direction.RIGHT):
        return "RIGHT"
    elif(Move == Direction.DOWN):
        return "DOWN"
    elif(Move == Direction.LEFT):
        return "LEFT"
    else:
        return "UNKNOWN"
            
    
def PlayGame(Board, MaxMoves):
    
    PrintBoard(Board)
   
    TestBoards = []
    TestBoards.append(TestBoard0);
    TestBoards.append(TestBoard1);
    TestBoards.append(TestBoard2);
    TestBoards.append(TestBoard3);
       
   
    while((IsGameOver(Board) == 0) and (IsWin(Board) == 0) and (MaxMoves > 0)):

        MaxMoves -= 1
        
        # Test 4 Moves       
        Score = 0
        WinningMove = 0
        HighestScore = 0

        # Initialize test boards
        for x in xrange(GameBoardSize):
            #NewBoard = copy.deepcopy(Board)
            TestBoard0[x] = Board[x]
            TestBoard1[x] = Board[x]
            TestBoard2[x] = Board[x]
            TestBoard3[x] = Board[x]

        
        for x in xrange(4):
            IsMovePossible = MakeMove(TestBoards[x], x, 0)
            Score = EvaluateBoard(TestBoards[x])
            #print("New Board Scores:%d :" % Score)
            #PrintBoard(TestBoards[x])
            if(IsMovePossible) and (Score > HighestScore):
                HighestScore = Score
                WinningMove = x
                
        # Make Move
        print("Making move %s" % GetMove(WinningMove))
        MakeMove(Board, WinningMove, 0);
        PrintBoard(Board)
        
    print("Game Over IsGameOver=%d IsWin=%d MaxMoves=%d" % (IsGameOver(Board), IsWin(Board), MaxMoves))
    
    if(IsWin(Board)):
        print("You Win");
    else:
        print("You Lose!");
    
    

InitializeBoard(GameBoard);
PlayGame(GameBoard, 3000);


#TestBoard = [2, 8, 4, 4, 32, 0, 0, 0, 8, 0, 0, 0, 2, 0, 0, 0]
#PrintBoard(TestBoard)
#MakeMove(TestBoard, 3, 1)
#PrintBoard(TestBoard)