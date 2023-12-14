#import <Foundation/Foundation.h>

@interface Solver: NSObject

@property (nonatomic, strong) NSString *conditionRecord;
@property (nonatomic, strong) NSArray<NSNumber *> *contiguousGroups;

@end

@implementation Solver

- (instancetype)initWithConditionRecord:(NSString *)conditionRecord contiguousGroups:(NSArray<NSNumber *> *)contiguousGroups {
  if (self = [super init]) {
    _conditionRecord = conditionRecord;
    _contiguousGroups = contiguousGroups;
  }
  return self;
}

- (int)countPossibleSolutions {
  NSMutableString *solution = [self.conditionRecord mutableCopy];

  return [self countPossibleSolutions:solution fromIndex:0];
}

- (int)countPossibleSolutions:(NSMutableString *)solution fromIndex:(NSUInteger)index {
  if (index == solution.length) {
    return [self isValid:solution] ? 1 : 0;
  } else if ([self.conditionRecord characterAtIndex:index] == '?') {
    int result = 0;

    [solution replaceCharactersInRange:NSMakeRange(index, 1) withString:@"."];
    result += [self countPossibleSolutions:solution fromIndex:index + 1];

    [solution replaceCharactersInRange:NSMakeRange(index, 1) withString:@"#"];
    result += [self countPossibleSolutions:solution fromIndex:index + 1];

    return result;
  } else {
    return [self countPossibleSolutions:solution fromIndex:index + 1];
  }
}

- (BOOL)isValid:(NSString *)solution {
  NSMutableArray *groups = [NSMutableArray arrayWithCapacity:self.contiguousGroups.count];

  int currentGroupSize = 0;

  for (NSUInteger i = 0; i < solution.length; i++) {
    unichar ch = [solution characterAtIndex:i];

    if (ch == '#') {
      currentGroupSize += 1;
    } else if (ch == '.' && currentGroupSize > 0) {
      [groups addObject:@(currentGroupSize)];
      currentGroupSize = 0;
    }
  }

  if (currentGroupSize > 0)
    [groups addObject:@(currentGroupSize)];

  return [groups isEqual:self.contiguousGroups];
}

@end


int processLine(NSString *line) {
  NSArray *parts = [line componentsSeparatedByString:@" "];
  NSString *conditions = parts[0];
  NSArray<NSNumber *> *contiguousGroups = [[parts[1] componentsSeparatedByString:@","] valueForKey:@"intValue"];

  Solver *solver = [[Solver alloc] initWithConditionRecord:conditions contiguousGroups:contiguousGroups];

  return [solver countPossibleSolutions];
}

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

  int result = 0;

  for (NSString *line in [fileContents componentsSeparatedByString:@"\n"]) {
    if (line.length > 0) {
      result += processLine(line);
    }
  }

  NSLog(@"[Part 1] Sum of possible solutions: %d", result);

  return 0;
}
