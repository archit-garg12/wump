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
        # #[action , prev_pos, curr_pos]
        # self.moves = []
        # # self.pos = [[()]]
        # self.stench_tracker = set()
        # self.traveled = set()
        # self.prev_action = 0
        # self.current_position = (1, 1)
        # #(0,1) is north, (1,0) is east, (0,-1) is south, (-1,0)  is west
        # self.curr_direction = (1,0)
        # self.maze_counter = 0
        # self.back_tracking = False
        # self.action_queue = []
        # self.found_gold = False
        # self.max_x = float('inf')
        # self.max_y = float('inf')
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

        self.last_action = Agent.Action.FORWARD
        self.last_position = (1,1)
        self.visited_positions = set()
        self.position_stack = []
        self.action_queue = [Agent.Action.CLIMB]
        self.current_direction = (1,0)
        self.current_position = (1,1)
        self.stench_tracker = list()
        self.wumpus_position = []
        self.max_x = float("inf")
        self.max_y = float("inf")
        self.wumpus_dead = False
        self.has_gold = False
    def getAction( self, stench, breeze, glitter, bump, scream ):

        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        print("positions before visit",self.position_stack)
        print("visited", self.visited_positions)
        print("actions",self.action_queue)
        if self.wumpus_dead:
            stench = False
        if self.last_action == Agent.Action.FORWARD:

            print("check empty", self.getUnvisitedAdjacentPositions())
            self.visited_positions.add(self.current_position)
            # if self.getUnvisitedAdjacentPositions() != set():
            #     self.position_stack.append(self.last_position)
            if (breeze or stench) and self.current_position == (1,1):
                print("running")
                return Agent.Action.CLIMB
                
            if self.current_position == (1,1) and (self.has_gold or self.getUnvisitedAdjacentPositions() == set()):
                print("running2")
                return Agent.Action.CLIMB
            if stench and not breeze:
                if self.current_position not in self.stench_tracker:
                    self.stench_tracker.append(self.current_position)
                if(self.findWumpusLocation(len(self.stench_tracker))):
                    self.position_stack.append(self.current_position)
                    self.position_stack.append(self.wumpus_position)            
            if bump:
                if self.current_direction == (1, 0):
                    self.max_x = self.current_position[0] -1
                    self.current_position = (self.current_position[0]-1, self.current_position[1])
                elif self.current_direction == (0, 1):
                    self.max_y = self.current_position[1] -1
                    self.current_position = (self.current_position[0], self.current_position[1]-1)
                print("MAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXESREEEEEEEEEEEEEEEEEEEEEEEEEEEee",self.max_x, self.max_y, self.current_position)
            elif not breeze and not stench and not glitter and not self.has_gold:
                for position in self.getUnvisitedAdjacentPositions():
                    self.position_stack.append(self.current_position)
                    self.position_stack.append(position)
            print(self.visited_positions)
            print("postitions after visit", self.position_stack)
            next_position = self.position_stack.pop()
            while self.current_position == next_position or next_position[0] > self.max_x or next_position[1] > self.max_y:
                next_position = self.position_stack.pop()
            self.queuePosition(next_position, Agent.Action.FORWARD)
            print("current posiiton", self.current_position)
            print("next position",next_position)
            print("current direction", self.current_direction)
            if glitter:
                self.action_queue.insert(0,Agent.Action.GRAB)
                self.has_gold = True
            self.last_position = self.current_position
            self.current_position = next_position
        if scream:
            self.wumpus_dead = True
            for x in self.stench_tracker:
                if x in self.visited_positions:
                    self.visited_positions.remove(x)
            # print("WUMPUS DEAD")
        self.last_action = self.action_queue.pop(0)
        return self.last_action

    def queuePosition(self, new_position, endAction):
        print((new_position[0] - self.current_position[0], new_position[1] - self.current_position[1]))
        print(self.current_position, new_position, "asdadasda")
        turns = self.getTurns( (new_position[0] - self.current_position[0], new_position[1] - self.current_position[1]) )
        self.current_direction = (new_position[0] - self.current_position[0], new_position[1] - self.current_position[1])
        self.action_queue = turns + self.action_queue
        self.action_queue.insert(len(turns), endAction)
        if self.wumpus_dead != True and len(self.wumpus_position) != 0:
            self.action_queue.insert(len(turns), Agent.Action.SHOOT)

    def getTurns(self, new_direction):
        turns = []
        print(new_direction, self.current_direction, "BFLASFKAFLAFH")
        temp_direction = self.current_direction
        while temp_direction != new_direction:
            left_turn = self.chooseDirection(temp_direction,  Agent.Action.TURN_LEFT)
            right_turn = self.chooseDirection(temp_direction,  Agent.Action.TURN_RIGHT)
            if left_turn == new_direction:
                temp_direction = left_turn
                turns.append(Agent.Action.TURN_LEFT)
            elif right_turn == new_direction:
                temp_direction = right_turn
                turns.append(Agent.Action.TURN_RIGHT)
            else:
                temp_direction = left_turn
                turns.append(Agent.Action.TURN_LEFT)
            # print(temp_direction, new_direction)
        return turns
    def findWumpusLocation(self ,tracker):
        if len(self.wumpus_position) != 0:
            return False
        if tracker == 2:
            if self.stench_tracker[0][0] == self.stench_tracker[1][0]:
                self.wumpus_position = (self.stench_tracker[0][0] ,min(self.stench_tracker[0][1], self.stench_tracker[1][1]) + 1)
                return True
            elif self.stench_tracker[0][1] == self.stench_tracker[1][1]:
                self.wumpus_position = (min(self.stench_tracker[0][0], self.stench_tracker[1][0]) + 1, self.stench_tracker[1][1])
                return True
            else:
                if (self.stench_tracker[0][0], self.stench_tracker[1][1]) in self.visited_positions:
                    self.wumpus_position = (self.stench_tracker[1][0], self.stench_tracker[0][1])
                    return True
                elif (self.stench_tracker[1][0], self.stench_tracker[0][1]) in self.visited_positions:
                    self.wumpus_position = (self.stench_tracker[0][0], self.stench_tracker[1][1])
                    return True 

    def getUnvisitedAdjacentPositions(self):
        possible_moves = set()
        for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_position = (direction[0] + self.current_position[0], direction[1] + self.current_position[1])
            if 1 <= new_position[0] <= self.max_x and 1 <= new_position[1] <= self.max_y and \
                    new_position not in self.visited_positions:
                possible_moves.add(new_position)
        return possible_moves

    def chooseDirection(self, current_dir, current_action=None):
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

