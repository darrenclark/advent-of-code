#import <Foundation/Foundation.h>

static NSCountedSet *counts;

typedef NSArray<NSArray<NSNumber *> *> *PossibleGroups;

@interface Memorize : NSObject

@property(nonatomic, strong) NSMutableDictionary *results;

@end

@implementation Memorize

- (instancetype)init {
  if (self = [super init]) {
    _results = [NSMutableDictionary dictionary];
  }
  return self;
}

- (id)lookup:(id)key orCompute:(id (^)())block {
  id result = _results[key];
  if (result != nil) {
    return result;
  }
  result = block();
  _results[key] = result;
  return result;
}

@end

@interface Solver : NSObject

@property(nonatomic, strong) NSArray<NSString *> *parts;
@property(nonatomic, strong) NSArray<NSNumber *> *contiguousGroups;
@property(nonatomic, strong) Memorize *memoizePossibleSolutions;
@property(nonatomic, strong) Memorize *memoizePossibleGroups;

@end

@implementation Solver

- (instancetype)initWithConditionRecord:(NSString *)conditionRecord
                       contiguousGroups:
                           (NSArray<NSNumber *> *)contiguousGroups {
  if (self = [super init]) {
    _contiguousGroups = contiguousGroups;

    _memoizePossibleSolutions = [[Memorize alloc] init];
    _memoizePossibleGroups = [[Memorize alloc] init];

    NSMutableArray *parts = [NSMutableArray array];
    for (NSString *string in
         [conditionRecord componentsSeparatedByString:@"."]) {
      if (string.length > 0) {
        [parts addObject:string];
      }
    }

    _parts = parts;
  }
  return self;
}

- (long)countPossibleSolutions {
  return [self countPossibleSolutions:[NSArray array] fromIndex:0].longValue;
}

- (NSNumber *)countPossibleSolutions:(NSArray *)groups
                           fromIndex:(NSUInteger)index {
  id key = @[ groups, @(index) ];
  return [_memoizePossibleSolutions
         lookup:key
      orCompute:^id {
        if (index == _parts.count) {
          return [groups isEqual:self.contiguousGroups] ? @1 : @0;
        } else {
          long result = 0;

          if (groups.count == _contiguousGroups.count) {
            // only "no groups" will match
            for (NSArray *possibleGroups in
                 [self possibleGroups:_parts[index]]) {
              if (possibleGroups.count == 0) {
                result += [self countPossibleSolutions:groups
                                             fromIndex:index + 1]
                              .longValue;
              }
            }

          } else {
            for (NSArray *possibleGroups in
                 [self possibleGroups:_parts[index]]) {
              if (![self nextGroups:possibleGroups
                      arePossibleAtGroupIndex:groups.count])
                continue;

              result +=
                  [self
                      countPossibleSolutions:
                          [groups arrayByAddingObjectsFromArray:possibleGroups]
                                   fromIndex:index + 1]
                      .longValue;
            }
          }

          return @(result);
        }
      }];
}

- (BOOL)nextGroups:(NSArray *)possibleGroups
    arePossibleAtGroupIndex:(NSUInteger)index {
  if (index + possibleGroups.count > _contiguousGroups.count)
    return NO;

  for (NSUInteger i = 0; i < possibleGroups.count; i++) {
    if (![possibleGroups[i] isEqual:_contiguousGroups[index + i]])
      return NO;
  }

  return YES;
}

- (PossibleGroups)possibleGroups:(NSString *)part {
  return [_memoizePossibleGroups lookup:part
                              orCompute:^id {
                                NSMutableArray *answer = [NSMutableArray array];
                                [self findPossibleGroups:[part mutableCopy]
                                               fromIndex:0
                                              intoAnswer:answer];
                                return answer;
                              }];
}

- (void)findPossibleGroups:(NSMutableString *)part
                 fromIndex:(NSUInteger)index
                intoAnswer:(NSMutableArray *)answer {
  if (index == part.length) {
    [answer addObject:[self parseGroups:part]];
  } else if ([part characterAtIndex:index] == '?') {
    [part replaceCharactersInRange:NSMakeRange(index, 1) withString:@"."];
    [self findPossibleGroups:part fromIndex:index + 1 intoAnswer:answer];

    [part replaceCharactersInRange:NSMakeRange(index, 1) withString:@"#"];
    [self findPossibleGroups:part fromIndex:index + 1 intoAnswer:answer];

    [part replaceCharactersInRange:NSMakeRange(index, 1) withString:@"?"];
  } else {
    [self findPossibleGroups:part fromIndex:index + 1 intoAnswer:answer];
  }
}

- (NSArray *)parseGroups:(NSString *)part {
  NSMutableArray *groups = [NSMutableArray array];

  int currentGroupSize = 0;

  for (NSUInteger i = 0; i < part.length; i++) {
    unichar ch = [part characterAtIndex:i];

    if (ch == '#') {
      currentGroupSize += 1;
    } else if (ch == '.' && currentGroupSize > 0) {
      [groups addObject:@(currentGroupSize)];
      currentGroupSize = 0;
    }
  }

  if (currentGroupSize > 0)
    [groups addObject:@(currentGroupSize)];

  return groups;
}

@end

int processLine(NSString *line) {
  NSArray *parts = [line componentsSeparatedByString:@" "];
  NSString *conditions = parts[0];
  NSArray<NSNumber *> *contiguousGroups =
      [[parts[1] componentsSeparatedByString:@","] valueForKey:@"intValue"];

  Solver *solver = [[Solver alloc] initWithConditionRecord:conditions
                                          contiguousGroups:contiguousGroups];

  return [solver countPossibleSolutions];
}

NSString *unfold5x(NSString *line) {
  NSArray *parts = [line componentsSeparatedByString:@" "];

  return [NSString stringWithFormat:@"%@?%@?%@?%@?%@ %@,%@,%@,%@,%@", parts[0],
                                    parts[0], parts[0], parts[0], parts[0],
                                    parts[1], parts[1], parts[1], parts[1],
                                    parts[1]];
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

  long result = 0;

  for (NSString *line in [fileContents componentsSeparatedByString:@"\n"]) {
    if (line.length > 0) {
      long r = processLine(line);
      result += r;
    }
  }

  NSLog(@"[Part 1] Sum of possible solutions: %ld", result);

  result = 0;

  for (NSString *line in [fileContents componentsSeparatedByString:@"\n"]) {
    if (line.length > 0) {
      result += processLine(unfold5x(line));
    }
  }

  NSLog(@"[Part 2] Sum of possible solutions: %ld", result);

  return 0;
}
