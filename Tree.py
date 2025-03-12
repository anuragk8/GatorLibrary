import copy
from Gator_Library import Book
import sys
class Tree():

    @staticmethod
    def SearchBook(self, book_id):
        node = self.root
        result = None
        while node != None:
            if node.book_id == book_id:
                result = node
            if node.book_id <= book_id:
                node = node.right
            else:
                node = node.left
        return result
    @staticmethod
    def printReservations(self, book_id):
        result = self.SearchBook(book_id)
        reservations = []
        if result != None:
            heap_change = copy.deepcopy(result.reservation_heap)
            for node in heap_change:
                print(node.patronID, node.timeofReservation, end =" ")
            print()
            for i in range(len(heap_change)):
                if heap_change == None:
                    reservations.append(None)
                    break
                else:
                    reservations.append(heap_change[0].patronID)
                    heap_change[0] = heap_change[-1]
                    heap_change.pop()
                    i = 0
                    while True:
                        left = (2 * (i + 1)) - 1
                        right = (2 * (i + 1))
                        least = 0
                        if right < len(heap_change) and \
                                heap_change[right].priority <= heap_change[least].priority:
                            if heap_change[right].priority == \
                                    heap_change[least].priority and i > 0:
                                if heap_change[right].timeofReservation < \
                                        heap_change[least].timeofReservation and i > 0:
                                    least = right
                            else:
                                least = right
                        if left < len(heap_change) and \
                                heap_change[left].priority < heap_change[least].priority:
                            if heap_change[left].priority == \
                                    heap_change[least].priority and i > 0:
                                if heap_change[left].timeofReservation < \
                                        heap_change[least].timeofReservation and i > 0:
                                    least = left
                            else:
                                least = left

                        if least != i:
                            heap_change[i], heap_change[least] = \
                                heap_change[least], heap_change[i]
                        else:
                            break
        else:
            reservations = []
        return reservations
    @staticmethod
    def PrintBook(self, file, book_id):
        result = self.SearchBook(book_id)
        reservations = self.printReservations(book_id)
        if result != None:
            file.write('\n')
            file.write(f"BookID = {result.book_id}\n")
            file.write(f"Title =  {result.book_name}\n")
            file.write(f"Author =  {result.author}\n")
            file.write(f"Availability =  {result.availability}\n")
            file.write(f"BorrowedBy = {result.borrower_id}\n")
            file.write(f"Reservations = {reservations}\n")
            file.write('\n')
    @staticmethod
    def PrintBooks(self,file, bookID1, bookID2):
        books = []
        books = self.preOrder(self.root, books)
        ids = []

        for i in range(len(books)):
            if books[i] < bookID2:
                if books[i] > bookID1:
                    ids.append(books[i])
        ids.sort()
        for id in ids:
            self.PrintBook(file, id)
            file.write('\n')
    @staticmethod
    def FindClosestBook(self,file, targetID):
        books = []
        books = self.preOrder(self.root, books)
        final_diff = sys.maxint
        arr = []
        for i in range(len(books)):
            diff = abs(books[i] - targetID)
            if diff < final_diff:
                final_diff = diff
                result = i
                arr.clear()
                arr.append(i)
            elif diff == final_diff:
                arr.append(i)
            arr.sort()
        for i in arr:
            self.PrintBook(file, books[i])
