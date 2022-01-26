class Stack:
    #Just a typical Stack module. This is needed for map creation so the user can have an 'undo' option.
    def __init__(self, maxSize):
        self.top = -1#points to top of stack
        self.contents = []

        for i in range(maxSize):#initialise with placeholders
            self.contents.append(0)
        self.maxSize = maxSize

    def push(self, item):
        if self.isFull():

            temp = self.contents
            for i in range(len(self.contents) - 1):
                self.contents[i] = temp[i + 1]

                self.contents[self.top] = item
        else:
            self.top += 1
            self.contents[self.top] = item

    def pop(self):
        if self.isEmpty():
            pass
        else:
            item = self.contents[self.top]
            self.top -= 1
            return item

    def isEmpty(self):
        if self.top == -1:
            return True
        else:
            return False

    def isFull(self):
        if self.top == self.maxSize - 1:
            return True
        else:
            return False