import sys, math, copy


class MDP:

    def __init__(self, board, policy, walls, end_states, step_reward, start):
        self.board = board
        self.walls = walls
        self.start = start
        self.old_board = copy.deepcopy(self.board)
        self.end_states = end_states
        self.policy =policy
        self.probability = {
        'target' : 0.8,
        'alt':     0.1,
        }
        self.delta = 0.85
        self.step_reward = step_reward
        self.noop_states = copy.deepcopy(self.end_states)
        self.init_board()
        self.init_policy()
        self.value_iteration()

    def init_board(self):
        """Initializing the board with the walls. Replacing walls with NaN."""
        for i in range(len(self.walls)):
            x, y = self.walls[i]
            self.board[x][y] =  None
            self.policy[x][y] = None
            self.noop_states.append(walls[i])

    def init_policy(self):
        """Initializing policy for the board."""
        for i in range(len(self.end_states)):
            x, y = self.end_states[i]
            print self.board[x][y]
            if self.board[x][y] > 0:
                self.policy[x][y] = "Goal"
            else:
                self.policy[x][y] = "Bad"

    def value_iteration(self):
        i = 0
        while True:
            i += 1
            print ('\n')
            print ('\n')
            print('_' * 80)


            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    if (row, col) in self.noop_states:
                        continue

                    print('Iteration %d' % int(i + 1))
                    print('Estimating S(%d,%d)' % (row, col))
                    self.board[row][col] = self.bellman_update((row, col))

                    self.print_board(decimal_places=4)

            #Before updating the previous board to reflect the new board changes, we need to check for diff and if diff < delta
            #How do we do that? Trying to implement...
            list = []
            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    if (row, col) in self.noop_states:
                        continue

                    list.append((self.board[row][col] - self.old_board[row][col]))

            print "List for utility change: "
            print list


            print "Change of utility's max = " + str(max(list))

            i = max(list)
            print i
            for j in range(len(list)):
                if (i == list[j]):
                    print "coords of max utility change is "
                    print j

            if (max(list) < self.delta):
                #print list
                print ('-'*150)
                print "END OF ITERATIONS"
                print ('-'*150)
                print ('\n')
                print ('\n')

                self.policy_formation()
                return


            #Update the previous board to the new board
            #print self.old_board
            #print self.board

            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    if (row, col) in self.noop_states:
                        continue
                    self.old_board[row][col] = self.board[row][col]

    def policy_formation(self):

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if (row, col) in self.noop_states:
                    continue
                print('Estimating S(%d,%d)' % (row, col))
                self.policy[row][col] = self.policy_update((row, col))
                 #Print the policy
                self.print_policy()
        return




    def policy_update(self, state_coords):
        r, c = state_coords

        e_coords = (r, c + 1)
        s_coords = (r + 1, c)
        w_coords = (r, c - 1)
        n_coords = (r - 1, c)

        e_util = self.get_utility_of_policy(self.board[r][c], e_coords)
        s_util = self.get_utility_of_policy(self.board[r][c], s_coords)
        w_util = self.get_utility_of_policy(self.board[r][c], w_coords)
        n_util = self.get_utility_of_policy(self.board[r][c], n_coords)


        #print('e_util%s = %f' % (e_coords, e_util))
        #print('s_util%s = %f' % (s_coords, s_util))
        #print('w_util%s = %f' % (w_coords, w_util))
        #print('n_util%s = %f' % (n_coords, n_util))

        # print 'E: '
        e_value = self.value_function(e_util, n_util, s_util, w_util)
        print('e_value%s = %f' % (e_coords, self.step_reward+ e_value))
        print  'S: '
        s_value = self.value_function(s_util, e_util, w_util, n_util)
        print('s_value%s = %f' % (s_coords, self.step_reward+s_value))
        print 'W: '
        w_value = self.value_function(w_util, s_util, n_util, e_util)
        print('w_value%s = %f' % (w_coords, self.step_reward+w_value))
        print 'N: '
        n_value = self.value_function(n_util, w_util, e_util, s_util)
        print('n_value%s = %f' % (n_coords, self.step_reward+n_value))

        print ('\n')
        print 'MAX IS : ' + str(max(self.step_reward+e_value, self.step_reward+s_value, self.step_reward+w_value, self.step_reward+n_value))
        xd =  (self.step_reward) + max(e_value, s_value, w_value, n_value)
        print 'Total utility for this state: ' #+ (self.step_reward) + ' ' + '+' +' '+ (self.discount_factor)+ ' '+ '*'+ ' '+ 'max( '+e_value+' '+s_val
        print xd

        #Finally, return the appropriate letter to be filled

        if (e_value == max(e_value, s_value, w_value, n_value) ):
            return "E"
        elif (s_value == max(e_value, s_value, w_value, n_value) ):
            return "S"
        elif (w_value == max(e_value, s_value, w_value, n_value) ):
            return "W"
        elif (n_value == max(e_value, s_value, w_value, n_value)):
            return "N"

    def bellman_update(self, state_coords):
        r, c = state_coords

        e_coords = (r, c + 1)
        s_coords = (r + 1, c)
        w_coords = (r, c - 1)
        n_coords = (r - 1, c)

        e_util = self.get_utility_of_state(self.old_board[r][c], e_coords)
        s_util = self.get_utility_of_state(self.old_board[r][c], s_coords)
        w_util = self.get_utility_of_state(self.old_board[r][c], w_coords)
        n_util = self.get_utility_of_state(self.old_board[r][c], n_coords)

        print('own_value%s = %d' % ((r, c), self.board[r][c]))
        #print('e_util%s = %f' % (e_coords, e_util))
        #print('s_util%s = %f' % (s_coords, s_util))
        #print('w_util%s = %f' % (w_coords, w_util))
        #print('n_util%s = %f' % (n_coords, n_util))

        print 'E: '
        e_value = self.value_function(e_util, n_util, s_util, w_util)
        print('e_value%s = %f' % (e_coords, self.step_reward+ e_value))
        print  'S: '
        s_value = self.value_function(s_util, e_util, w_util, n_util)
        print('s_value%s = %f' % (s_coords, self.step_reward+s_value))
        print 'W: '
        w_value = self.value_function(w_util, s_util, n_util, e_util)
        print('w_value%s = %f' % (w_coords, self.step_reward+w_value))
        print 'N: '
        n_value = self.value_function(n_util, w_util, e_util, s_util)
        print('n_value%s = %f' % (n_coords, self.step_reward+n_value))

        print ('\n')
        print 'MAX IS : ' + str(max(self.step_reward+e_value, self.step_reward+s_value, self.step_reward+w_value, self.step_reward+n_value))




        xx =  (self.step_reward) +  max(e_value, s_value, w_value, n_value)
        print 'Total utility for this state: ' #+ (self.step_reward) + ' ' + '+' +' '+ (self.discount_factor)+ ' '+ '*'+ ' '+ 'max( '+e_value+' '+s_val
        print xx
        return xx
    def get_utility_of_state(self, own_value, target_coords):
        row, col = target_coords

        if row < 0 or col < 0:
            print('Bumping against a wall in S(%d,%d)' % (row, col))
            return own_value

        try:
            value = self.old_board[row][col] or own_value
        except IndexError:
            print('Bumping against a wall in S(%d,%d)' % (row, col))
            value = own_value
        return float(value)


    def get_utility_of_policy(self, own_value, target_coords):
        row, col = target_coords

        if row < 0 or col < 0:
            print('Bumping against a wall in S(%d,%d)' % (row, col))
            return own_value

        try:
            value = self.board[row][col] or own_value
        except IndexError:
            print('Bumping against a wall in S(%d,%d)' % (row, col))
            value = own_value
        return float(value)


    def value_function(self, target, left=0, right=0, back=0):
        xy = float(self.probability['target'] * target + \
            self.probability['alt'] * left + \
            self.probability['alt'] * right +\
            self.probability['alt'] * back)

        print "-0.85 + " +str(self.probability['target']) + str("*(")+ str(target)+str(") + ") +str(self.probability['alt']) + str("*(")+str(left)+str(") + ")+str(self.probability['alt']) + str("*(")+str(right)+str(") ")
        return xy

    def print_board(self, decimal_places=0):
        for row in range(len(self.board)):
            print('-' * 70)
            sys.stdout.write(str(row))
            for col in range(len(self.board[row])):
                val = self.board[row][col]
                if type(val) == float:
                    val = round(val, decimal_places)
                sys.stdout.write(' | %14s' % val)
            print('|')
        print('-' * 70)

    def print_policy(self):
        for row in range(len(self.policy)):
            print('-' * 70)
            sys.stdout.write(str(row))
            for col in range(len(self.policy[row])):
                sys.stdout.write(' | %14s' % self.policy[row][col])
            print('|')
        print('-' * 70)


