
import game as g
import copy as copy
import util 
wordChecker=g.Dictionary("dictionary.txt")
def GADDAGAdder(stringname,array):
    for i in range(1,len(stringname),1):
        array.append(stringname[0:i][::-1]+'+'+stringname[i:len(stringname)])
    array.append(stringname[::-1])
array=[]
GADDAGAdder("AARDVARK",array)
print(array)

wordCheckerReversed=g.Dictionary("revdictionary.txt")

#Row/Column Checker
# Flow:
# We start by putting a play container so that its extendable to the right.
# When the node is extendable to left,insert. Then check if node extendable to right, then extend. If node not extendable to right, then append to words, if the word is not extendable anymore.
def ExtendRight(Square,Board,hand,play,Direction,allsuffixes,hands,words,x,y,lefttrail):
     #insert contains all letters
    print("play="+play)
    if Square.get_letterTile()!=None and Direction=="Horizontal":
        if y<15:
            print("Down not empty")
            ExtendRight(Board[x][y+1],Board,hand,play+Board[x][y].get_letterTile().get_letter(),Direction,allsuffixes,hands,words,x,y+1,lefttrail)
        if wordCheckerReversed.dictionary.t.has_subtrie((play+Board[x][y].get_letterTile().get_letter())[::-1])==True and Board[x][y+1].get_letterTile()==None :
            allsuffixes.append((play+Board[x][y].get_letterTile().get_letter())[::-1])
            hands.append(copy.deepcopy(hand))
        return
    if Square.get_letterTile()!=None and Direction=="Vertical":
        if x<15:
            print("Right not empty")
            ExtendRight(Board[x+1][y],Board,hand,play+Board[x][y].get_letterTile().get_letter(),Direction,allsuffixes,hands,words,x+1,y,lefttrail)
        if wordCheckerReversed.dictionary.t.has_subtrie((play+Board[x][y].get_letterTile().get_letter())[::-1])==True and Board[x+1][y].get_letterTile()==None:
            allsuffixes.append((play+Board[x][y].get_letterTile().get_letter())[::-1])
            hands.append(copy.deepcopy(hand))
        return
    if (Square.get_letterTile()==None and not hand) :
        return 
    if Direction=="Horizontal" and y<15 and (Square.get_letterTile()==None and hand):  #If extendable from position
        for i in range(0,len(hand)):
            print(hand)
            print("i="+hand[i])
            if wordChecker.check_word(play+hand[i]) and Board[x][y+1].get_letterTile()==None:
                if lefttrail==None:
                    words.append(play+hand[i])
            if wordCheckerReversed.dictionary.t.has_subtrie((play+hand[i])[::-1])==True and Board[x][y+1].get_letterTile()==None and cross_check(hand[i],"Horizontal",Board,x,y):
                print("Check Reversed")
                temp=hand[i]
                hand.pop(i)
                allsuffixes.append((play+temp)[::-1])
                hands.append(copy.deepcopy(hand))
                hand.insert(i,temp)
            if (wordChecker.dictionary.t.has_subtrie(play+hand[i])==True or wordCheckerReversed.dictionary.t.has_subtrie((play+hand[i])[::-1])) and cross_check(hand[i],"Horizontal",Board,x,y):
                print("Extension entered")
                temp=hand[i]
                hand.pop(i)
                ExtendRight(Board[x][y+1],Board,hand,play+temp,Direction,allsuffixes,hands,words,x,y+1,lefttrail)
                hand.insert(i,temp)
                print("Appended")
    
    if Direction=="Vertical" and x<15 and (Square.get_letterTile()==None and hand):
        for i in range(0,len(hand)):
            if wordChecker.check_word(play+hand[i]) and (Board[x+1][y].get_letterTile()==None):
                if lefttrail==None:
                    words.append(play+hand[i])
            if wordCheckerReversed.dictionary.t.has_subtrie((play+hand[i])[::-1])==True and Board[x+1][y].get_letterTile()==None and cross_check(hand[i],"Vertical",Board,x,y):
                print("Check Reversed")
                temp=hand[i]
                hand.pop(i)
                allsuffixes.append((play+temp)[::-1])
                hands.append(copy.deepcopy(hand))
                hand.insert(i,temp)
            if (wordChecker.dictionary.t.has_subtrie(play+hand[i])==True or wordCheckerReversed.dictionary.t.has_subtrie((play+hand[i])[::-1])) and cross_check(hand[i],"Vertical",Board,x,y):
                print("Extension entered")
                temp=hand[i]
                hand.pop(i)
                ExtendRight(Board[x+1][y],Board,hand,play+temp,Direction,allsuffixes,hands,words,x+1,y,lefttrail)
                hand.insert(i,temp)
                print("Appended")

