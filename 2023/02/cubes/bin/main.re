let max_red = 12;
let max_green = 13;
let max_blue = 14;

type color =
  | Red
  | Green
  | Blue;

type round = {
  red: int,
  green: int,
  blue: int,
};

let round_zeros = {red: 0, green: 0, blue: 0};

type game = {
  id: int,
  rounds: list(round),
};

let parse_rounds = rounds_part => {
  let parse_cube_count = cube_part => {
    let parts = cube_part |> String.split_on_char(' ');
    let count = parts |> List.hd |> int_of_string;
    let color =
      switch (List.nth(parts, 1)) {
      | "red" => Red
      | "green" => Green
      | "blue" => Blue
      | _ => raise(Not_found)
      };
    (count, color);
  };

  let update_round = (rnd, (count, color)) => {
    switch (color) {
    | Red => {...rnd, red: count}
    | Green => {...rnd, green: count}
    | Blue => {...rnd, blue: count}
    };
  };

  let parse_round = round_part => {
    round_part
    |> String.split_on_char(',')
    |> List.map(String.trim)
    |> List.map(parse_cube_count)
    |> List.fold_left(update_round, round_zeros);
  };

  rounds_part |> String.split_on_char(';') |> List.map(parse_round);
};

let parse_id = id_part => {
  let split = String.split_on_char(' ', id_part);
  int_of_string(List.nth(split, 1));
};

let parse_game = line => {
  let parts = String.split_on_char(':', line);
  let game = {
    id: parse_id(List.hd(parts)),
    rounds: parse_rounds(List.nth(parts, 1)),
  };
  game;
};

let is_possible_game = rounds => {
  let is_possible_round = ({red, green, blue}) => {
    red <= max_red && green <= max_green && blue <= max_blue;
  };
  List.for_all(is_possible_round, rounds);
};

let power = rounds => {
  let do_max = (rnd1, rnd2) => {
    {
      red: max(rnd1.red, rnd2.red),
      green: max(rnd1.green, rnd2.green),
      blue: max(rnd1.blue, rnd2.blue),
    };
  };
  let maxes = List.fold_left(do_max, round_zeros, rounds);
  maxes.red * maxes.green * maxes.blue
};

let part1 = () => {
  let rec loop = acc =>
    try({
      let line = read_line();
      let {id, rounds} = parse_game(line);
      if (is_possible_game(rounds)) {
        loop(acc + id);
      } else {
        loop(acc);
      };
    }) {
    | End_of_file => acc
    };

  Printf.printf("Sum of game IDs: %d\n", loop(0));
};

let part2 = () => {
  let rec loop = acc =>
    try({
      let line = read_line();
      let {id: _, rounds} = parse_game(line);
      loop(acc + power(rounds));
    }) {
    | End_of_file => acc
    };

  Printf.printf("Sum of powers: %d\n", loop(0));
};

let main = args => {
  switch (args) {
  | [_, "part1", ..._] => part1()
  | [_, "part2", ..._] => part2()
  | _ => part2()
  };
};

main(Array.to_list(Sys.argv));
