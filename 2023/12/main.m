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

@property (nonatomic, strong) NSString *conditionRecord;
@property (nonatomic, strong) NSArray<NSNumber *> *contiguousGroups;

@property(nonatomic, strong) Memorize *memoize;

@end

@implementation Solver

- (instancetype)initWithConditionRecord:(NSString *)conditionRecord
                       contiguousGroups:
                           (NSArray<NSNumber *> *)contiguousGroups {
  if (self = [super init]) {
    _conditionRecord = conditionRecord;
    _contiguousGroups = contiguousGroups;

    _memoize = [[Memorize alloc] init];
  }
  return self;
}

- (long)countPossible {
  return [self countPossibleFromIndex:0 groupIndex:0];
}

- (long)countPossibleFromIndex:(NSUInteger)index groupIndex:(NSUInteger)groupIndex {
  return [[_memoize lookup:@[@(index), @(groupIndex)] orCompute:^id{
    long result = 0;

    if (index >= _conditionRecord.length) {
      return groupIndex == _contiguousGroups.count ? @1 : @0;
    }

    unichar ch = [_conditionRecord characterAtIndex:index];
    if (ch == '.' || ch == '?') {
      result += [self countPossibleFromIndex:index + 1 groupIndex:groupIndex];
    }

    @try {
      NSUInteger groupEnd = index + _contiguousGroups[groupIndex].longValue;
      if ([self isGroupFrom:index upTo:groupEnd]) {
        result += [self countPossibleFromIndex:groupEnd + 1 groupIndex:groupIndex + 1];
      }
    } @catch (NSException * e) {
      if ([e.name isEqual:NSRangeException]) {
        // ignore - array past end
      } else if ([e.name isEqual:NSInvalidArgumentException]) {
        // ignore - string past end
      } else {
        @throw e;
      }
    }

    return @(result);
  }] longLongValue];
}

- (BOOL)isGroupFrom:(NSUInteger)start upTo:(NSUInteger)end {
  for (NSUInteger i = start; i < end; i++) {
    if ([_conditionRecord characterAtIndex:i] == '.') {
      return NO;
    }
  }

  return end >= _conditionRecord.length || [_conditionRecord characterAtIndex:end] != '#';
}

@end

long processLine(NSString *line) {
  NSArray *parts = [line componentsSeparatedByString:@" "];
  NSString *conditions = parts[0];
  NSArray<NSNumber *> *contiguousGroups =
      [[parts[1] componentsSeparatedByString:@","] valueForKey:@"intValue"];

  Solver *solver = [[Solver alloc] initWithConditionRecord:conditions
                                          contiguousGroups:contiguousGroups];

  return [solver countPossible];
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
      result += processLine(line);
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
