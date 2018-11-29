import sys;
class Field:
    def __init__(self,x,y,typeoffield):
        self.x = int(x)
        self.y = int(y)
        self.typeoffield = typeoffield
class MapSize:
    def __init__(self,Map_Split):
        self.Columns = int(Map_Split[0]);
        self.Rows = int(Map_Split[1]);

def GetGamma():
    while True:
        input = float(sys.stdin.readline());
        if isinstance(input, float):
            if input >= 0.0 and input <= 1.0:
                break;
        print("Źle wskazana gamma");
    return input;
def GetMap():
    F = open("Map.txt", "r");
    Map = F.readlines();
    return Map
def GetMapSizeSplit(Map):
    Map_Split = Map[0].split();
    return Map_Split
def GetFields(Map,MapSize,caret):
    Fields = list();
    for x in range(0, MapSize.Rows):
        for y in range(0, MapSize.Columns):
            row = Map[caret + x].split();
            Fields.append(Field(y, x, row[y]));
    return Fields;
def SetPotentialAndRewards(Fields,Map,MapSize,caret):
    for x in range(MapSize.Rows):
        for y in range(MapSize.Columns):
            row = Map[caret + x].split();
            Fields[y + x * MapSize.Columns].potential = float(row[y]);
            Fields[y + x * MapSize.Columns].reward = float(row[y]);
def MDP_Bellman(Fields,MapSize,gamma):
    for i in range(1000):
        isdone = False;
        for x in Fields:
            if (x.typeoffield == "1"):
                ChoiceRewards = GetListOfRewards(Fields, x, MapSize);
                biggestChoiceReward = max(ChoiceRewards);
                x.DirectionChoice = GetDirection(biggestChoiceReward, ChoiceRewards);
                oldpotential = x.potential;
                x.potential = x.reward + float(gamma) * float(biggestChoiceReward);
                if(abs(oldpotential - x.potential)<0.0001):
                    isdone = True;
                    break;
            if(isdone):
                break;
def PickField(Fields,xa,ya):
    for x in Fields:
        if(x.x == xa and x.y == ya):
            return x;
def GetFieldLeft(fields,field):
    if (field.x == 0):
        return field;
    else:
        x = PickField(fields, field.x - 1, field.y);
        if (x.typeoffield == "0"):
            return field;
        else:
            return x;
def GetFieldRight(fields,field,columns):
    if (field.x == columns-1):
        return field;
    else:
        x = PickField(fields, field.x + 1, field.y);
        if (x.typeoffield == "0"):
            return field;
        else:
            return x;
def GetFieldUp(fields,field):
    if (field.y == 0):
        return field;
    else:
        x = PickField(fields, field.x, field.y - 1);
        if (x.typeoffield == "0"):
            return field;
        else:
            return x;
def GetFieldDown(fields,field,rows):
    if (field.y == rows-1):
        return field;
    else:
        x = PickField(fields, field.x, field.y + 1);
        if (x.typeoffield == "0"):
            return field;
        else:
            return x;
def GetReward(mainfield,secondaryfieldone,secondaryfieldtwo):
    return float((0.8 * float(mainfield.potential)) + (0.1 * float(secondaryfieldone.potential)) + (
                0.1 * float(secondaryfieldtwo.potential)));
def GetListOfRewards(fields,field,mapsize):
    fieldUp = GetFieldUp(fields,field);
    fieldLeft = GetFieldLeft(fields,field);
    fieldRight = GetFieldRight(fields,field,mapsize.Columns);
    fieldDown = GetFieldDown(fields,field,mapsize.Rows);
    ChoiceRewards = list();
    ChoiceRewards.append(GetReward(fieldUp,fieldLeft,fieldRight))  # go up
    ChoiceRewards.append(GetReward(fieldRight,fieldUp,fieldDown))  # go right
    ChoiceRewards.append(GetReward(fieldDown,fieldLeft,fieldRight))  # go down
    ChoiceRewards.append(GetReward(fieldLeft,fieldUp,fieldDown))  # go left
    return ChoiceRewards;
def GetDirection(bestreward,rewards):
    for y in range(4):
        if (bestreward == rewards[y]):
            return y+1;
def MapaPotencjalow(Fields):
    mapa = "";
    for i in range(4):
        for x in Fields:
            if x.y == i:
                mapa += str(x.potential) + " ";
        mapa += "\n"
    return mapa;
def MapaKierunkow(Fields):
    mapa = ""
    for i in range(4):
        for x in Fields:
            if x.y == i:
                if x.typeoffield != "1":
                    x.DirectionChoice = "0"
                mapa += " " + str(x.DirectionChoice);
        mapa += "\n"
    return mapa;

gamma = GetGamma()
Map = GetMap()
Map_Split = GetMapSizeSplit(Map)
caret = 1;
MapSize = MapSize(Map_Split);

Fields = GetFields(Map,MapSize,caret);
caret+=MapSize.Rows+1;

SetPotentialAndRewards(Fields,Map,MapSize,caret);

MDP_Bellman(Fields,MapSize,gamma);

print("Mapa potencjałów: ")
print(MapaPotencjalow(Fields))
print("Mapa kierunków: ")
print(MapaKierunkow(Fields))











