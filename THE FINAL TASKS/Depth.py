import sys
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def building_tree():
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if line == '-':
            break
        if line:
            lines.append(line)

    if not lines:
        return None

    n = int(lines[0])
    nodes = {}


    for line in lines[1:n + 1]:
        parts = line.split()
        node_id = int(parts[0])
        value = int(parts[1])
        nodes[node_id] = TreeNode(value)


    for line in lines[1:n + 1]:
        parts = line.split()
        node_id = int(parts[0])
        left_id = parts[2] if parts[2] != 'None' else None
        right_id = parts[3] if parts[3] != 'None' else None

        if left_id is not None:
            nodes[node_id].left = nodes[int(left_id)]
        if right_id is not None:
            nodes[node_id].right = nodes[int(right_id)]

    return nodes.get(0, None)  # Корень с id=0

def max_depth(root):
    if not root:
        return 0
    return max(max_depth(root.left), max_depth(root.right)) + 1

print()
root = building_tree()
print(max_depth(root))