def ExtendLeft(Square,Board,hand,play,Direction,words,x,y):
    if Direction == "Vertical"  and Square.get_letterTile()!=None:
        if x>0:
            ExtendLeft(Board[x-1][y],Board,hand,play+Board[x][y].get_letterTile().get_letter(),"Vertical",words,x-1,y)
            print("Left Appended:"+play+Board[x][y].get_letterTile().get_letter())
        if wordCheckerReversed.check_word(play+Board[x][y].get_letterTile().get_letter()):
            words.append((play+Board[x][y].get_letterTile().get_letter())[::-1])
            print("Reversed True")
    if Direction == "Horizontal"  and Square.get_letterTile()!=None:
        if y>0:
            ExtendLeft(Board[x][y-1],Board,hand,play+Board[x][y].get_letterTile().get_letter(),"Horizontal",words,x,y-1)
        if wordCheckerReversed.check_word(play+Board[x][y].get_letterTile().get_letter()):
            words.append((play+Board[x][y].get_letterTile().get_letter())[::-1])
            print("Reversed True")
    for m in range(0,len(hand)):
        if Direction =="Vertical" and x>0 and Square.get_letterTile()==None and hand:
            if wordCheckerReversed.check_word(play+hand[m]) and Board[x-1][y].get_letterTile()==None and cross_check(hand[m],"Vertical",Board,x,y):
                words.append((play+hand[m])[::-1])
                print("Reversed True")
            if wordCheckerReversed.dictionary.t.has_subtrie(play+hand[m])==True and cross_check(hand[m],"Vertical",Board,x,y):
                temp=hand[m]
                hand.pop(m)
                ExtendLeft(Board[x-1][y],Board,hand,play+temp,Direction,words,x-1,y)
                hand.insert(m,temp)
                    
        if Direction=="Horizontal" and y>0 and Square.get_letterTile()==None and hand:
            print("left play="+play)
            print(hand)
            print("i="+hand[m])
            if wordCheckerReversed.check_word(play+hand[m]) and Board[x][y-1].get_letterTile==None and cross_check(hand[m],"Horizontal",Board,x,y):
                words.append((play+hand[m])[::-1])
                print("Reversed True")
            if wordCheckerReversed.dictionary.t.has_subtrie(play+hand[m])==True and cross_check(hand[m],"Horizontal",Board,x,y):
                temp=hand[m]
                hand.pop(m)
                ExtendLeft(Board[x][y-1],Board,hand,play+temp,Direction,words,x,y-1)
                hand.insert(m,temp)
                print("Appended")



def wordSearch(Square,Board,hand,play,Direction,allsuffixes,allhands,words,x,y):
    lefttrail=None
    if Direction=="Vertical" and Board[x-1][y].get_letterTile()!=None:
        lefttrail=1
    if Direction=="Horizontal" and Board[x][y-1].get_letterTile()!=None:
        lefttrail=1
    ExtendRight(Square,Board,hand,play,Direction,allsuffixes,allhands,words,x,y,lefttrail)
    if Direction=="Vertical" and x>0:
        for i in range(0,len(allsuffixes)):
            play=allsuffixes[i]
            hand=allhands[i]
            ExtendLeft(Board[x-1][y],Board,hand,play,Direction,words,x-1,y)
    if Direction=='Horizontal' and y>0:
        for i in range(0,len(allsuffixes)):
            play=allsuffixes[i]
            hand=allhands[i]
            ExtendLeft(Board[x][y-1],Board,hand,play,Direction,words,x,y-1)

def DictionaryGADDAG(filename):
    with open (filename,"r") as file:
        words=file.readlines()
    words=[word.rstrip() for word in words]
    file = open("revdictionary.txt","w")
    array=[]
    for k in words:
        GADDAGAdder(k,array)
    for i in array:
        file.write(i+"\n")
    file.close()


def cross_check(Letter,Direction,Board,x,y):
    pass
    word=Letter
    print("Test")
    if Direction=="Vertical":
        j=1
        while(y<15):
            if Board[x][y+j].get_letterTile()==None:
                 break
            else:
                 word=word+Board[x][y+j].get_letterTile().get_letter()
                 j=j+1
        j=1
        while(y>0):
            if Board[x][y-j].get_letterTile()==None:
                break
            else:
                word=Board[x][y-j].get_letterTile().get_letter()+word
                j=j+1
        if len(word)<=1:
            return True
        else:
            return wordChecker.check_word(word)
    if Direction=="Horizontal":
        j=1
        while(x<15):
            
            if Board[x+j][y].get_letterTile()==None:
                 break
            else:
                 word=word+Board[x+j][y].get_letterTile().get_letter()
                 j=j+1
        j=1
        while(x>0):
            if Board[x-j][y].get_letterTile()==None:
                break
            else:
                word=word+Board[x-j][y].get_letterTile().get_letter()
                j=j+1
        if len(word)<=1:
            return True
        else:
            return wordChecker.check_word(word)

abc=g.Board()
suffixlist=[]
words=[]
play=[]
hands=[]
DictionaryGADDAG("dictionary.txt")
#DictionaryReversal("dictionary.txt")
wordSearch(abc.board[0][0],abc.board,["A","B","A","B","A","L","E"],"","Horizontal",suffixlist,hands,words,3,3)
print(words)
print(""+"a")

print((wordChecker.dictionary.t.has_subtrie("AD")))

def BoardScanner(Board,hand):
    for i in range(0,16,1):
        for j in range(0,16,1):
            if Board[i][j+1].get_letterTile()!=None:
                suffixlist=[]
                hands=[]
                wordSearch(Board[i][j],Board,hand,"","Vertical",suffixlist,hands,words,i,j)
            if Board[i+1][j].get_letterTile()!=None:
                suffixlist=[]
                hands=[]
                wordSearch(Board[i][j],Board,hand,"","Horizontal",suffixlist,hands,words,i,j)



            





