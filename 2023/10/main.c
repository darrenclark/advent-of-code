#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>


static const char* usage = "Expected two args: part1|part2 ./path/to/input.txt";

_Noreturn static void exit_with_message(const char *message) {
  printf("%s\n", message);
  exit(1);
}

typedef enum {
  NORTH = (1u << 1),
  SOUTH = (1u << 2),
  EAST = (1u << 3),
  WEST = (1u << 4),
} direction_t;

typedef unsigned int direction_mask_t;

static direction_mask_t edges(char c) {
  switch (c) {
    case '|': return NORTH | SOUTH;
    case '-': return WEST | EAST;
    case 'J': return NORTH | WEST;
    case 'L': return NORTH | EAST;
    case '7': return SOUTH | WEST;
    case 'F': return SOUTH | EAST;
    default: return 0;
  }
}

static char mask_to_char(direction_mask_t m) {
  switch (m) {
    case NORTH | SOUTH: return '|';
    case WEST | EAST: return '-';
    case NORTH | WEST: return 'J';
    case NORTH | EAST: return 'L';
    case SOUTH | WEST: return '7';
    case SOUTH | EAST: return 'F';
    default: exit_with_message("mask_to_char failed");
  }
}

static direction_mask_t edges_count(direction_mask_t m) {
  int count = 0;
  if (m & NORTH) count += 1;
  if (m & SOUTH) count += 1;
  if (m & WEST) count += 1;
  if (m & EAST) count += 1;
  return count;
}

void debug_direction_mask(const char *label, direction_mask_t m) {
  printf("%s n=%d s=%d w=%d e=%d\n", label, (m & NORTH) != 0, (m & SOUTH) != 0, (m & WEST) != 0, (m & EAST) != 0);
}

typedef enum {
  FILL_UNKNOWN,
  FILL_PIPE,
  FILL_OUTSIDE,
  FILL_INSIDE,
} fill_t;

typedef struct {
  char **grid;  // grid[y][x]
  int width, height;
} input_t;

typedef struct {
  int x, y;
} location_t;

static bool location_equal(location_t a, location_t b) {
  return a.x == b.x && a.y == b.y;
}

typedef struct {
  input_t input;
  location_t start;
  location_t current;
  direction_mask_t entered_from;
  // part1
  int steps;
  // part2
  fill_t **fill;
} state_t;

static char neighbour(state_t *state, int dx, int dy) {
  int x = state->current.x + dx;
  int y = state->current.y + dy;

  if (x < 0 || y < 0 || x >= state->input.width || y >= state->input.height) {
    return '\0';
  } else {
    return state->input.grid[y][x];
  }
}

static int fill_idx(int x, int dx) {
  return x * 3 + 1 + dx;
}

static const int MAX_HEIGHT = 1024;


static input_t parse_input(char *input_file) {
  FILE *f = fopen(input_file, "r");
  if (f == NULL) {
    exit_with_message("File can't be opened");
  }

  char **grid = malloc(sizeof(char *) * MAX_HEIGHT);
  int y = 0;
  int width = -1;

  char *line = NULL;
  size_t linecap = 0;
  size_t linelen = 0;

  while ((linelen = getline(&line, &linecap, f)) > 0) {
    // Why is this needed? Why doeesn't the above while loop `> 0` work?
    if (linelen <= 0) {
      break;
    }

    grid[y] = strdup(line);

    int line_width = strlen(line);
    if (line_width <= 0) {
      // Why is this needed? Why doesn't the above getline check work?
      break;
    } else if (width < 0) {
      width = line_width;
    } else if (width != line_width) {
      printf("width=%d line_width=%d y=%d\n", width, line_width, y);
      exit_with_message("File has inconsistent line widths.  Check input");
    }

    y++;
    if (y >= MAX_HEIGHT) {
      exit_with_message("File has too many lines.  Increase MAX_HEIGHT and recompile.");
    }
  }

  fclose(f);

  input_t result;
  result.grid = grid;
  result.width = width - 1; // -1 to exclude newlines
  result.height = y;
  return result;
}

static location_t find_start(input_t *input) {
  location_t location;
  for (location.y = 0; location.y <= input->height; location.y++) {
    for (location.x = 0; location.x <= input->width; location.x++) {
      if (input->grid[location.y][location.x] == 'S') {
        return location;
      }
    }
  }

  exit_with_message("input didn't have start position");
}

static direction_mask_t connected_edges(state_t *state) {
  char current_cell = neighbour(state, 0, 0);
  direction_mask_t current = edges(current_cell);

  direction_mask_t north = edges(neighbour(state, 0, -1));
  direction_mask_t south = edges(neighbour(state, 0, 1));
  direction_mask_t west = edges(neighbour(state, -1, 0));
  direction_mask_t east = edges(neighbour(state, 1, 0));

  direction_mask_t result = 0;

  if (current_cell == 'S') {
    if (north & SOUTH) {
      result |= NORTH;
    }
    if (south & NORTH) {
      result |= SOUTH;
    }
    if (west & EAST) {
      result |= WEST;
    }
    if (east & WEST) {
      result |= EAST;
    }

    if (edges_count(result) != 2) {
      exit_with_message("start didn't have a connected pipe");
    }
  } else {
    if (current & NORTH && north & SOUTH) {
      result |= NORTH;
    }
    if (current & SOUTH && south & NORTH) {
      result |= SOUTH;
    }
    if (current & WEST && west & EAST) {
      result |= WEST;
    }
    if (current & EAST && east & WEST) {
      result |= EAST;
    }
  }

  return result;
}

