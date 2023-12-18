const fs = require('fs');

function findVerticalReflection(pattern) {
  for (var i = 1; i < pattern.length; i++) {
    if (pattern[i] == pattern[i-1]) {
      // possible pattern
      for (var j = 1; ; j++) {
        if (i - 1 - j < 0 || i + j >= pattern.length) return i;
        if (pattern[i - 1 - j] != pattern[i + j]) break;
      }
    }
  }
  return null;
}

function findReflection(pattern) {
  let index = findVerticalReflection(pattern);
  if (index != null) {
    return {direction: "vertical", index: index};
  }

  index = findVerticalReflection(rotate(pattern));
  if (index != null) {
    return {direction: "horizontal", index: index};
  }

  return null;
}

function reflectionEqual(a, b) {
  return a.index == b.index && a.direction == b.direction;
}

function reflectionValue(r) {
  if (r.direction == 'vertical') {
    return r.index * 100;
  } else {
    return r.index;
  }
}

function rotate(pattern) {
  let result = [];

  for (var i = 0; i < pattern[0].length; i++) {
    let line = "";
    for (var j = 0; j < pattern.length; j++) {
      line += pattern[j][i];
    }
    result.push(line);
  }

  return result;
}

function flip(row, index) {
  let replacement = row[index] == '#' ? '.' : '#';

  return row.substr(0, index) + replacement + row.substr(index + 1, row.length - 1 - index)
}

function main() {
  if (process.argv.length != 3) {
    console.error("usage: node reflections.js path/to/input.txt");
    process.exit(1);
  }

  let input = fs.readFileSync(process.argv[2], {encoding: 'utf8', mode: 'r'});

  let sumPart1 = 0;
  let sumPart2 = 0;

  for (p of input.split("\n\n")) {
    let pattern = p.trim().split("\n");

    // Part 1
    let reflection = findReflection(pattern);
    sumPart1 += reflectionValue(reflection);

    // Part 2
    let foundSecondReflection = false;
    for (var y = 0; y < pattern.length; y++) {
      for (var x = 0; x < pattern[y].length; x++) {
        let original = pattern[y];
        pattern[y] = flip(original, x);

        let reflection2 = findReflection(pattern);
        if (reflection2 != null && !reflectionEqual(reflection, reflection2)) {
          sumPart2 += reflectionValue(reflection2);
          foundSecondReflection = true;
          break;
        }

        pattern[y] = original;
      }
      if (foundSecondReflection) break;
    }
  }
  console.log("[PART 1] Summarized pattern notes:", sumPart1);
  console.log("[PART 2] Summarized pattern notes:", sumPart2);
}

main()
