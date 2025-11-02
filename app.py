from flask import Flask, render_template, request, jsonify
import heapq
import numpy as np

app = Flask(__name__)

GRID_SIZE = (10, 10)
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def is_valid_move(grid, pos):
    x, y = pos
    return 0 <= x < GRID_SIZE[0] and 0 <= y < GRID_SIZE[1] and grid[x][y] != -1

def a_star(grid, start, goal):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = [(0, start, [start])]
    heapq.heapify(open_set)
    visited = set()
    
    while open_set:
        cost, (x, y), path = heapq.heappop(open_set)
        if (x, y) == goal:
            return path
        
        for dx, dy in DIRECTIONS:
            next_pos = (x + dx, y + dy)
            if next_pos not in visited and is_valid_move(grid, next_pos):
                visited.add(next_pos)
                new_cost = len(path) + heuristic(next_pos, goal)
                heapq.heappush(open_set, (new_cost, next_pos, path + [next_pos]))

    return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_path', methods=['POST'])
def find_path():
    data = request.json
    grid = np.array(data['grid'])
    start = tuple(data['start'])
    goal = tuple(data['goal'])

    path = a_star(grid, start, goal)
    return jsonify({'path': path})

if __name__ == '__main__':
    app.run(debug=True)
