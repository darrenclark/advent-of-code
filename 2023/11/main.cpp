#include <numeric>
#include <iostream>
#include <fstream>
#include <vector>
#include <stdexcept>

struct Galaxy {
  int x, y;
  Galaxy(): x(0), y(0) {}
  Galaxy(int x, int y): x(x), y(y) {}

  int distance(Galaxy& other) {
    int dx = abs(x - other.x);
    int dy = abs(y - other.y);

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

  // galaxy expansion
  for (int i = grid.height - 1; i >= 0; i--) {
    if (grid.rowEmpty(i)) grid.duplicateRow(i);
  }
  for (int i = grid.width - 1; i >= 0; i--) {
    if (grid.colEmpty(i)) grid.duplicateCol(i);
  }

  auto galaxies = grid.galaxies();
  int sumOfPaths = 0;
  for (auto it = galaxies.begin(); it != galaxies.end() - 1; ++it) {
    sumOfPaths += std::accumulate(it + 1, galaxies.end(), 0, [&](auto sum, auto& g) {
        return sum + g.distance(*it);
    });
  }

  std::cout << "[part 1] Sum of shortest paths: " << sumOfPaths << std::endl;
}
