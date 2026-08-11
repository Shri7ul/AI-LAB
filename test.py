# Name: Shriful Islam
# ID: 0112410115
# Heuristic: Manhattan distance is admissible because movement is limited
# to four directions and every move costs at least 1.


# Python-এর built-in heap module import করছি।
# A* এর priority queue / min-heap বানানোর জন্য heapq ব্যবহার করব।
import heapq


# Assignment যেই exact function signature চেয়েছে।
#
# grid  = city map
# start = starting position, যেমন (0, 0)
# goal  = destination position, যেমন (4, 7)
#
# Return করবে:
# (path, total_cost)
def astar(
    grid: list[str],
    start: tuple[int, int],
    goal: tuple[int, int]
) -> tuple[list[tuple[int, int]], int]:

    # ---------------------------------------------------------
    # HEURISTIC FUNCTION: h(n)
    # ---------------------------------------------------------

    # Manhattan distance admissible কারণ আমরা শুধু
    # up/down/left/right move করতে পারি এবং প্রতিটি move-এর
    # minimum cost 1।
    #
    # তাই Manhattan distance হলো goal-এ পৌঁছানোর minimum
    # number of moves, এবং এটি কখনো actual minimum cost-এর
    # চেয়ে বেশি হবে না।
    def heuristic(cell):

        # Current cell-এর row এবং column বের করছি।
        #
        # যেমন cell = (2, 3)
        # তাহলে r = 2, c = 3
        r, c = cell

        # Goal-এর row এবং column বের করছি।
        #
        # যেমন goal = (4, 7)
        # তাহলে gr = 4, gc = 7
        gr, gc = goal

        # Manhattan distance:
        #
        # |current_row - goal_row|
        # +
        # |current_col - goal_col|
        #
        # এটিই A* এর h(n)।
        return abs(r - gr) + abs(c - gc)


    # Grid-এ মোট কয়টা row আছে।
    #
    # যেমন:
    # [
    #   "S..",
    #   ".#.",
    #   "..G"
    # ]
    #
    # এখানে rows = 3
    rows = len(grid)


    # প্রথম row-এর length দিয়ে column সংখ্যা বের করছি।
    #
    # "S..#...." হলে cols = 8
    cols = len(grid[0])


    # ---------------------------------------------------------
    # PRIORITY QUEUE
    # ---------------------------------------------------------

    # A* যেসব node পরে explore করবে সেগুলো এখানে থাকবে।
    #
    # আমরা heap-এর মধ্যে রাখব:
    #
    # (f, g, position)
    #
    # যেখানে:
    # f = g + h
    # g = start থেকে current পর্যন্ত actual cost
    # position = current cell
    pq = []


    # ---------------------------------------------------------
    # g_score
    # ---------------------------------------------------------

    # প্রতিটি cell-এ start থেকে পৌঁছানোর সবচেয়ে কম
    # known cost এখানে রাখব।
    #
    # Start-এর cost 0।
    #
    # Example:
    # g_score[(0, 0)] = 0
    g_score = {start: 0}


    # ---------------------------------------------------------
    # came_from
    # ---------------------------------------------------------

    # কোন cell-এ কোন previous cell থেকে এসেছি
    # সেটা এখানে save করব।
    #
    # Example:
    # came_from[(1, 0)] = (0, 0)
    #
    # এর মানে (1,0)-এ আমরা (0,0) থেকে এসেছি।
    #
    # পরে এই dictionary ব্যবহার করে final path তৈরি করব।
    came_from = {}


    # Start থেকে goal পর্যন্ত heuristic calculate করছি।
    #
    # এটা h(start)।
    h = heuristic(start)


    # Start-কে priority queue-তে ঢুকাচ্ছি।
    #
    # (h, 0, start)
    #
    # এখানে:
    # f = h
    # g = 0
    # position = start
    #
    # কারণ start-এর g = 0,
    # তাই f = g + h = 0 + h = h
    heapq.heappush(pq, (h, 0, start))


    # ---------------------------------------------------------
    # POSSIBLE MOVEMENTS
    # ---------------------------------------------------------

    # Assignment অনুযায়ী শুধু 4 দিকে যাওয়া যাবে।
    #
    # (-1, 0) = Up
    # (1, 0)  = Down
    # (0, -1) = Left
    # (0, 1)  = Right
    #
    # Diagonal movement নেই।
    directions = [
        (-1, 0),   # Up
        (1, 0),    # Down
        (0, -1),   # Left
        (0, 1)     # Right
    ]


    # ---------------------------------------------------------
    # MAIN A* LOOP
    # ---------------------------------------------------------

    # যতক্ষণ priority queue-তে explore করার node আছে,
    # ততক্ষণ A* চলবে।
    while pq:

        # Priority queue থেকে সবচেয়ে ছোট f-এর node বের করছি।
        #
        # f         = g + h
        # current_g = current node-এর actual g
        # current   = current position
        #
        # heapq min-heap হওয়ায় সবচেয়ে ছোট f আগে বের হবে।
        f, current_g, current = heapq.heappop(pq)


        # -----------------------------------------------------
        # OUTDATED ENTRY CHECK
        # -----------------------------------------------------

        # একই node-এর জন্য আগে heap-এ একটি expensive path
        # ঢুকতে পারে, পরে cheaper path পাওয়া যেতে পারে।
        #
        # Example:
        # আগে g = 10 পাওয়া গিয়েছিল
        # পরে g = 6 পাওয়া গেল
        #
        # g_score-এ এখন 6 থাকবে।
        # পুরোনো g=10 entry heap থেকে বের হলে সেটা ignore করব।
        if current_g != g_score.get(current):
            continue


        # -----------------------------------------------------
        # GOAL CHECK
        # -----------------------------------------------------

        # যদি current node-ই goal হয়,
        # তাহলে আমরা destination-এ পৌঁছে গেছি।
        if current == goal:

            # Final path রাখার জন্য empty list।
            path = []


            # Goal থেকে backwards গিয়ে start পর্যন্ত যাব।
            node = goal


            # যতক্ষণ start-এ পৌঁছাইনি,
            # came_from ব্যবহার করে previous node বের করব।
            while node != start:

                # Current node path-এ যোগ করছি।
                path.append(node)

                # Current node-এর previous node বের করছি।
                #
                # Example:
                # came_from[G] = C
                # তাহলে G থেকে C-তে যাব।
                node = came_from[node]


            # Start-ও path-এর অংশ,
            # তাই শেষে start যোগ করছি।
            path.append(start)


            # এখন path উল্টো অবস্থায় আছে:
            #
            # G -> C -> B -> A -> S
            #
            # reverse করলে:
            #
            # S -> A -> B -> C -> G
            path.reverse()


            # Final path এবং goal পর্যন্ত actual total cost
            # return করছি।
            return path, current_g


        # -----------------------------------------------------
        # CURRENT POSITION
        # -----------------------------------------------------

        # Current position থেকে row এবং column আলাদা করছি।
        #
        # Example:
        # current = (2, 3)
        #
        # r = 2
        # c = 3
        r, c = current


        # -----------------------------------------------------
        # EXPLORE FOUR NEIGHBORS
        # -----------------------------------------------------

        # Up, Down, Left, Right—
        # চারটি possible movement একে একে check করছি।
        for dr, dc in directions:

            # নতুন neighbor-এর row বের করছি।
            nr = r + dr

            # নতুন neighbor-এর column বের করছি।
            nc = c + dc


            # -------------------------------------------------
            # GRID BOUNDARY CHECK
            # -------------------------------------------------

            # যদি নতুন position grid-এর বাইরে চলে যায়,
            # তাহলে সেটা valid movement না।
            #
            # তাই এই neighbor skip করছি।
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue


            # -------------------------------------------------
            # WALL CHECK
            # -------------------------------------------------

            # যদি neighbor '#' হয়,
            # তাহলে সেখানে যাওয়া যাবে না।
            if grid[nr][nc] == '#':
                continue


            # Valid neighbor-এর coordinate save করছি।
            neighbor = (nr, nc)


            # -------------------------------------------------
            # MOVEMENT COST
            # -------------------------------------------------

            # যদি rough terrain '~' হয়,
            # সেখানে ঢোকার cost = 3।
            if grid[nr][nc] == '~':
                move_cost = 3

            # Normal open cell '.' হলে
            # সেখানে ঢোকার cost = 1।
            else:
                move_cost = 1


            # -------------------------------------------------
            # NEW g(n)
            # -------------------------------------------------

            # Current পর্যন্ত আসতে current_g cost হয়েছে।
            # Neighbor-এ ঢুকতে move_cost লাগবে।
            #
            # তাই:
            #
            # new_g = current_g + move_cost
            #
            # এটিই neighbor-এর নতুন actual cost।
            new_g = current_g + move_cost


            # -------------------------------------------------
            # CHEAPER PATH CHECK
            # -------------------------------------------------

            # আমরা আগে neighbor-এ পৌঁছানোর কোনো cost জানি কি?
            #
            # যদি জানি এবং নতুন path-এর cost কম হয়,
            # তাহলে নতুন path better।
            #
            # যদি neighbor আগে কখনো না আসে,
            # g_score.get() infinity return করবে।
            if new_g < g_score.get(neighbor, float('inf')):


                # Neighbor-এর নতুন cheapest cost save করছি।
                g_score[neighbor] = new_g


                # Neighbor-এ আমরা current node থেকে এসেছি।
                #
                # পরে path reconstruction-এর সময়
                # এটা ব্যবহার করব।
                came_from[neighbor] = current


                # -------------------------------------------------
                # HEURISTIC h(n)
                # -------------------------------------------------

                # Neighbor থেকে goal পর্যন্ত Manhattan distance
                # calculate করছি।
                h = heuristic(neighbor)


                # -------------------------------------------------
                # A* COST f(n)
                # -------------------------------------------------

                # A* এর মূল formula:
                #
                # f(n) = g(n) + h(n)
                #
                # g = start থেকে এখানে আসার actual cost
                # h = goal পর্যন্ত estimated remaining cost
                f = new_g + h


                # নতুন node priority queue-তে ঢুকাচ্ছি।
                #
                # A* পরে সবচেয়ে ছোট f-এর node আগে explore করবে।
                heapq.heappush(pq, (f, new_g, neighbor))


    # ---------------------------------------------------------
    # NO PATH FOUND
    # ---------------------------------------------------------

    # Priority queue শেষ হয়ে গেছে,
    # কিন্তু goal পাওয়া যায়নি।
    #
    # অর্থাৎ start থেকে goal-এ যাওয়ার কোনো valid path নেই।
    return [], -1