from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

goal  = ((1,2,3),
         (4,5,6),
         (7,8,0))

goal15 = (
         ('1', '2', '3', '4'),
         ('5', '6', '7', '8'),
         ('9', '10', '11','12'),
         ('13', '14', '15','0')
         )

goal  = (('1','2','3'),
         ('4','5','6'),
         ('7','8','0'))
blank_value = '0'

left = 0
right= 1
up   = 2
down = 3

#Function to find the row, column of an item in the grid
#usually called to find the position of the blank( 0 )
def find_position( board, item ):
    Nrows    = len(board)
    Ncolumns = len(board[0])
    for r in range(Nrows) :
        for c in range(Ncolumns):
            if board[r][c] == item :
                return r,c
    #some error
    return None
                
def move( board, action) :
    """move blank in the direction"""
    
    Nrows    = len(board)
    Ncolumns = len(board[0])
    
    board = [ list(row) for row in board ] #tuple to list; because we need to make a change. This will also make a copy
    
    
    #nor r,c is the position of zero
    z = find_position( board, blank_value)
    r,c = z
    
    if action == up :
        r,c = r-1, c  
    if action == down :
        r,c = r+1, c
    if action == right :
        r,c = r, c+1  
    if action == left :
        r,c = r, c-1
        
    #is it outside the grid?   
    if r < 0 or r >= Nrows or c < 0 or c >= Ncolumns :
        return None
    
    board[z[0]][z[1]] = board[r][c]
    board[r][c] = blank_value

    
    return tuple([ tuple(row) for row in board ]) #the incoming bord will not be modified

def successors( board ) :
    """ returns a list of next valid boards from this position"""
    #depends on the blank position we may have 2,3, or 4 next boards
    next_boards = []
    for direction in [up, left,right,down] :
        new = move(board, direction)
        if new is not None :
            next_boards.append( new )
    return next_boards

#A hacky way to create a random initial 8puzzle
import random
def shuffle_puzzle(goal, N=100) :
    for _ in range(N) :
        kids = successors( goal )
        goal = random.choice(kids)
    return goal


#########################################################################
# BFS - Breadth First Search
#########################################################################


# The parents dict has the format like { node: parent, .... start : None, ...}
#By following the back pointers up the parents chain we can reach start and thus extracting the path
def get_path(parents_dict, end):  
    """returns path from start to end. start is the one with parent as None"""
    path = []
    while end is not None :
        path.append( end )
        end = parents_dict[end]
        
    return list(reversed(path)) #we were building path from end to start, so reverse it


def bfs(start, goal) :
    """returns the path list of nodes from start to goal"""
    
    store   = [ start ]
    visited = { start: True } #dont care about order
    parents = { start: None } #we keep the back pointers here
    
    if start == goal :      
        return get_path(parents, goal)
    
    while store :
        #print ("-----------")
        #print ("visited:", visited)
        #print ("store:", store)
        
        board = store.pop(0) #pop(0) makes it bfs, pop() makes this dfs
        
        #print("pop:", board)
        #visited[ board ] = True
        
        for s in successors( board ) :
            if s not in visited: # and s not in store:
                parents[s] = board
                if s == goal :
                    print ("visited:", len(visited))
                    return get_path(parents, goal)
                
                visited[s] = True
                store.append( s )
                
                
        #print ("visited:", visited)
        #print ("store:", store)
        #print ("-----------")
    print ("visited:", len(visited))                        
    return [] #didnt find a path

#########################################################################
# A*
#########################################################################


# In[21]:


#we need a priority queue
#  This is a VERY BAD Priority Queue.
#We use it just for debugging.

#it returns the min number item
def priority_append(pq, item, priority) :
    pq[item] = priority #pq is just a dict
    
def priority_pop(pq) :
    min_priority = min(pq.values())
    for key in pq :
        if pq[key] == min_priority :
            pq.pop(key) #delete that item from queue
            return key, min_priority
    return None #impossible

def heuristic_simple( board, goal) :
    h = 0
    for i in range(9) :
        if board[i] == blank_value :
            continue
        if board[i] != goal[i] :
            h += 1
    return h

def heuristic( board, goal) :    
    Nrows    = len(board)
    Ncolumns = len(board[0])
    h = 0
    for r in range(Nrows) :
        for c in range(Ncolumns):
            if board[r][c] == blank_value :
                continue
            rg,cg = find_position(goal, board[r][c])
            h += (abs(rg-r) + abs(cg-c))
    return h
            

def greedy(start, goal) :
    """returns a set of boards from start to goal. Greedy is suboptimal"""
    
    store   = { start : heuristic(start,goal) } #store is a priority queue now
    #store = PQ()
    #priority_append(store, start, 0+heuristic(start,goal) )
    
    visited = { start: True }
    parents = { start: None } #we keep the bak pointers here
    
    while store :
        
        board, priority = priority_pop(store) 
        
        if board == goal :
            print ("visited:", len(visited))
            return get_path(parents, goal)
        
        #This must be here. Cannot be in the expansion time because of heuristics
        visited[board] = True
        
        for s in successors( board ) :
            if s not in visited : 
                #we need a check here              
                priority = heuristic(s, goal)
                if s not in store :                   
                    priority_append(store, s, priority )
                    parents[s] = board
                else :
                    #do we have a lesser priority one?
                    if priority < store[s] :
                        priority_append(store, s, priority )
                        parents[s] = board

    #print ("visited:", len(visited))           
    return []

def astar(start, goal) :
    """returns a set of boards from start to goal"""
    
    store   = { start : 0+heuristic(start,goal) } #store is a priority queue now
    #store = PQ()
    #priority_append(store, start, 0+heuristic(start,goal) )
    
    visited = { start: True }
    parents = { start: None } #we keep the bak pointers here
    
    while store :
        
        board, priority = priority_pop(store) 
        depth           = priority - heuristic(board, goal) #parent depth
        
        if board == goal :
            print ("visited:", len(visited))
            return get_path(parents, goal)
        
        #This must be here. Cannot be in the expansion time because of heuristics
        visited[board] = True
        
        for s in successors( board ) :
            if s not in visited : 
                #we need a check here              
                priority = depth + 1 + heuristic(s, goal)
                if s not in store :                   
                    priority_append(store, s, priority )
                    parents[s] = board
                else :
                    #do we have a lesser priority one?
                    if priority < store[s] :
                        priority_append(store, s, priority )
                        parents[s] = board

    #print ("visited:", len(visited))           
    return []


#hardest puzzle ref: http://w01fe.com/blog/2009/01/the-hardest-eight-puzzle-instances-take-31-moves-to-solve/

#start = ((8,6,7),(2,5,4),(3,0,1))
#start = ((6,4,7),(8,5,0),(3,2,1))


#x = bfs(start,goal)
#y = greedy(start,goal)
#z = astar(start, goal)
y = []



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

from fastapi import Request

@app.post("/start")
async def get_body(request: Request):
    request = await request.json()
    start = request['tiles']
    algo = request['algo']
    start = tuple( [tuple(row) for row in start] )
    if algo == 'greedy':
        y = greedy(start, goal)
    elif algo == 'bfs':
        y = bfs(start, goal)
    print('len y', len(y))
    return {"states": y}

@app.get("/")
def index():
    return {"greedy_states": y}

