
import threading

import time as time
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHTRED = (100, 0, 0)
GREEN = (0, 255, 0)
LIGHTGREEN = (0, 100, 0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)
LIGHTYELLOW = (100, 100, 0)
BROWN = (210, 105, 30)
finished = -1
started = False
# Define the maze grid
grid = np.array([
    [1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1],
    [1,1,0,0,1,1,2,2,1,1,1,1,0,0,0,1,1,0,0,0,1,1,1,1,1,1,1,1,0,0,1,1],
    [1,1,0,0,1,1,2,2,1,1,1,1,0,0,0,1,1,0,0,0,1,1,1,1,1,1,1,1,0,0,1,1],
    [1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,2,2,0,0,0,0,1,1],
    [1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,2,2,0,0,0,0,1,1],
    [1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0],
    [0,0,0,0,1,1,0,0,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1,1,0,0],
    [1,1,1,1,2,2,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,2,2,1,1,1,1],
    [1,1,1,1,2,2,1,1,1,1,0,0,1,1,0,0,0,0,1,1,0,0,1,1,1,1,2,2,1,1,1,1],
    [1,1,0,0,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,1,1],
    [1,1,0,0,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,1,1],
    [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,2,2,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,2,2,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
    [1,1,0,0,1,1,0,0,2,2,1,1,0,0,0,1,1,0,0,0,0,0,2,2,0,0,1,1,0,0,1,1],
    [1,1,0,0,1,1,0,0,2,2,1,1,0,0,0,1,1,0,0,0,0,0,2,2,0,0,1,1,0,0,1,1],
    [1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1]])
lights_touched = []

#cycle trough grid and print when the value is 2 the index
for row in range(len(grid)):
    for col in range(len(grid[row])):
        if grid[row,col] == 2:
            print(row,col)

positions_with_value_lights = {
 (2, 6): 0, (2, 7): 0,
 (3, 6): 0, (3, 7): 0,
 (4, 24): 1, (4, 25): 1,
 (5, 24): 1, (5, 25): 1,
 (10, 4): 2, (10, 5): 2,
 (10, 26): 3, (10, 27): 3,
 (11, 4): 2, (11, 5): 2,
 (11, 26): 3, (11, 27): 3,
 (14, 15): 4, (14, 16): 4,
 (15, 15): 4, (15, 16): 4,
 (16, 8): 5, (16, 9): 5,
 (16, 22): 6, (16, 23): 6,
 (17, 8): 5, (17, 9): 5,
 (17, 22): 6, (17, 23): 6
}

def addToList_if_light(x,y, current_tick):
  if (y,x) in positions_with_value_lights:
      lights_touched.append(Light(positions_with_value_lights[(y,x)], current_tick))

CELL_SIZE = 20
TIMOUT_TIME = 0.3
GRID_WIDTH = len(grid[0])
GRID_HEIGHT = len(grid)
WINDOW_SIZE = (GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE + 60)
seeker_size = CELL_SIZE * 3

class Seeker:
    def __init__(self,x,y,id):
        self.x = x
        self.y = y
        self.id = id
    
    def to_json(self):
        return {"x": self.x, "y": self.y, "id": self.id}

class RunnerHazel:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_json(self):
        return {"x": self.x, "y": self.y}

class Light:
    def __init__(self, id, tick):
        self.id = id
        self.tick = tick

    def to_json(self):
        return {"id": self.id, "tick": self.tick}

class GameState:
    def __init__(self):
        self.startTime = int(round(time.time() * 1000))
        self.lastTickTime = int(round(time.time() * 1000))
        self.currentTick = 0
        self.seekerHasMadeTurn = False
        self.runnerHasMadeTurn = False
        self.seekerHasJoined = False
        self.runnerHasJoined = False
        self.lastSeeker1Move = (0, 0)
        self.lastSeeker2Move = (0,0)
        self.lastSeeker3Move = (0,0)
        self.lastRunnerMove = (0,0)

gameState = GameState()

def isLegalMove(x_direction, y_direction, currentX, currentY):
    if abs(x_direction) == 1 and abs(y_direction) == 1:
        return False
    lenght, width = grid.shape
    if currentX + x_direction >= width or currentY + y_direction >= lenght:
        return False
    if grid[currentY+y_direction, currentX + x_direction] == 0:
        return False
    return True

def canDrawSquareSeeker(x_direction, y_direction, currentX, currentY):
    lenght, width = grid.shape
    if currentX + x_direction >= width or currentY + y_direction >= lenght:
        return False
    if grid[currentY+y_direction, currentX + x_direction] == 0:
        return False
    return True 
    
# Example usage
seeker1 = Seeker(x=10, y=0, id=0)
seeker2 = Seeker(x=15, y=0, id=1)
seeker3 = Seeker(x=21, y=0, id=2)

runner = RunnerHazel(15, 19)
seekers_list = [seeker1, seeker2, seeker3]


@app.route('/seekers/status', methods=['GET'])
def get_status_seeker():
    if not started:
        gameState.seekerHasJoined = True
        return jsonify(wait=-1),400
    if gameState.seekerHasMadeTurn and finished == 0:
        currTime = int(round(time.time() * 1000))
        tillNextMove = TIMOUT_TIME - (currTime-gameState.lastTickTime) / 1000
        return jsonify(wait=tillNextMove), 400
    seekers_data = [seeker.to_json() for seeker in seekers_list]
    lights_data = [light.to_json() for light in lights_touched]
    return jsonify(seekers=seekers_data, lights=lights_data, finished=finished, current_tick=gameState.currentTick), 200

@app.route('/runner/status', methods=['GET'])
def get_status_runner():
    if not started:
        gameState.runnerHasJoined = True
        return jsonify(wait=-1),400
    if gameState.runnerHasMadeTurn and finished == 0:
        currTime = int(round(time.time() * 1000))
        tillNextMove = TIMOUT_TIME - (currTime-gameState.lastTickTime) / 1000
        return jsonify(wait=tillNextMove), 400
    seekers_data = [seeker.to_json() for seeker in seekers_list]
    lights_data = [light.to_json() for light in lights_touched]
    runner_data = runner.to_json()
    return jsonify(runner = runner_data, seekers=seekers_data, lights=lights_data, finished=finished, current_tick=gameState.currentTick), 200

# Route for POST /move-seekers
@app.route('/seekers/move', methods=['POST'])
def move_seekers():
    if not started or finished:
        return jsonify(error="Not started"),500 
    if gameState.seekerHasMadeTurn:
        return jsonify(error="Already made turn"), 500
    #parse the data coming from the request
    data = request.get_json()
    if "seekers" in data:
        seekers_array = data['seekers']
        for seeker in seekers_array:
            x_direction = seeker['x_direction']
            y_direction = seeker['y_direction']
            seeker_id = seeker['id']
            seeker = None
            if seeker_id == 0:
                seeker = seeker1
            if seeker_id == 1:
                seeker = seeker2
            if seeker_id == 2:
                seeker = seeker3
            if isLegalMove(x_direction, y_direction, seeker.x, seeker.y):
                if seeker_id == 0:
                    gameState.lastSeeker1Move = (x_direction, y_direction)
                if seeker_id == 1:
                    gameState.lastSeeker2Move = (x_direction, y_direction)
                if seeker_id == 2:
                    gameState.lastSeeker3Move = (x_direction, y_direction)
                gameState.seekerHasMadeTurn = True
            else:
                return jsonify("Illegal Move"),500
    else:
        return jsonify("Wrong Json be ashamed of yourself"),500
    return jsonify(OK= "Ok"),200

# Route for POST /move-runner
@app.route('/runner/move', methods=['POST'])
def move_runner():
    if not started or finished:
        return jsonify(error="Not started"), 500
    if gameState.runnerHasMadeTurn:
        return jsonify(error="Has already made turn"),500
    #parse the data coming from the request
    data = request.get_json()
    if "runner" in data:
        x_direction_runner = data['runner']['x_direction']
        y_direction_runner = data['runner']['y_direction']
        if isLegalMove(x_direction_runner, y_direction_runner, runner.x, runner.y):
            gameState.lastRunnerMove = (x_direction_runner, y_direction_runner)
            gameState.runnerHasMadeTurn = True
        else:
            return jsonify("Illegal Move"),500
    else:
        return jsonify("Wrong json"),500
    return jsonify("ok"), 200

def run_flask():
    app.run(host='0.0.0.0',debug=False)

def start_Game():
    global started, gameState, finished
    started = True
    gameState.startTime = int(round(time.time() * 1000))
    gameState.lastTickTime = int(round(time.time() * 1000))
    finished = 0

def update_Game():
    global started
    global gameState
    global finished
    currTime = int(round(time.time() * 1000))  
    if not started or finished:
        if gameState.seekerHasJoined and gameState.runnerHasJoined:
            start_Game()
        return
    if (currTime-gameState.lastTickTime) / 1000 < TIMOUT_TIME:
        return
    if gameState.currentTick*TIMOUT_TIME >= 20:
        print("Finished!!! Time is up")
        finished = 2
        return
    #update Game:
    if gameState.seekerHasMadeTurn:
        seeker1.x += gameState.lastSeeker1Move[0]
        seeker1.y += gameState.lastSeeker1Move[1]
        seeker2.x += gameState.lastSeeker2Move[0]
        seeker2.y += gameState.lastSeeker2Move[1]
        seeker3.x += gameState.lastSeeker3Move[0]
        seeker3.y += gameState.lastSeeker3Move[1]

    if gameState.runnerHasMadeTurn:
        runner.x += gameState.lastRunnerMove[0]
        runner.y += gameState.lastRunnerMove[1]

    addToList_if_light(runner.x, runner.y, gameState.currentTick)

    distance1 = np.sqrt((runner.x - seeker1.x)**2 + (runner.y - seeker1.y)**2)
    distance2 = np.sqrt((runner.x - seeker2.x)**2 + (runner.y - seeker2.y)**2)
    distance3 = np.sqrt((runner.x - seeker3.x)**2 + (runner.y - seeker3.y)**2)
    if distance1 <= 2 or distance2 <= 2 or distance3 <= 2:
        print("Finished!!!!")
        finished = 1
        return

    gameState.runnerHasMadeTurn = False
    gameState.seekerHasMadeTurn = False
    gameState.lastTickTime = int(round(time.time() * 1000))
    gameState.currentTick += 1

# def draw_seeker(pos_x, pos_y, color, lightcolor, screen):
#     pygame.draw.rect(screen, color, (pos_x * CELL_SIZE, pos_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
#     if canDrawSquareSeeker(0,1,pos_x,pos_y):
#         pygame.draw.rect(screen, lightcolor, (pos_x * CELL_SIZE, (pos_y+1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
#     if canDrawSquareSeeker(0,-1,pos_x,pos_y):
#         pygame.draw.rect(screen, lightcolor, (pos_x * CELL_SIZE, (pos_y-1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
#     if canDrawSquareSeeker(1,0,pos_x,pos_y):
#         pygame.draw.rect(screen, lightcolor, ((pos_x+1) * CELL_SIZE, pos_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
#     if canDrawSquareSeeker(-1,0,pos_x,pos_y):
#         pygame.draw.rect(screen, lightcolor, ((pos_x-1) * CELL_SIZE, pos_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
#     if canDrawSquareSeeker(1,1,pos_x,pos_y):
#         pygame.draw.rect(screen, lightcolor, ((pos_x+1) * CELL_SIZE, (pos_y+1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
#     if canDrawSquareSeeker(-1,-1,pos_x,pos_y):
#         pygame.draw.rect(screen, lightcolor, ((pos_x-1) * CELL_SIZE, (pos_y-1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
#     if canDrawSquareSeeker(1,-1,pos_x,pos_y):
#         pygame.draw.rect(screen, lightcolor, ((pos_x+1) * CELL_SIZE, (pos_y-1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
#     if canDrawSquareSeeker(-1,1,pos_x,pos_y):
#         pygame.draw.rect(screen, lightcolor, ((pos_x-1) * CELL_SIZE, (pos_y+1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def run_game():
    # Main game loop
    running = True
    while running:
        update_Game()
        # Define UI elements
        timeLeft = 20 - gameState.currentTick * TIMOUT_TIME
        timeLeft = round(timeLeft, 1)
        if(timeLeft < 0):
            timeLeft = 0

if __name__ == '__main__':
    # run_flask()
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # # Start Pygame in the main thread
    run_game()

    # # Wait for the Flask thread to finish
    flask_thread.join()

