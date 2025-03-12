import sys
class Node():
    def __init__(self, book_id):
        self.book_id = book_id
        self.book_name = None
        self.author = None
        self.availability = None
        self.borrower_id = None
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1
        self.color_flips = 0

class RedBlackTree():
    def __init__(self):
        # self.TNULL = Node(0)
        # self.TNULL.color = 0 #root node is always black
        # self.TNULL.left = None
        # self.TNULL.right = None
        self.root = None

    def fix_insert(self, node):
        while node.parent.color == 1:
            if node.parent == node.parent.parent.right:
                u = node.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.left_rotate(node.parent.parent)
            else:
                u = node.parent.parent.right

                if u.color == 1:
                    u.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.right_rotate(node.parent.parent)
            if node == self.root:
                break
        self.root.color = 0
    def LL_rotate(self, node):
        print("tuch to chutiya")
        pp = node.parent
        gp = node.parent.parent
        gp.left = pp.right

        pp.right.parent = gp
        pp.right = gp
        gp.parent = pp
        pp.parent = gp.parent
        gp.parent = pp
        if gp.parent != None:
            p = self.root
        pp.color = 0


    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.item = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1
        y = None
        x = self.root
        #print(x.book_id)
        while x != self.TNULL:
            y = x
            if node.item < x.item: #make changes here
                x = x.left
            else:
                x = x.right
        node.parent = y
        if y == None:
            self.root = node
        elif node.item < y.item:
            y.left = node
            node.color = 1
        else:
            y.right = node
            node.color = 1

        if node.parent == None:
            node.color = 0
            return

        if node.parent.parent == None:
            return

        #self.fix_insert(node)

    def __print_helper(self, node, indent, last):
        if node != None:
            print(indent)
            if last:
                print("R----")
                indent += "     "
            else:
                print("L----")
                indent += "|    "
            s_color = "RED" if node.color == 1 else "BLACK"
            print(str(node.book_id) + "(" + s_color + ")", node.color_flips)
            if node.parent != None:
                print(node.parent.book_id)
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)

    def print_tree(self):
        self.__print_helper(self.root, "", True)

    def InsertBook(self, bookID, bookName, authorName, availabilityStatus):
        book = Node(bookID)
        book.book_id = bookID
        book.book_name = bookName
        book.author = authorName
        book.availability = availabilityStatus
        book.left = None
        book.right = None
        book.color = 1
        root = self.root
        parent = None

        while root != None:
            parent = root
            if book.book_id > root.book_id:
                root = root.right
            else:
                root = root.left
        book.parent = parent
        #if parent != None:
            #print(book.book_id, parent.book_id)


        if self.root == None:
            self.root = book
            book.color = 0
        elif book.book_id > parent.book_id:
            parent.right = book
            book.color = 1
        elif book.book_id < parent.book_id:
            parent.left = book
            book.color = 1
        if book.parent == None:
            return

        if book.parent.parent == None:
            return
        #fix insert
        gp = book.parent.parent
        pp = book.parent
        while pp.color == 1:
            if pp == gp.right:
                r = gp.left
            elif pp == gp.left:
                r = gp.right
            if r == None:
                print(gp.book_id, pp.book_id)
                if pp == gp.right:
                    gp.right = pp.left
                    if pp.left != None:
                        pp.left.parent = gp
                    pp.left = gp
                    if gp.parent == None:
                        self.root = pp
                    elif gp == gp.parent.right:
                        gp.parent.right = pp
                    else:
                        gp.parent.left = pp
                    pp.parent = gp.parent
                    gp.parent = pp
                    print("kakakaka", book.book_id)

                elif pp == gp.left:
                    gp.left = pp.right
                    pp.right.parent = gp
                    pp.right = gp
                    if gp.parent == None:
                        self.root = pp
                    elif gp == gp.parent.right:
                        gp.parent.right = pp
                    else:
                        gp.parent.left = pp
                    pp.parent = gp.parent
                    gp.parent = pp
                pp.color = 0
            if r != None and r.color == 1:
                pp.color = 0
                r.color = 0
                if gp != self.root:
                    gp.color = 1
                    gp.color_flips += 1
                r.color_flips += 1
                pp.color_flips += 1
                book.parent.parent = gp
                book.parent = pp
            elif r != None and r.color == 0:
                print("he jhala")
                self.LL_rotate(book)
        print(book.book_id, book.parent.book_id)

        #print(book.book_id, book.color_flips)
            # if r == None:
            #     return








        # if book.parent == None:
        #     book.color = 0
        #     return
        # if book.parent.parent == None:
        #     return






if __name__ == "__main__":
    bst = RedBlackTree()
    bst.InsertBook(55, "Book1", "Author1", "Yes")
    bst.InsertBook(40, "Book2", "Author2", "Yes")
    bst.InsertBook(75, "Book2", "Author2", "Yes")
    #bst.InsertBook(65, "Book5", "Author5", "Yes")
    bst.InsertBook(85, "Book4", "Author4", "Yes")
    bst.InsertBook(65, "Book3", "Author3", "Yes")
    bst.InsertBook(60, "Book5", "Author5", "Yes")
    bst.InsertBook(27, "Book6", "Author6", "Yes")
    # bst.InsertBook(85, "Book7", "Author7", "Yes")
    # bst.insert(55)
    # bst.insert(40)
    # bst.insert(65)
    # bst.insert(60)
    # bst.insert(75)
    # bst.insert(57)
    # bst.insert(35)
    # bst.insert(85)
    bst.print_tree()
