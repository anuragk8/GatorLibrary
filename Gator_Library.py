import sys
import time
import copy
import re

class Book():
    def __init__(self, book_id):
        self.book_id = book_id
        self.book_name = None
        self.author = None
        self.availability = None
        self.borrower_id = None
        self.borrower_priority = None
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1
        self.color_flips = 0
        self.reservation_heap = []


class Heap_Node():
    def __init__(self, priority):
        self.priority = priority
        self.patronID = None
        self.timeofReservation = None


class Tree():
    def __init__(self):
        self.null_node = Book(0)
        self.null_node.color = 0
        self.null_node.left = None
        self.null_node.right = None
        self.root = self.null_node

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

    def printReservations(self, book_id):
        result = self.SearchBook(book_id)
        reservations = []
        if result != None:
            heap_change = copy.deepcopy(result.reservation_heap)
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


    def ColorFlipCount(self, file):
        books1 = []
        books1 = self.preOrder2(self.root, books1)
        sum = 0
        for i in range(len(books1)):
            sum += books1[i].color_flips
        file.write(f"Color Flips: {sum}\n")


    def preOrder(self, node, books):
        if node != None:
            books.append(node.book_id)
            self.preOrder(node.left, books)
            self.preOrder(node.right, books)
        return books

    def preOrder2(self, node, books):
        if node != None:
            books.append(node)
            self.preOrder2(node.left, books)
            self.preOrder2(node.right, books)
        return books

    def FindClosestBook(self,file, targetID):
        books = []
        books = self.preOrder(self.root, books)
        final_diff = 999
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


    def BorrowBook(self, file, patronID, book_id, patronPriority):
        time.sleep(0.0001)
        req_book = self.SearchBook(book_id)
        res_time = time.time()
        if req_book.availability == "Yes":
            req_book.availability = "No"
            req_book.borrower_id = patronID
            file.write(f"Book {req_book.book_id} borrowed by Patron {req_book.borrower_id}\n\n")
        else:
            # creating a min heap when the book is not available for borrowing
            file.write(f"Book {req_book.book_id} Reserved by Patron {patronID}\n\n")
            heap_node = Heap_Node(patronPriority)
            heap_node.patronID = patronID
            heap_node.timeofReservation = res_time
            req_book.reservation_heap.append(heap_node)
            i = len(req_book.reservation_heap) - 1
            while req_book.reservation_heap[(i - 1) // 2].priority >= \
                    req_book.reservation_heap[i].priority and i > 0:
                if req_book.reservation_heap[(i - 1) // 2].priority == \
                        req_book.reservation_heap[i].priority and i > 0:
                    if req_book.reservation_heap[(i - 1) // 2].timeofReservation < \
                            req_book.reservation_heap[i].timeofReservation and i > 0:
                        req_book.reservation_heap[i], req_book.reservation_heap[(i - 1) // 2] = \
                            req_book.reservation_heap[(i - 1) // 2], req_book.reservation_heap[i]

                req_book.reservation_heap[i], req_book.reservation_heap[(i - 1) // 2] = \
                    req_book.reservation_heap[(i - 1) // 2], req_book.reservation_heap[i]
                i = (i - 1) // 2


    def ReturnBook(self, file, patronID, bookID):
        ret_book = self.SearchBook(bookID)
        if len(ret_book.reservation_heap) == 0:
            ret_book.availability = "Yes"
            file.write("Book Returned")
        else:
            if len(ret_book.reservation_heap) > 0:
                file.write(f"Book {bookID} Returned by {ret_book.borrower_id}\n\n")
                file.write(f"Book {bookID} Allotted to Patron {ret_book.reservation_heap[0].patronID}\n\n")
                ret_book.borrower_id = ret_book.reservation_heap[0].patronID
                ret_book.reservation_heap[0] = ret_book.reservation_heap[-1]
                ret_book.reservation_heap.pop()
                i = 0
                while True:
                    left = (2 * (i+1)) - 1
                    right = (2 * (i+1))
                    least = 0
                    if right < len(ret_book.reservation_heap) and \
                            ret_book.reservation_heap[right].priority <= ret_book.reservation_heap[least].priority:
                        if ret_book.reservation_heap[right].priority == \
                                ret_book.reservation_heap[least].priority and i > 0:
                            if ret_book.reservation_heap[right].timeofReservation < \
                                    ret_book.reservation_heap[least].timeofReservation and i > 0:
                                least = right
                        else:
                            least = right
                    if left < len(ret_book.reservation_heap) and \
                            ret_book.reservation_heap[left].priority < ret_book.reservation_heap[least].priority:
                        if ret_book.reservation_heap[left].priority == \
                                ret_book.reservation_heap[least].priority and i > 0:
                            if ret_book.reservation_heap[left].timeofReservation < \
                                    ret_book.reservation_heap[least].timeofReservation and i > 0:
                                least = left
                        else:
                            least = left


                    if least != i:
                        ret_book.reservation_heap[i], ret_book.reservation_heap[least] = \
                            ret_book.reservation_heap[least], ret_book.reservation_heap[i]
                    else:
                        break

    def Right_Rotation(self, pp):
        p = pp.right
        pp.right = p.left
        if p.left != None:
            p.left.parent = pp

        p.parent = pp.parent
        if pp.parent == None:
            self.root = p
        elif pp == pp.parent.left:
            pp.parent.left = p
        else:
            pp.parent.right = p
        p.left = pp
        pp.parent = p

    def Left_Rotation(self, pp):
        p = pp.left
        pp.left = p.right
        if p.right != None:
            p.right.parent = pp

        p.parent = pp.parent
        if pp.parent == None:
            self.root = p
        elif pp == pp.parent.right:
            pp.parent.right = p
        else:
            pp.parent.left = p
        p.right = pp
        pp.parent = p

    def InsertBook(self, bookID, bookName, authorName, availabilityStatus):
        book = Book(bookID)
        book.book_id = bookID
        book.book_name = bookName
        book.author = authorName
        book.parent = None
        book.availability = availabilityStatus
        book.left = self.null_node
        book.right = self.null_node
        book.color = 1

        root = self.root
        parent = None

        while root != self.null_node:
            parent = root
            if book.book_id > root.book_id:
                root = root.right
            else:
                root = root.left
        book.parent = parent

        if parent == None:
            self.root = book
            book.color = 0
        elif book.book_id > parent.book_id:
            parent.right = book
            book.color = 1
        elif book.book_id < parent.book_id:
            parent.left = book
            book.color = 1

        if book.parent == None:
            book.color = 0
            return

        if book.parent.parent == None:
            return
        # print(book.parent.book_id, book.parent.color)
        while book.parent.color == 1:  # the parent of a newly inserted red node is also red
            pp = book.parent
            gp = pp.parent
            if pp == gp.left:  # when the node is the left child
                d = book.parent.parent.right
                if d.color == 1:  # XLr case
                    d.color = 0
                    d.color_flips += 1
                    if pp.color == 1:
                        pp.color_flips += 1
                    pp.color = 0
                    if gp.color == 0:
                        gp.color_flips += 1
                    gp.color = 1
                    book = gp  # recursively check for 2 red nodes in a row
                elif d.color == 0:  # XLb case
                    if book == pp.right:
                        book = pp
                        self.Right_Rotation(book)
                    if book.parent.color == 1:
                        book.parent.color_flips += 1
                    book.parent.color = 0
                    if book.parent.parent.color == 0:
                        book.parent.color_flips += 1
                    book.parent.parent.color = 1
                    self.Left_Rotation(book.parent.parent)
            elif book == pp.right:
                d = book.parent.parent.left
                if d.color == 1:
                    d.color = 0
                    d.color_flips += 1
                    if pp.color == 1:
                        pp.color_flips += 1
                    pp.color = 0
                    if gp.color == 0:
                        gp.color_flips += 1
                    gp.color = 1
                    d = gp
                elif d.color == 0:
                    if book == pp.left:
                        book = pp
                        self.Left_Rotation(book)
                    if book.parent.color == 1:
                        book.parent.color_flips += 1
                    book.parent.color = 0
                    if book.parent.parent.color == 0:
                        book.parent.parent.color_flips += 1
                    book.parent.parent.color = 1

                    self.Right_Rotation(book.parent.parent)
            if book == self.root:
                break
        self.root.color = 0

    def print_tree(self):
        self.__print_helper(self.root, "", True)

    def minimum(self, node):
        while node.left != self.null_node:
            node = node.left
        return node

    def maximum(self, node):
        while node.right != None:
            node = node.right
        return node

    def replace_tree(self, node_to_replace, replacement_node):
        if node_to_replace.parent is None:
            self.root = replacement_node
        # Case 2: Node to replace is a right child
        elif node_to_replace == node_to_replace.parent.right:
            node_to_replace.parent.right = replacement_node
        # Case 3: Node to replace is a left child
        else:
            node_to_replace.parent.left = replacement_node

        # Update the parent of the replacement node
        if replacement_node is not None:
            replacement_node.parent = node_to_replace.parent
        else:
            node_to_replace.parent = None

    def balance_after_delete(self, node):
        # Fix the red-black tree properties after deletion
        while node.color == 0 and node != self.root:
            # Case: x is a left child
            if node == node.parent.left:
                sibling = node.parent.right
                # Case 1: Sibling is red
                if sibling.color == 1:
                    sibling.color_flips += 1
                    sibling.color = 0
                    if node.parent.color == 0:
                        node.parent.color_flips += 1
                    node.parent.color = 1
                    self.right_rotation(node.parent)
                    sibling = node.parent.right

                # Case 2: Both children of sibling are black
                if sibling.left.color == 0 and sibling.right.color == 0:
                    sibling.color = 1
                    sibling.color_flips += 1
                    node = node.parent
                else:
                    # Case 3: Right child of sibling is black
                    if sibling.right.color == 0:
                        if sibling.left.color == 1:
                            sibling.left.color_flips += 1
                        sibling.left.color = 0
                        if sibling.color == 0:
                            sibling.color_flips += 1
                        sibling.color = 1
                        self.Left_Rotation(sibling)
                        sibling = node.parent.right

                    # Case 4: Sibling becomes the new parent
                    sibling.color = node.parent.color
                    if node.parent.color == 1:
                        node.parent.color_flips += 1
                    node.parent.color = 0
                    if sibling.right is not None:
                        if sibling.right.color == 1:
                            sibling.right.color_flips += 1
                        sibling.right.color = 0
                        self.Right_Rotation(node.parent)
                    node = self.root
            else:
                # Case: x is a right child
                sibling = node.parent.left

                # Case 1: Sibling is red
                if sibling.color == 1:
                    sibling.color = 0
                    sibling.color_flips += 1
                    if node.parent.color == 0:
                        node.parent.color_flips += 1
                    node.parent.color = 1
                    self.Left_Rotation(node.parent)
                    sibling = node.parent.left

                # Case 2: Both children of sibling are black
                if sibling.right.color == 0 and sibling.right.color == 0:
                    sibling.color = 1
                    sibling.color_flips += 1
                    node = node.parent
                else:
                    # Case 3: Left child of sibling is black
                    if sibling.left.color == 0:
                        if sibling.right.color == 1:
                            sibling.right.color_flips += 1
                        sibling.right.color = 0
                        if sibling.color == 0:
                            sibling.color_flips += 1
                        sibling.color = 1
                        self.right_rotation(sibling)
                        sibling = node.parent.left

                    # Case 4: Sibling becomes the new parent
                    sibling.color = node.parent.color
                    if node.parent.color == 1:
                        node.parent.color_flips += 1
                    node.parent.color = 0
                    if sibling.left.color == 1:
                        sibling.left.color_flips += 1
                    sibling.left.color = 0
                    self.Left_Rotation(node.parent)
                    node = self.root

        # Set the color of the current node to black
        if node.color == 1:
            node.color_flips += 1
        node.color = 0

    def delete_book(self, output_file, root_node, target_key):
        #Search for the node with the target key
        current_node = self.null_node
        while root_node != self.null_node:
            if root_node.book_id == target_key:
                current_node = root_node
            if root_node.book_id > target_key:
                root_node = root_node.left
            elif root_node.book_id <= target_key:
                root_node = root_node.right

        # If the target key is not found, write a message and return
        if current_node == self.null_node:
            output_file.write("Cannot find the key in the tree\n")
            return

        #Output information about the book and its reservations
        reservations = self.printReservations(current_node.book_id)
        output_file.write(f"Book {current_node.book_id} is no longer available.\n")
        if len(reservations) > 0:
            output_file.write(f"Reservations made by Patrons {reservations} have been cancelled!\n")

        #Identify the node to be deleted and its original color
        node_to_delete = current_node
        original_color = node_to_delete.color

        #Determine the replacement node based on the number of children
        if current_node.left == self.null_node:  # Case when the node to be deleted is a leaf node
            replacement_node = current_node.right
            self.replace_tree(current_node, current_node.right)
        elif current_node.right == self.null_node:
            replacement_node = current_node.left
            self.replace_tree(current_node, current_node.left)
        else:
            # For a node with two children, find the minimum node in the right subtree
            node_to_delete = self.minimum(current_node.right)
            original_color = node_to_delete.color
            replacement_node = node_to_delete.right

            # Update the parent and child relationships
            if node_to_delete.parent == current_node:
                replacement_node.parent = node_to_delete
            else:
                self.replace_tree(node_to_delete, node_to_delete.right)
                node_to_delete.right = current_node.right
                node_to_delete.right.parent = node_to_delete

            # Perform the transplant operation
            self.replace_tree(current_node, node_to_delete)
            node_to_delete.left = current_node.left
            node_to_delete.left.parent = node_to_delete
            node_to_delete.color = current_node.color

        # Step 5: Fix the tree if the original color of the deleted node was black
        if original_color == 0:
            self.balance_after_delete(replacement_node)

    def DeleteBook(self, file, item):
        self.delete_book(file, self.root, item)

    def execute_commands(self, input_file, output_file):
        output = open(output_file, 'w')
        with open(input_file) as f:
            func_calls = f.readlines()
        func_calls = [line.strip() for line in func_calls]
        for line in func_calls:
            args = re.search(r"\((.*)\)", line).group(1)
            if re.search(r"^printbook\(", line.lower()):
                self.PrintBook(output, int(args))
            elif re.search(r"^insertbook", line.lower()):
                book_id, book_name, book_author, avail_stat = args.split(', "')
                avail_stat = avail_stat.strip('"')
                book_id = book_id.strip('"')
                book_name = book_name.strip('"')
                book_author = book_author.strip('"')
                self.InsertBook(int(book_id), book_name, book_author, avail_stat)
            elif re.search(r"^printbooks", line.lower()):
                try:
                    start, end = args.split(", ")
                except:
                    start, end = args.split(",")
                self.PrintBooks(output, int(start), int(end))
            elif re.search(r"^borrowbook", line.lower()):
                patron_id, book_id, priority = args.split(", ")
                self.BorrowBook(output, int(patron_id), int(book_id), int(priority))
            elif re.search(r"^returnbook", line.lower()):
                patron_id, book_id = args.split(", ")
                self.ReturnBook(output, int(patron_id), int(book_id))
            elif re.search(r"^deletebook", line.lower()):
                book_id = args.strip('"')
                self.DeleteBook(output, int(book_id))
            elif re.search(r"^findclosestbook", line.lower()):
                self.FindClosestBook(output, int(args))
            elif re.search(r"^colorflipcount", line.lower()):
                self.ColorFlipCount(output)
            elif re.search(r"^quit", line.lower()):
                output.write(f"Program Terminated!!")
                break
        output.close()