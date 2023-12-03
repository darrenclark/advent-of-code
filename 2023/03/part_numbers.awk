#!/usr/bin/env awk -f

{
  if (length > width) {
    width = length;
  }

  y = NR - 1;
  for (x = 0; x < length; x++) {
    grid[x, y] = substr($0, x + 1, 1);
  }
}

function is_symbol(grid, x, y) {
  return grid[x, y] ~ /^[^0-9\.]$/;
}

function is_part_number(grid, num, y, x_start, x_end) {
  for (x1 = x_start - 1; x1 < x_end + 1; x1++) {
    if (is_symbol(grid, x1, y - 1) || is_symbol(grid, x1, y) || is_symbol(grid, x1, y + 1)) {
      return 1;
    }
  }

  return 0;
}

END {
  height = NR;

  sum_of_part_numbers = 0;

  for (y = 0; y < height; y++) {
    num = -1;
    num_start_x = -1;

    for (x = 0; x < width; x++) {
      ch = grid[x, y];
      if (ch ~ /[0-9]/) {
        if (num_start_x < 0) {
          num_start_x = x;
          num = ch + 0;
        } else {
          num = num * 10 + ch;
        }
      } else if (num > 0) {
        if (is_part_number(grid, num, y, num_start_x, x)) {
          sum_of_part_numbers += num;
        }

        num = -1;
        num_start_x = -1;
      }
    }

    if (num > 0) {
      if (is_part_number(grid, num, y, num_start_x, x)) {
        sum_of_part_numbers += num;
      }

      num = -1;
      num_start_x = -1;
    }
  }

  printf "Sum of part numbers: %d\n", sum_of_part_numbers
}
