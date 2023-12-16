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

function main() {
  if (process.argv.length != 3) {
    console.error("usage: node reflections.js path/to/input.txt");
    process.exit(1);
  }

  let input = fs.readFileSync(process.argv[2], {encoding: 'utf8', mode: 'r'});

  let sum = 0;

  for (p of input.split("\n\n")) {
    var pattern = p.trim().split("\n");

    let vertical = findVerticalReflection(pattern)
    if (vertical != null) {
      sum += vertical * 100;
    } else {
      sum += findVerticalReflection(rotate(pattern));
    }
  }
  console.log("[PART 1] Summarized pattern notes:", sum);
}

main()
