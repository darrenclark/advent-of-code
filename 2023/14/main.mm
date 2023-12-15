#import <Foundation/Foundation.h>
#import <vector>
#import <string>

class Platform {
  std::vector<std::string> grid;

  using It = std::vector<std::string>::iterator;

public:
  void addRow(const std::string& row) {
    grid.push_back(row);
  }

  void tiltNorth() {
    for (auto rowIt = grid.begin() + 1; rowIt != grid.end(); ++rowIt) {
      for (auto colIt = rowIt->begin(); colIt != rowIt->end(); ++colIt) {
        if (*colIt == 'O') {
          size_t colIndex = colIt - rowIt->begin();
          auto destIt = findSlideDestination(rowIt - 1, colIndex);
          if (destIt != grid.end()) {
            NSLog(@"moving: %lu", colIndex);
            *colIt = '.';
            destIt->at(colIndex) = 'O';
          }
        }
      }
    }
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

  void print() {
    for (auto rowIt = grid.begin(); rowIt != grid.end(); ++rowIt) {
      NSLog(@"%s", rowIt->data());
    }
  }

private:
  It findSlideDestination(It rowIt, size_t colIndex) {
    It result = grid.end();

    for (; rowIt >= grid.begin(); --rowIt) {
      char c = rowIt->at(colIndex);
      NSLog(@"%c on %lu", c, (rowIt - grid.begin()));
      if (c == '.') {
        result = rowIt;
      } else {
        return result;
      }
    }

    return result;
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

  Platform p;

  NSLog(@"Input:");
  for (NSString *line in [fileContents componentsSeparatedByString:@"\n"]) {
    if (line.length > 0) {
      NSLog(@"%@", line);
      p.addRow(line.UTF8String);
    }
  }

  p.tiltNorth();
  NSLog(@"Tilted:");
  p.print();

  NSLog(@"[Part 1] Total load: %lu", p.calculateLoad());

  return 0;
}