static void put_fill_pipe(state_t *state, direction_mask_t ce) {
  state->fill[fill_idx(state->current.y, 0)][fill_idx(state->current.x, 0)] = FILL_PIPE;

  if (ce & NORTH) {
    state->fill[fill_idx(state->current.y, -1)][fill_idx(state->current.x, 0)] = FILL_PIPE;
  }

  if (ce & SOUTH) {
    state->fill[fill_idx(state->current.y, 1)][fill_idx(state->current.x, 0)] = FILL_PIPE;
  }

  if (ce & WEST) {
    state->fill[fill_idx(state->current.y, 0)][fill_idx(state->current.x, -1)] = FILL_PIPE;
  }

  if (ce & EAST) {
    state->fill[fill_idx(state->current.y, 0)][fill_idx(state->current.x, 1)] = FILL_PIPE;
  }
}

static void fill_outside(state_t *state) {
  int fill_width = state->input.width * 3;
  int fill_height = state->input.height * 3;

  // outer ring is always "outside"
  for (int x = 0; x < fill_width; x++) {
    state->fill[0][x] = FILL_OUTSIDE;
    state->fill[fill_height - 1][x] = FILL_OUTSIDE;
  }
  for (int y = 0; y < fill_height; y++) {
    state->fill[y][0] = FILL_OUTSIDE;
    state->fill[y][fill_width - 1] = FILL_OUTSIDE;
  }

  int filled;

  do {
    filled = 0;

    for (int y = 1; y < fill_height - 1; y++) {
      for (int x = 1; x < fill_width - 1; x++) {
        if (state->fill[y][x] != FILL_UNKNOWN) continue;

        if (state->fill[y-1][x] == FILL_OUTSIDE ||
            state->fill[y+1][x] == FILL_OUTSIDE ||
            state->fill[y][x-1] == FILL_OUTSIDE ||
            state->fill[y][x+1] == FILL_OUTSIDE) {
          state->fill[y][x] = FILL_OUTSIDE;
          filled += 1;
        }
      }
    }
  } while (filled > 0);
}

static void fill_inside(state_t *state) {
  // (all other states have been marked at this point)
  int fill_width = state->input.width * 3;
  int fill_height = state->input.height * 3;
  for (int y = 0; y < fill_height; y++) {
    for (int x = 0; x < fill_width; x++) {
      if (state->fill[y][x] == FILL_UNKNOWN) {
        state->fill[y][x] = FILL_INSIDE;
      }
    }
  }
}

static void step(state_t *state) {
  direction_mask_t ce = connected_edges(state);
  put_fill_pipe(state, ce);

  if (state->steps == 0) {
    // swap out S for actual pipe piece - to make rest of code nicer
    state->input.grid[state->start.y][state->start.x] = mask_to_char(ce);
  }

  if (ce & NORTH && (state->entered_from & NORTH) == 0) {
    state->current.y -= 1;
    state->entered_from = SOUTH;
  } else if (ce & SOUTH && (state->entered_from & SOUTH) == 0) {
    state->current.y += 1;
    state->entered_from = NORTH;
  } else if (ce & WEST && (state->entered_from & WEST) == 0) {
    state->current.x -= 1;
    state->entered_from = EAST;
  } else if (ce & EAST && (state->entered_from & EAST) == 0) {
    state->current.x += 1;
    state->entered_from = WEST;
  } else {
    exit_with_message("hit dead end");
  }

  state->steps += 1;
}

static void init_state(state_t *state, char *input_file) {
  state->input = parse_input(input_file);
  state->start = find_start(&state->input);

  state->current = state->start;
  state->entered_from = 0;
  state->steps = 0;

  state->fill = calloc(state->input.height * 3, sizeof(fill_t*));
  for (int y = 0; y < state->input.height * 3; y++) {
    state->fill[y] = calloc(state->input.width * 3, sizeof(fill_t));
  }
}

static void part1(char *input_file) {
  state_t state;
  init_state(&state, input_file);

  step(&state);
  while (!location_equal(state.current, state.start)) {
    step(&state);
  }

  printf("Steps to furthest from start: %01.f\n", ceil(state.steps / 2.0));
}

static void part2(char *input_file) {
  state_t state;
  init_state(&state, input_file);

  step(&state);
  while (!location_equal(state.current, state.start)) {
    step(&state);
  }

  fill_outside(&state);
  fill_inside(&state);

  int enclosed_squares = 0;

  for (int y = 0; y < state.input.height; y++) {
    for (int x = 0; x < state.input.width; x++) {
      int fill_x = fill_idx(x, 0);
      int fill_y = fill_idx(y, 0);
      if (state.fill[fill_y][fill_x] == FILL_INSIDE)
        enclosed_squares += 1;
    }
  }

  // print map
  for (int y = 0; y < state.input.height * 3; y++) {
    for (int x = 0; x < state.input.width * 3; x++) {
      char o = '?';
      switch (state.fill[y][x]) {
      case FILL_UNKNOWN: o = '?'; break;
      case FILL_PIPE: o = '#'; break;
      case FILL_INSIDE: o = 'I'; break;
      case FILL_OUTSIDE: o = ' '; break;
      }
      printf("%c", o);
    }
    printf("\n");
  }

  printf("Enclosed squares: %d\n", enclosed_squares);
}

int main(int argc, char *argv[]) {
  if (argc != 3) {
    exit_with_message(usage);
  }

  if (strcmp(argv[1], "part1") == 0) {
    part1(argv[2]);
  } else if (strcmp(argv[1], "part2") == 0) {
    part2(argv[2]);
  } else {
    exit_with_message(usage);
  }
}
