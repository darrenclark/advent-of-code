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

function is_gear(grid, x, y) {
  return grid[x, y] == "*";
}

function update_possible_gears(grid, num, y, x_start, x_end) {
  for (x1 = x_start - 1; x1 < x_end + 1; x1++) {
    if (is_gear(grid, x1, y - 1)) {
      possible_gears[x1, y - 1] = possible_gears[x1, y - 1] "," num;
    }
    if (is_gear(grid, x1, y)) {
      possible_gears[x1, y] = possible_gears[x1, y] "," num;
    }
    if (is_gear(grid, x1, y + 1)) {
      possible_gears[x1, y + 1] = possible_gears[x1, y + 1] "," num;
    }
  }
}

END {
  height = NR;

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
        update_possible_gears(grid, num, y, num_start_x, x);

        num = -1;
        num_start_x = -1;
      }
    }

    if (num > 0) {
      update_possible_gears(grid, num, y, num_start_x, x);

      num = -1;
      num_start_x = -1;
    }
  }

  sum_of_gear_ratios = 0

  for (idx in possible_gears) {
    sub(/^,/, "", possible_gears[idx]);
    split(possible_gears[idx], nums, ",");

    if (length(nums) == 2) {
      sum_of_gear_ratios += nums[1] * nums[2];
    }
  }

  printf "Sum of gear ratios: %d\n", sum_of_gear_ratios
}
