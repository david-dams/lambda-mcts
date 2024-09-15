from lib import *

# Example primitives
def add(a):
    return lambda b: a + b

def const(value):
    return value

ADD = Primitive('ADD', add)
CONST_ONE = Primitive('1', lambda: 1, is_atom=True)
CONST_TWO = Primitive('2', lambda: 2, is_atom=True)
PRIMITIVES = [ADD, CONST_ONE, CONST_TWO]

# Goal function
def goal(array):
    """
    User-defined function that evaluates the array and returns a value between 0 and 1.
    For simplicity, let's assume the goal is to compute the value 6.
    The closer the evaluated result is to 6, the higher the score.
    """
    try:
        result = evaluate(array)
        score = max(0, 1 - abs(result - 6) / 6)
        return score
    except Exception:
        return 0  # Invalid programs score 0


# Main Execution
if __name__ == "__main__":
    n_max = 5  # Maximum size of the array
    root_state = []
    root_node = Node(root_state)

    best_node = mcts(root_node, n_iter=1000, n_max=n_max, goal = goal)
    print("Best program found:", best_node.state)
    print("Evaluated to:", evaluate(best_node.state))
    print("Goal score:", goal(best_node.state))
