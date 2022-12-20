import fileinput


class Grid:
    grid: list[list[int]]
    width: int
    height: int

    def __init__(self, grid):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid[0])

    @classmethod
    def from_input(cls):
        grid = []

        for line in fileinput.input():
            row = [int(x) for x in list(line.strip())]
            grid.append(row)

        return Grid(grid)

    def count_visible(self):
        count = 0

        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.is_visible(x, y):
                    count += 1

        return count

    def is_visible(self, x, y):
        # edge trees always visible
        if x == 0 or x == self.width - 1:
            return True

        if y == 0 or y == self.height - 1:
            return True

        tree_height = self.grid[y][x]
        if tree_height > self.get_max_height_up(x, y):
            return True
        if tree_height > self.get_max_height_down(x, y):
            return True
        if tree_height > self.get_max_height_left(x, y):
            return True
        if tree_height > self.get_max_height_right(x, y):
            return True

        return False

    def get_max_height_up(self, x, y):
        return max([self.grid[vy][x] for vy in range(0, y)])

    def get_max_height_down(self, x, y):
        return max([self.grid[vy][x] for vy in range(y + 1, self.height)])

    def get_max_height_left(self, x, y):
        return max([self.grid[y][vx] for vx in range(0, x)])

    def get_max_height_right(self, x, y):
        return max([self.grid[y][vx] for vx in range(x + 1, self.width)])

    def max_scenic_score(self):
        valid_x = range(0, self.width)
        valid_y = range(0, self.height)

        return max([self.scenic_score(x, y) for y in valid_y for x in valid_x])

    def scenic_score(self, x, y):
        return (
            self.viewing_distance(x, y, 0, -1)
            * self.viewing_distance(x, y, 0, 1)
            * self.viewing_distance(x, y, -1, 0)
            * self.viewing_distance(x, y, 1, 0)
        )

    def viewing_distance(self, x, y, dx, dy):
        count = 0
        tree_height = self.grid[y][x]

        valid_x = range(0, self.width)
        valid_y = range(0, self.height)

        x += dx
        y += dy

        while x in valid_x and y in valid_y:
            th = self.grid[y][x]
            if th < tree_height:
                count += 1
            elif th >= tree_height:
                count += 1
                break

            x += dx
            y += dy

        return count


grid = Grid.from_input()

print("Visible (part 1): ", grid.count_visible())
print("Best Scenic Score (part 2): ", grid.max_scenic_score())
