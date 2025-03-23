maze = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
start_x, start_y = int(len(maze[0])/2), len(maze)-1
end_x, end_y = int(len(maze[0])/2), 0

original_path = [9, 8, 9, 6, 7, 4, 7, 6, 1, 0, 1, 6, 7, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 9, 8, 11, 10, 5, 4, 5, 2, 3, 0, 3, 2, 5, 4, 7, 6, 1, 0, 3, 2, 29, 28, 31, 30, 1, 0, 1, 30, 31, 28, 29, 26, 27, 24]

def check_path(player_x, player_y, path, seen_array):
    if (player_x, player_y) not in seen_array:
        seen_array.append((player_x, player_y))
        if path:
            if player_x ^ player_y != path.pop():
                return False
        return True
    return False


def get_availables_moves(player_x, player_y):
    moves = []
    if player_y > 0 and maze[player_y - 1][player_x] == 1:
        moves.append("Top")
    if player_y + 1 < len(maze) and maze[player_y + 1][player_x] == 1:
        moves.append("Bottom")
    if player_x > 0 and maze[player_y][player_x - 1] == 1:
        moves.append("Left")
    if player_x + 1 < len(maze[0]) and maze[player_y][player_x + 1] == 1:
        moves.append("Right")
    return moves


def get_good_moves(player_x, player_y, path, seen_array=[], directions=[]):
    moves = get_availables_moves(player_x, player_y)
    print(f"({player_x}:{player_y}), availables : {moves}")

    for move in moves:
        new_player_x, new_player_y = player_x, player_y
        if move == "Top":
            new_player_y -= 1
        if move == "Bottom":
            new_player_y += 1
        if move == "Left":
            new_player_x -= 1
        if move == "Right":
            new_player_x += 1

        cur_path = path.copy()
        cur_seen_array = seen_array.copy()

        if check_path(new_player_x, new_player_y, cur_path, cur_seen_array):
            print(f"({new_player_x};{new_player_y}) good move")

            if (new_player_x, new_player_y) not in cur_seen_array:
                cur_seen_array.append((new_player_x, new_player_y))

            if new_player_x == end_x and new_player_y == end_y:
                print("[+] Found path")
                print(directions)
                exit()
            get_good_moves(
                new_player_x,
                new_player_y,
                cur_path,
                cur_seen_array,
                directions + [move],
            )


get_good_moves(start_x, start_y, original_path)
