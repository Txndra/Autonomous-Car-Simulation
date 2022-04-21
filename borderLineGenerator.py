class BorderLineGenerator:
    def __init__(self, tracks, rows, columns, trackSize):
        self.horLines = []
        self.verLines = []
        self.tracks = tracks
        self.rows = rows
        self.columns = columns
        self.trackSize = trackSize

    def generate(self):
        self.calculateNeighbours()
        self.calculateBorderLines()
        self.condense()
        return (self.horLines, self.verLines)

    def calculateNeighbours(self):

        for t in self.tracks:

            if ((t.tileID + 1) % self.columns != 0 ) and self.findTrack(t.tileID + 1):
                t.east = True
            if (t.tileID % self.columns !=0) and self.findTrack(t.tileID - 1):
                t.west = True
            if (t.tileID > (self.columns - 1)) and self.findTrack(t.tileID - self.columns):
                t.north = True
            if (t.tileID < (self.columns * (self.rows-1))) and self.findTrack(t.tileID + self.columns):
                t.south = True
        
    def calculateBorderLines(self):
        for t in self.tracks:
            if not t.north:
                self.horLines.append((t.x, t.x + self.trackSize, t.y))
            if not t.south:
                self.horLines.append((t.x, t.x + self.trackSize, t.y + self.trackSize))
            if not t.west:
                self.verLines.append((t.y, t.y + self.trackSize, t.x))
            if not t.east:
                self.verLines.append((t.y, t.y + self.trackSize, t.x + self.trackSize))

    def condense(self):
        self.mergeSort(self.verLines, 2)
        self.mergeSort(self.horLines, 2)
        self.verLines = self.groupAndSort(self.verLines)
        self.horLines = self.groupAndSort(self.horLines)

        self.verLines = self.adjoin(self.verLines)
        self.horLines = self.adjoin(self.horLines)

    def findTrack(self, ID):
        #Simple binary search
        found = False
        index = -1
        first = 0
        last = len(self.tracks) - 1
        while first <= last and not found:
            midpoint = (first + last)//2
            if self.tracks[midpoint].tileID == ID:
                found = True
                index = midpoint
            else:
                if self.tracks[midpoint].tileID < ID:
                    first = midpoint + 1
                else:
                    last = midpoint -1
        return found

    def mergeSort(self, mergelist, x): #recursive mergeSort algorithm
        if len(mergelist) > 1:
            mid = len(mergelist)//2
            lefthalf = mergelist[:mid]
            righthalf = mergelist[mid:]
            self.mergeSort(lefthalf, x)
            self.mergeSort(righthalf, x)
            i = 0
            j = 0
            k = 0

            while i < len(lefthalf) and j < len(righthalf):
                if lefthalf[i][x] < righthalf[j][x]:
                    mergelist[k] = lefthalf[i]
                    i += 1
                else:
                    mergelist[k] = righthalf[j]
                    j += 1
                k +=1

            while i < len(lefthalf):
                mergelist[k] = lefthalf[i]
                i += 1
                k += 1

            while j < len(righthalf):
                mergelist[k] = righthalf[j]
                j += 1
                k += 1

    def groupAndSort(self, anArray):
        #turns 1D array onto 2d array of grouped tuples sorted
        groupedLines = []
        groupedLine = []
        currentLast = anArray[0][-1]
        for i in anArray:
            if i[-1] != currentLast:
                self.mergeSort(groupedLine, 0)
                groupedLines.append(groupedLine)
                groupedLine = [i]
                currentLast = i[-1]
            else:
                groupedLine.append[i]
        self.mergeSort(groupedLine, 0)
        groupedLines.append(groupedLine)
        groupedLine = [i]

        return groupedLines

    def adjoin(self, sortedGroups): #Joins up adjacent lines
        adjoinedLines = []
        for group in sortedGroups:

            if len(group) == 1:
                adjoinedLines.append((group[0][0], group[0][1], group[0][2]))
            else:
                start = group[0][0]
                end = group[0][1]
                constant = group[0][2]
                for line in group[1:]:
                    if line == group[-1] and line[0] == end:
                        adjoinedLines.append((start, line[1], constant))
                    elif line[0] == end:
                        end = line[1]
                    else:
                        adjoinedLines.append((start, end, constant))
                        start = line[0]
                        end = line[1]
                    if line == group[-1]:
                            adjoinedLines.append((line[0], line[1], constant))

        return adjoinedLines
            
