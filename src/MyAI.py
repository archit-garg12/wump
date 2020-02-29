# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        #[action , prev_pos, curr_pos]
        self.moves = []
        # self.pos = [[()]]
        self.stench_tracker = set()
        self.traveled = set()
        self.prev_action = 0
        self.curr_pos = (1,1)
        #(0,1) is north, (1,0) is east, (0,-1) is south, (-1,0)  is west
        self.curr_direction = (1,0)
        self.maze_counter = 0
        self.back_tracking = False
        self.action_queue = []
        self.found_gold = False
        self.max_x = float('inf')
        self.max_y = float('inf')
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):

        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        
        print("moves", self.moves)
        if self.action_queue == []:
            self.determineAction(stench, breeze, glitter, bump, scream)
        print("action queue", self.action_queue)
        current_action = self.action_queue.pop()
        print("direction", self.curr_direction)
        if current_action == Agent.Action.FORWARD:
            possible_moves = self.all_moves()
            cant_move_adj = [True if p in self.traveled else False for p in possible_moves]
            next_x = self.curr_pos[0] + self.curr_direction[0]
            next_y = self.curr_pos[1] + self.curr_direction[1]
            print("possible move", next_x, next_y)
            if ((next_x < self.max_x and next_x >= 1)) and (next_y < self.max_y and next_y >= 1):
                print("in constraintes")
                next_pos = (next_x, next_y)
            else:
                next_pos = self.curr_pos
            print("currpos",self.curr_pos,"nextpos", next_pos, self.traveled)
            if all(cant_move_adj) and self.moves != []:
                 self.action_queue = self.moves.pop().undo_action()
                 self.back_tracking = True
            elif all(cant_move_adj) and self.moves == []:
                return Agent.Action.CLIMB
            elif next_pos not in self.traveled or self.back_tracking:
                self.prev_pos = self.curr_pos
                self.curr_pos = next_pos
                self.traveled.add((self.curr_pos))

            else:
                current_action = Agent.Action.TURN_RIGHT
            if not self.back_tracking and current_action == Agent.Action.FORWARD and not bump:
                self.moves.append(ActionType(self.prev_pos, self.curr_pos, self.curr_direction))
        if current_action == Agent.Action.TURN_RIGHT or current_action == Agent.Action.TURN_LEFT:
            self.curr_direction = self.choose_dir(self.curr_direction, current_action)
        return current_action
        
    def all_moves(self):
        possible_moves = set()
        for x in [(1,0), (0,1), (-1,0), (0,-1)]:
            if 1 <= x[0] + self.curr_pos[0] < self.max_x and 1 <= x[1] + self.curr_pos[1] < self.max_y:
                possible_moves.add((x[0] + self.curr_pos[0], x[1] + self.curr_pos[1]))
        return possible_moves
    def determineAction(self, stench, breeze, glitter, bump, scream):

        self.back_tracking = False
        if glitter:
            self.action_queue = [Agent.Action.GRAB]
            self.found_gold = True
        elif self.found_gold:
            if self.moves != []:
                self.action_queue = self.moves.pop().undo_action()
            else:
                self.action_queue = [Agent.Action.CLIMB]
            self.back_tracking = True
        elif breeze:
            
            if self.curr_pos == (1,1):
                self.action_queue = [Agent.Action.CLIMB]
            else:
                self.action_queue = self.moves.pop().undo_action()
                self.back_tracking = True
           

        elif stench:
            if self.curr_pos == (1,1):
                self.action_queue = [Agent.Action.CLIMB]
            else:
                self.stench_tracker.add(self.curr_pos)
        elif bump:
            if self.curr_pos[0] >= self.curr_pos[1] and self.curr_direction == (-1,0):
                self.max_x = self.curr_pos[0]
            elif self.curr_pos[0] < self.curr_pos[1] and self.curr_direction == (0, -1):
                self.max_y = self.curr_pos[1]
            print(self.max_x, self.max_y)
            self.action_queue = [Agent.Action.FORWARD, Agent.Action.TURN_RIGHT]
            
        else:
            self.action_queue = [Agent.Action.FORWARD]

    def choose_dir(self, current_dir, current_action=None):
        if current_action == Agent.Action.TURN_LEFT or current_action == None:
            if current_dir == (0, 1):
                return (-1, 0)
            elif current_dir == (1, 0):
                return (0, 1)
            elif current_dir == (0, -1):
                return (1, 0)
            elif current_dir == (-1, 0):
                return (0, -1)
        elif current_action == Agent.Action.TURN_RIGHT:
            if current_dir == (0, 1):
                return (1, 0)
            elif current_dir == (1, 0):
                return (0, -1)
            elif current_dir == (0, -1):
                return (-1, 0)
            elif current_dir == (-1, 0):
                return (0, 1)
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
   
           

class ActionType(MyAI):
    def __init__(self, prev_pos, curr_pos, current_dir):
        self.curr_dir = current_dir
        self.r_dir = (-curr_pos[0]+prev_pos[0],-curr_pos[1]+prev_pos[1])
    def undo_action(self):
        print("undoing")
        return_actions = []
        return_actions.append(Agent.Action.FORWARD)
        print("initial pos", self.curr_dir)
        while self.curr_dir != self.r_dir:
            self.curr_dir = self.choose_dir(self.curr_dir)
            print("goal turn", self.r_dir,"currently faceing", self.curr_dir)
            return_actions.append(Agent.Action.TURN_LEFT)
        return return_actions
    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
