#include <numeric>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <vector>
#include <stdexcept>

struct Expansions {
  long size;
  std::vector<int> rows;
  std::vector<int> columns;

  Expansions(long size): size(size), rows(), columns() {}

  long extraSpaceBetweenColumns(int left, int right) {
    long result = 0;
    for (auto c: columns) {
      if (left < c && c < right) result += size;
    }
    return result;
  }

  long extraSpaceBetweenRows(int top, int bottom) {
    long result = 0;
    for (auto r: rows) {
      if (top < r && r < bottom) result += size;
    }
    return result;
  }
};

struct Galaxy {
  int x, y;
  Galaxy(): x(0), y(0) {}
  Galaxy(int x, int y): x(x), y(y) {}

  long distance(Galaxy& other, Expansions& expansions) {
    long dx = abs(x - other.x);
    long dy = abs(y - other.y);

    if (dx != 0) {
      int left = std::min(x, other.x);
      int right = std::max(x, other.x);
      dx += expansions.extraSpaceBetweenColumns(left, right);
    }

    if (dy != 0) {
      int top = std::min(y, other.y);
      int bottom = std::max(y, other.y);
      dy += expansions.extraSpaceBetweenRows(top, bottom);
    }

    return dx + dy;
  }
};


struct Grid {
  int width, height;
  std::vector<std::string> grid;

  Grid(): width(0), height(0), grid() {}

  void addRow(const std::string &row) {
    if (width > 0 && width != row.size()) {
      throw std::runtime_error("size of row doesn't match rest of grid");
    }

    grid.push_back(row);

    if (width <= 0) width = row.size();
    height += 1;
  }

  bool rowEmpty(int rowNum) {
    auto row = grid.at(rowNum);
    return std::all_of(row.begin(), row.end(), [](auto c) { return c == '.'; });
  }

  void duplicateRow(int rowNum) {
    std::string row = grid.at(rowNum);
    grid.insert(grid.begin() + rowNum, row);
    height += 1;
  }

  std::string column(int colNum) {
    std::string col;
    for (int i = 0; i < height; i++) {
      col += grid.at(i).at(colNum);
    }
    return col;
  }

  bool colEmpty(int colNum) {
    auto col = column(colNum);
    return std::all_of(col.begin(), col.end(), [](auto c) { return c == '.'; });
  }

  void duplicateCol(int colNum) {
    auto col = column(colNum);

    for (int i = 0; i < height; i++) {
      std::string &c = grid.at(i);
      c.insert(c.begin() + colNum, col.at(i));
    }

    width += 1;
  }

  Expansions expansions(long size) {
    Expansions result(size);
    for (int x = 0; x < width; x++) {
      if (colEmpty(x)) result.columns.push_back(x);
    }
    for (int y = 0; y < height; y++) {
      if (rowEmpty(y)) result.rows.push_back(y);
    }
    return result;
  }

  std::vector<Galaxy> galaxies() {
    std::vector<Galaxy> result;
    for (int y = 0; y < height; y++) {
      for (int x = 0; x < width; x++) {
        if (grid.at(y).at(x) == '#') {
          result.push_back({x, y});
        }
      }
    }
    return result;
  }
};

long sumShortestPaths(Grid grid, long expansionSize) {
  auto expansions = grid.expansions(expansionSize);
  auto galaxies = grid.galaxies();
  long sumOfPaths = 0;
  for (auto it = galaxies.begin(); it != galaxies.end() - 1; ++it) {
    sumOfPaths += std::accumulate(it + 1, galaxies.end(), 0L, [&](auto sum, auto& g) {
        return sum + g.distance(*it, expansions);
    });
  }
  return sumOfPaths;
}

int main(int argc, const char *argv[]) {
  if (argc != 2) {
    std::cerr << "expected 1 arg (path to input)" << std::endl;
    return 1;
  }

  Grid grid;

  std::ifstream input_file(argv[1]);
  std::string line;
  while (std::getline(input_file, line)) {
    grid.addRow(line);
  }

  std::cout << "[part 1] Sum of shortest paths: " << sumShortestPaths(grid, 1) << std::endl;
  std::cout << "[part 2] Sum of shortest paths: " << sumShortestPaths(grid, 999999) << std::endl;
}
