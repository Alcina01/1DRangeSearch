# It is also Important to know that we use balanced Binary tree for this Range Search Algorithm

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(root, value):
    if root is None:
        return TreeNode(value)
    
    if value < root.value:
        root.left = insert(root.left, value)
    elif value > root.value:
        root.right = insert(root.right, value)

    return root

def build_tree():
    root = None
    n = int(input("Enter the number of elements: "))
    
    for _ in range(n):
        value = int(input("Enter a value: "))
        root = insert(root, value)

    return root
 
# // This is just to see my input in order to verify the working of the code, not essential to the range Search and can be omitted. //
def print_tree(root):  
    if root is not None:
        print_tree(root.left)
        print(root.value, end=" ")
        print_tree(root.right)

# // This Function basically finds the node where we can start splitting the vertices, 
# z.B. for very large amounts of inputs, only the right/left subtree might be needed 
# therefore this routine reduces drastically the time required to search for points in range //
def FINDSPLITNODE(root, x, x_prime): 
    current = root
    while current is not None and (current.left is not None or current.right is not None) and (x_prime <= current.value or x > current.value):
        if x_prime <= current.value:
            current = current.left
        else:
            current = current.right
    return current

# This function is recursively called to add all the leaves of nodes we know 
# are definitely in the range  Since the number of internal nodes of any
# binary tree is less than its number of leaves, this subroutine takes an amount of
# time that is linear in the number of reported points
def REPORTSUBTREE(node):
    if node is not None:
        if node.left is None and node.right is None:
            return [node.value]
        else:
            left_subtree = REPORTSUBTREE(node.left) if node.left else []
            right_subtree = REPORTSUBTREE(node.right) if node.right else []
            return left_subtree + right_subtree +[node.value]
    return []

# Having a time complexity of O(log n), n is the number of nodes in the tree,
# the range search function  
def DRANGEQUERY(root, x, x_prime):
    if root.value==x or root.value==x_prime:
        rootmain=root
    split_node = FINDSPLITNODE(root, x, x_prime)

    if split_node is not None and split_node.left is None and split_node.right is None:
        return [split_node.value]
    else:
        result = []
        result+=[rootmain.value]
        result+=[split_node.value]
        current = split_node.left
        while current is not None:
            if (x <= current.value):
                result+=[current.value]
                result += REPORTSUBTREE(current.right)
                current = current.left
            else:
                current = current.right
        
        current = split_node.right
        while current is not None :
            if (x_prime >= current.value):
                result+=[current.value]
                result += REPORTSUBTREE(current.left)
                current = current.right
            else:
                current = current.left

        return result
    


root = build_tree()

x = int(input("Enter the lower bound of the range: "))
x_prime = int(input("Enter the upper bound of the range: "))
print("Lower Bound :",x)
print("Upper Bound :",x_prime)
print("Tree values in inorder traversal:\n")
print_tree(root)
print("\n")

result = DRANGEQUERY(root, x, x_prime)

print("Points in the range:", result)

# The time spent in a call to REPORTSUBTREE is linear in the
#  number of reported points. Hence, the total time spent in all such calls is O(k).
#  The remaining nodes that are visited are nodes on the search path of x or x′.
#  Because T is balanced, these paths have length O(logn). The time we spend
#  at each node is O(1), so the total time spent in these nodes is O(logn), which
#  gives a query time of O(logn+k).
