#Coordinate Toolkit used to navigate cars
#Uses a range of mathematical calculations including calculating gradients, equations of lines, points of intersections between lines
class CT:
    def calcGradient(start, end): #Uses start and end of line (both Cartestian) as parameters to calculate gradient
        if start[0] == end[0]: #if line is vertical (x's are same) it will not have gradient (as it's infinity)
            return None 
        else:
            m = (end[1] - start[1])/(end[0] - start[0]) #(y2-y1)/(x2-x1) to calculate the gradiant 'm'
            return m #returns m as the gradient

    def calcYintercept(point, m): #uses a point on the line to calculate the y intercept
        return point[1] - (point[0] * m) #rearraged y-y1=m(x-x1) formula

    def getIntersect(s1,e1,s2,e2):
        m1 = CT.calcGradient((s1),(e1)) #gets gradient for first line
        m2 = CT.calcGradient((s2),(e2)) #gets gradient for second line

        if m1 != m2: #if not parallel
            if m1 is not None and m2 is not None:#if neither are vertical
                c1 = CT.calcYintercept(s1, m1) #calculates y intercept of both lines
                c2 = CT.calcYintercept(s2, m2)
                
                
                x = (c2 - c1) / (m1 - m2) #get x point of intersection
                
                y = (m1 * x) + c1 #for y plug in x into either
            elif m2 is None:#if line 2 vertical (but not line 1)
                c1 = CT.calcYintercept(s1, m1)
                x = s2[0]#line 1 cuts 2 at 2's x which is contstant as it's vertical line
                #plug in for y
                y = (m1 * x) + c1
            elif m1 is None:#if line 1 vertical
                c2 = CT.calcYintercept(s2, m2)
                x = s1[0]
                y = (m2 * x) + c2
        else: #if parallel they don't intersect
            return None
        return ((x,y))#
    
    def getIntersectBetweenLineSegments(line1, line2):
        ver = False
        hor = False
        if line2[0][0] == line2[1][0]: 
            ver = True
        elif line2[0][1] == line2[1][1]:
            hor = True

        intersect = CT.getIntersect(line1[0], line1[1], line2[0], line2[1])
        if intersect is not None:
            if hor == True:
                if intersect[0] >= line2[0][0]and intersect[0] <= line2[1][0]:
                    if (line1[0][1] <= intersect[1] and intersect[1] <= line1[1][1]) or (line1[1][1] <= intersect[1] and intersect[1] <= line1[0][1]):
                        return intersect
            elif ver == True:
                if intersect[1] >= line2[0][1] and intersect[1] <= line2[1][1]:
                    if (line1[0][0] <= intersect[0] and intersect[0] <= line1[1][0]) or (line1[1][0] <= intersect[0] and intersect[0] <= line1[0][0]):
                        return intersect
            else:
                print('line2 must be a horizontal or vertical line, make sure it was passed in correctly')
        return None
        
