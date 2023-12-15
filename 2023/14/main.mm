#import <Foundation/Foundation.h>
#import <vector>
#import <string>
#import <utility>
#import <optional>
#import <unordered_map>

class Platform {
  std::vector<std::string> grid;
  int width;

public:
  void addRow(const std::string& row) {
    if (width == 0) width = row.size();
    grid.push_back(row);
  }

  void tilt(int dx, int dy) {
    if (dy == -1) {
      // north
      for (long row = 1; row < grid.size(); row++) {
        for (long col = 0; col < grid[row].size(); col++) {
          char c = grid[row][col];
          if (c == 'O') {
            auto dest = findSlideDestination(col, row, dx, dy);
            if (dest.has_value()) {
              grid[row][col] = '.';
              grid[dest->second][dest->first] = 'O';
            }
          }
        }
      }
    } else if (dy == 1) {
      // south
      for (long row = grid.size() - 2; row >= 0; row--) {
        for (long col = 0; col < grid[row].size(); col++) {
          char c = grid[row][col];
          if (c == 'O') {
            auto dest = findSlideDestination(col, row, dx, dy);
            if (dest.has_value()) {
              grid[row][col] = '.';
              grid[dest->second][dest->first] = 'O';
            }
          }
        }
      }
    } else if (dx == -1) {
      // west
      for (long row = 0; row < grid.size(); row++) {
        for (long col = 1; col < grid[row].size(); col++) {
          char c = grid[row][col];
          if (c == 'O') {
            auto dest = findSlideDestination(col, row, dx, dy);
            if (dest.has_value()) {
              grid[row][col] = '.';
              grid[dest->second][dest->first] = 'O';
            }
          }
        }
      }
    } else if (dx == 1) {
      // east
      for (long row = 0; row < grid.size(); row++) {
        for (long col = grid[row].size() - 2; col >= 0; col--) {
          char c = grid[row][col];
          if (c == 'O') {
            auto dest = findSlideDestination(col, row, dx, dy);
            if (dest.has_value()) {
              grid[row][col] = '.';
              grid[dest->second][dest->first] = 'O';
            }
          }
        }
      }
    }
  }

  long calculateLoadOnCycleN(long n) {
    std::unordered_map<std::string, bool> seenPositions;
    long i = 0;

    while (!seenPosition(seenPositions)) {
      cycle(1);
      i += 1;
    }

    long firstRepeat = i;

    i = 0;
    seenPositions.clear();

    while (!seenPosition(seenPositions)) {
      cycle(1);
      i += 1;
    }

    long period = i;

    // "jump" to position as if we were on cycle 'n'
    long moreCycles = (n - firstRepeat) % period;
    cycle(moreCycles);

    return calculateLoad();
  }

  long calculateLoad() {
    long load = 0;
    for (auto rowIt = grid.rbegin(); rowIt != grid.rend(); ++rowIt) {
      long loadPerRock = rowIt - grid.rbegin() + 1;
      for (auto colIt = rowIt->begin(); colIt != rowIt->end(); ++colIt) {
        if (*colIt == 'O') load += loadPerRock;
      }
    }
    return load;
  }

private:
  std::optional<std::pair<long, long>> findSlideDestination(long x, long y, int dx, int dy) {
    std::optional<std::pair<long, long>> result = std::nullopt;

    x += dx;
    y += dy;

    while (x >= 0 && x < width && y >= 0 && y < grid.size()) {
      if (grid[y][x] == '.') {
        result = std::make_pair(x, y);
      } else {
        break;
      }

      x += dx;
      y += dy;
    }

    return result;
  }

  void cycle(long nTimes) {
    for (long i = 0; i < nTimes; i++) {
      tilt(0, -1);
      tilt(-1, 0);
      tilt(0, 1);
      tilt(1, 0);
    }
  }

  bool seenPosition(std::unordered_map<std::string, bool>& seenPositions) {
    auto pos = position();
    auto it = seenPositions.find(pos);
    if (it != seenPositions.end()) {
      return true;
    } else {
      seenPositions[pos] = true;
      return false;
    }
  }

  std::string position() {
    std::string s;
    s.reserve(grid.size() * width);
    for (auto& row : grid)
      s.append(row);
    return s;
  }
};

int main(int argc, char *argv[]) {
  if (argc != 2) {
    NSLog(@"Expected one argument: input_file.txt");
    return 1;
  }

  NSString *inputFile = [NSString stringWithUTF8String:argv[1]];
  NSError *error;
  NSString *fileContents =
      [NSString stringWithContentsOfFile:inputFile
                                encoding:NSUTF8StringEncoding
                                   error:&error];

  if (fileContents == nil) {
    NSLog(@"Failed to read file: %@", error);
    return 1;
  }

  Platform platform;

  for (NSString *line in [fileContents componentsSeparatedByString:@"\n"]) {
    if (line.length > 0) {
      platform.addRow(line.UTF8String);
    }
  }

  Platform platformPart1 = platform;
  platformPart1.tilt(0, -1);
  NSLog(@"[Part 1] Total load after sliding north: %lu", platformPart1.calculateLoad());

  Platform platformPart2 = platform;
  long targetCycles = 1000000000;
  NSLog(@"[Part 2] Total load on cycle %ld: %lu", targetCycles, platformPart2.calculateLoadOnCycleN(targetCycles));

  return 0;
}
