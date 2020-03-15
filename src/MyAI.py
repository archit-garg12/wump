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
        if self.wumpus_dead:
            stench = False
        if self.last_action == Agent.Action.FORWARD:

            self.visited_positions.add(self.current_position)
            if (breeze or stench) and self.current_position == (1,1):
                return Agent.Action.CLIMB
                
            if self.current_position == (1,1) and (self.has_gold or self.getUnvisitedAdjacentPositions() == set()):
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
            elif not breeze and not stench and not glitter and not self.has_gold:
                for position in self.getUnvisitedAdjacentPositions():
                    self.position_stack.append(self.current_position)
                    self.position_stack.append(position)
            next_position = self.position_stack.pop()
            while self.current_position == next_position or next_position[0] > self.max_x or next_position[1] > self.max_y:
                next_position = self.position_stack.pop()
            self.queuePosition(next_position, Agent.Action.FORWARD)
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
        self.last_action = self.action_queue.pop(0)
        return self.last_action

    def queuePosition(self, new_position, endAction):
        turns = self.getTurns( (new_position[0] - self.current_position[0], new_position[1] - self.current_position[1]) )
        self.current_direction = (new_position[0] - self.current_position[0], new_position[1] - self.current_position[1])
        self.action_queue = turns + self.action_queue
        self.action_queue.insert(len(turns), endAction)
        if self.wumpus_dead != True and len(self.wumpus_position) != 0:
            self.action_queue.insert(len(turns), Agent.Action.SHOOT)

    def getTurns(self, new_direction):
        turns = []
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
                
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
