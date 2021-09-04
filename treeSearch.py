class TreeNode:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.children = []

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get_level(self):
        level = 0
        parent = self.parent
        while parent:
            parent = parent.parent
            level += 1
        return level

    def print_tree(self):
        prefix = "\t" * self.get_level() + "|___" if self.parent else ""
        print(prefix + str(self.data))
        for child in self.children:
            child.print_tree()