#     def old(self):
#         print("moves", self.moves)
#         if self.action_queue == []:
#             self.determineAction(stench, breeze, glitter, bump, scream)
#         print("action queue", self.action_queue)
#         current_action = self.action_queue.pop()
#         print("direction", self.curr_direction)
#         if current_action == Agent.Action.FORWARD:
#             possible_moves = self.all_moves()
#             cant_move_adj = [True if p in self.traveled else False for p in possible_moves]
#             next_x = self.current_position[0] + self.curr_direction[0]
#             next_y = self.current_position[1] + self.curr_direction[1]
#             print("possible move", next_x, next_y)
#             if ((next_x < self.max_x and next_x >= 1)) and (next_y < self.max_y and next_y >= 1):
#                 print("in constraintes")
#                 next_pos = (next_x, next_y)
#             else:
#                 next_pos = self.current_position
#             print("currpos", self.current_position, "nextpos", next_pos, self.traveled)
#             if all(cant_move_adj) and self.moves != []:
#                  self.action_queue = self.moves.pop().undo_action()
#                  self.back_tracking = True
#             elif all(cant_move_adj) and self.moves == []:
#                 return Agent.Action.CLIMB
#             elif next_pos not in self.traveled or self.back_tracking:
#                 self.prev_pos = self.current_position
#                 self.current_position = next_pos
#                 self.traveled.add((self.current_position))
#
#             else:
#                 current_action = Agent.Action.TURN_RIGHT
#             if not self.back_tracking and current_action == Agent.Action.FORWARD and not bump:
#                 self.moves.append(ActionType(self.prev_pos, self.current_position, self.curr_direction))
#         if current_action == Agent.Action.TURN_RIGHT or current_action == Agent.Action.TURN_LEFT:
#             self.curr_direction = self.choose_dir(self.curr_direction, current_action)
#         return current_action
#
#     def all_moves(self):
#         possible_moves = set()
#         for x in [(1,0), (0,1), (-1,0), (0,-1)]:
#             if 1 <= x[0] + self.current_position[0] <= self.max_x and 1 <= x[1] + self.current_position[1] <= self.max_y:
#                 possible_moves.add((x[0] + self.current_position[0], x[1] + self.current_position[1]))
#         return possible_moves
#     def determineAction(self, stench, breeze, glitter, bump, scream):
#
#         self.back_tracking = False
#         if glitter:
#             self.action_queue = [Agent.Action.GRAB]
#             self.found_gold = True
#         elif self.found_gold:
#             if self.moves != []:
#                 self.action_queue = self.moves.pop().undo_action()
#             else:
#                 self.action_queue = [Agent.Action.CLIMB]
#             self.back_tracking = True
#         elif breeze:
#
#             if self.current_position == (1, 1):
#                 self.action_queue = [Agent.Action.CLIMB]
#             else:
#                 self.action_queue = self.moves.pop().undo_action()
#                 self.back_tracking = True
#
#
#         elif stench:
#             if self.current_position == (1, 1):
#                 self.action_queue = [Agent.Action.CLIMB]
#             else:
#                 self.stench_tracker.add(self.current_position)
#         elif bump:
#             if self.current_position[0] >= self.current_position[1] and self.curr_direction == (-1, 0):
#                 self.max_x = self.current_position[0]
#             elif self.current_position[0] < self.current_position[1] and self.curr_direction == (0, -1):
#                 self.max_y = self.current_position[1]
#             print(self.max_x, self.max_y)
#             self.action_queue = [Agent.Action.FORWARD, Agent.Action.TURN_RIGHT]
#
#         else:
#             self.action_queue = [Agent.Action.FORWARD]
#
#     def choose_dir(self, current_dir, current_action=None):
#         if current_action == Agent.Action.TURN_LEFT or current_action == None:
#             if current_dir == (0, 1):
#                 return (-1, 0)
#             elif current_dir == (1, 0):
#                 return (0, 1)
#             elif current_dir == (0, -1):
#                 return (1, 0)
#             elif current_dir == (-1, 0):
#                 return (0, -1)
#         elif current_action == Agent.Action.TURN_RIGHT:
#             if current_dir == (0, 1):
#                 return (1, 0)
#             elif current_dir == (1, 0):
#                 return (0, -1)
#             elif current_dir == (0, -1):
#                 return (-1, 0)
#             elif current_dir == (-1, 0):
#                 return (0, 1)
#         # ======================================================================
#         # YOUR CODE ENDS
#         # ======================================================================
#
#     # ======================================================================
#     # YOUR CODE BEGINS
#     # ======================================================================
#
#
#
# class ActionType(MyAI):
#     def __init__(self, prev_pos, curr_pos, current_dir):
#         self.curr_dir = current_dir
#         self.r_dir = (-curr_pos[0]+prev_pos[0],-curr_pos[1]+prev_pos[1])
#     def undo_action(self):
#         print("undoing")
#         return_actions = []
#         return_actions.append(Agent.Action.FORWARD)
#         print("initial pos", self.curr_dir)
#         while self.curr_dir != self.r_dir:
#             self.curr_dir = self.choose_dir(self.curr_dir)
#             print("goal turn", self.r_dir,"currently faceing", self.curr_dir)
#             return_actions.append(Agent.Action.TURN_LEFT)
#         return return_actions
    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
