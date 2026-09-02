import heapq

def astar(grid:list[str],start:tuple[int,int],goal:tuple[int,int])->tuple[list[tuple[int,int]],int]:

    def heuristic(cell):
        r,c=cell
        gr,gc=goal

        return abs(r-gr)+abs(c-gc)

    rows = len(grid)
    cols = len(grid[0])

    pq=[]

    g_score = {start:0}

    came_from = {}

    h=heuristic(start)

    heapq.heappush(pq,(h,0,start))

    direction =[
        (-1,0),
        (1,0),
        (0,-1),
        (0,1)
    ]

    while pq:

        f,current_g,current = heapq.heappop(pq)

        if current_g != g_score.get(current):
            continue

        if current == goal:

            path =[]

            node = goal

            while node != start:

                path.append(node)

                node = came_from[node]

            path.append(start)

            path.reverse()

            return path , current_g

        r , c =current

        for dr , dc in direction :

            nr = r+dr

            nc = c+dc

            if not (0<=nr<rows and 0<= nc <cols):
                continue

            if grid [nr][nc] == '#':
                continue

            neighbor =(nr,nc)

            if grid[nr][nc] == '~':
                move_cost = 3

            else:
                move_cost = 1

                
                            