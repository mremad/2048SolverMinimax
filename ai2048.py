
from game2048 import Game
from node import Node

UP = "w"
DOWN = "s"
LEFT = "a"
RIGHT = "d"

class MiniMaxSolver:

    def __init__(self, target):

        self.max_depth = 3
        self.root = Node()
        self.hist_states = dict()
        self.target = target

    def build_tree(self, game):
        PLAYER = 0
        CPU = 1

        queue = []

        root = Node()
        root.set_board_key(game.board)
        self.hist_states[root.node_key] = True

        curr_level = 0
        curr_turn = PLAYER

        queue.append(root)

        while True:
            if len(queue) == 0:
                return None
            proc_node = queue.pop(0)
            #print proc_node.depth
            if proc_node.depth > self.max_depth:
                break

            curr_board = proc_node.get_board()
            if proc_node.type == "min":
                poss = game.get_possible_cells(curr_board)
                for cell in poss:
                    for val in [2,4]:
                        new_board = game.make_computer_move(curr_board,cell,val)
                        new_node = Node()
                        new_node.set_board_key(new_board)
                        #if new_node.node_key in self.hist_states:
                            #print "found prev state"
                        #    continue
                        new_node.type = "max"
                        new_node.depth = proc_node.depth + 1
                        proc_node.children.append(new_node)
                        new_node.parent = proc_node
                        self.hist_states[new_node.node_key] = True
                queue.extend(proc_node.children)
            else:
                new_board_left = game.player_turn(LEFT, curr_board)
                new_board_right = game.player_turn(RIGHT, curr_board)
                new_board_up = game.player_turn(UP, curr_board)
                new_board_down = game.player_turn(DOWN, curr_board)

                poss = [new_board_left, new_board_right, new_board_up, new_board_down]
                actions = [LEFT, RIGHT, UP, DOWN]
                for new_board, action in zip(poss, actions):
                    if new_board == None:
                        continue
                    new_node = Node()
                    new_node.set_board_key(new_board)
                    new_node.action = action
                    #if new_node.node_key in self.hist_states:
                        #print "found prev state"
                    #    continue
                    new_node.type = "min"
                    new_node.depth = proc_node.depth + 1
                    proc_node.children.append(new_node)
                    new_node.parent = proc_node
                    self.hist_states[new_node.node_key] = True
                queue.extend(proc_node.children)
        return root

    def perform_minimax_update(self, tree):
        if len(tree.children) == 0:
            if self.target == "smooth":
                return tree.calculate_board_score_smooth()
            elif self.target == "emptiness":
                return tree.calculate_board_score_emptiness()


        if tree.type == "max":
            max = -100000000
            for child in tree.children:
                child.score = self.perform_minimax_update(child)
                if child.score > max:
                    max = child.score
                    tree.action = child.action
            tree.score = max
            return tree.score
        else:
            min = 500000
            for child in tree.children:
                child.score = self.perform_minimax_update(child)
                if child.score < min:
                    min = child.score
            tree.score = min
            return tree.score

    def update_scores(self, tree):
        self.perform_minimax_update(tree)

        return tree


    def run_minimax(self, game):
        max_nodes = None


def main():
    game = Game()
    game.initialize_board()
    game.board = game.computer_turn(game.board)
    target = "smooth"
    allowed_moves = -1
    while True:
        minimax_sol = MiniMaxSolver(target)
        minimax_sol.max_depth = 3

        #print "building tree..."
        tree = minimax_sol.build_tree(game)
        if tree == None:
            break
        #print "updating tree..."
        tree = minimax_sol.update_scores(tree)
        #tree.print_tree()

        new_action = tree.action
        print tree.score
        new_move = game.player_turn(new_action, game.board)
        game.board = new_move
        game.board = game.computer_turn(game.board)
        game.print_board(game.board)
        allowed_moves -= 1

        if allowed_moves == 0:
            if target == "smooth":
                target = "emptiness"
                allowed_moves = 3
            else:
                target = "smooth"
                allowed_moves = 9*5
    game.print_board(game.board)

if __name__ == "__main__":
    runs = 20

    for i in range(runs):
        main()
        break