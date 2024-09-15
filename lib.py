import random
import math
from copy import deepcopy

# Define primitives
class Primitive:
    def __init__(self, name, func, is_atom=False):
        self.name = name
        self.func = func  # Function to execute
        self.is_atom = is_atom  # True if atom, False if curried function

    def __call__(self, *args):
        return self.func(*args)

# Evaluation function
def evaluate(array):
    """
    Recursively evaluates the array.
    """
    if not isinstance(array, list):
        if array.is_atom:
            return array()
        else:
            raise ValueError("Invalid primitive usage.")
    else:
        func = array[0]
        args = array[1:]
        if not func.is_atom:
            if len(args) == 1:
                arg_value = evaluate(args[0])
                return func(arg_value)
            else:
                raise ValueError("Curried functions must have exactly one argument.")
        else:
            raise ValueError("Atoms cannot be called as functions.")

# MCTS Node
class Node:
    def __init__(self, state, parent=None):
        self.state = state  # The array representing the program
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0  # Total value from simulations

    def is_fully_expanded(self, n_max):
        return len(self.children) >= len(self.get_possible_actions(n_max))

    def get_possible_actions(self, n_max):
        actions = []
        # Generate possible insertions to the left and right
        if len(self.state) < n_max:
            for prim in PRIMITIVES:
                # Insert to the left
                new_state_left = deepcopy(self.state) + [prim]
                actions.append(('insert_left', new_state_left))

                # Insert to the right
                new_state_right = [prim] + deepcopy(self.state)
                actions.append(('insert_right', new_state_right))
        return actions

    def expand(self, n_max):
        actions = self.get_possible_actions(n_max)
        for action_type, new_state in actions:
            child_node = Node(new_state, parent=self)
            self.children.append(child_node)

    def best_child(self, c_param=1.4):
        choices_weights = [
            (child.value / child.visits) + c_param * math.sqrt((2 * math.log(self.visits) / child.visits))
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def tree_policy(self, n_max):
        current_node = self
        while not current_node.is_terminal():
            if not current_node.is_fully_expanded(n_max):
                current_node.expand(n_max)
                return random.choice(current_node.children)
            else:
                current_node = current_node.best_child()
        return current_node

    def is_terminal(self):
        # Define a termination condition, e.g., maximum depth or perfect score
        return len(self.state) >= n_max or goal(self.state) == 1

    def default_policy(self, n_max):
        current_state = deepcopy(self.state)
        while len(current_state) < n_max:
            possible_actions = self.get_possible_actions(n_max)
            if not possible_actions:
                break
            action = random.choice(possible_actions)
            current_state = action[1]
            if goal(current_state) == 1:
                break
        return goal(current_state)

    def backup(self, reward):
        current_node = self
        while current_node is not None:
            current_node.visits += 1
            current_node.value += reward
            current_node = current_node.parent

# MCTS Algorithm
def mcts(root, n_iter, n_max):
    for _ in range(n_iter):
        leaf = root.tree_policy(n_max)
        reward = leaf.default_policy(n_max)
        leaf.backup(reward)
    return root.best_child(c_param=0)
