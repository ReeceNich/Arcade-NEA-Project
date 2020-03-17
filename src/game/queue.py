class Queue:
    def __init__(self):
        self.queue = []
        self.front_pointer = -1
        self.rear_pointer = 0
    
    def en_queue(self, item):
        # adds new item to the front of the list.
        self.queue.insert(self.rear_pointer, item)
        self.front_pointer += 1

    def de_queue(self):
        # removes the end item and returns it.
        self.front_pointer -= 1
        return self.queue.pop(self.front_pointer + 1)
        
    def is_empty(self):
        # test to see if queue is empty.
        if self.front_pointer <= self.rear_pointer:
            return True
        else:
            return False
        

    def size(self):
        # test to see if queue is full 
        return self.front_pointer - self.rear_pointer + 1
        


if __name__ == "__main__":
    q = Queue()

    q.en_queue("First")
    q.en_queue("Second")
    q.en_queue("Third")

    for i in range(0, q.size()):
        print(q.de_queue())
    