if __name__ == '__main__':

    # Taking input for size of board
    inp = raw_input()
    inp = inp.split()
    n = int(inp[0])
    m = int(inp[1])

    # Initializing board with 0
    board = [[0 for i in range(m)] for j in range(n)]

    # Initializing policy
    policy = [["n/a" for i in range(m)] for j in range(n)]

    # Taking row wise input
    for i in range(n):
        rows = raw_input()
        rows = rows.split()
        for j in range(m):
            board[i][j] = float(rows[j])

    # Taking input for e and w, number of end states and number of walls
    inp = raw_input()
    inp = inp.split()
    e = int(inp[0])
    w = int(inp[1])

    # Initializing end states and walls arrays
    end_states = []
    walls = []

    # Taking input for all end states
    for i in range(e):
        inp = raw_input()
        inp = inp.split()
        end_states.append(tuple((int(inp[0]), int(inp[1]))))

    # Taking input for all walls
    for i in range(w):
        inp = raw_input()
        inp = inp.split()
        walls.append(tuple((int(inp[0]), int(inp[1]))))

    # Taking input for start state
    inp = raw_input()
    inp = inp.split()

    start = tuple((inp[0], inp[1]))

    # Taking input for unit step reward
    unit_step_reward = float(raw_input())

    # Creating class object and beginning value iteration
    m = MDP(board, policy, walls, end_states, unit_step_reward, start)
