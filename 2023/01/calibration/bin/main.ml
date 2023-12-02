let digit_regex = Str.regexp {|\([0-9]\|one\|two\|three\|four\|five\|six\|seven\|eight\|nine\)|}

let to_digit str = match str with
  "one" -> "1"
  | "two" -> "2"
  | "three" -> "3"
  | "four" -> "4"
  | "five" -> "5"
  | "six" -> "6"
  | "seven" -> "7"
  | "eight" -> "8"
  | "nine" -> "9"
  | s -> s

let first_digit line =
  let _ = Str.search_forward digit_regex line 0 in
    line |> Str.matched_string |> to_digit

let last_digit line =
  let _ = Str.search_backward digit_regex line (String.length line) in
    line |> Str.matched_string |> to_digit

let calibration_value line =
  let first = first_digit line in
  let last = last_digit line in
  int_of_string (first ^ last)

let () =
  let rec loop acc =
    try
      let line = read_line () in
      let v = calibration_value line in
      loop acc + v
    with End_of_file -> acc
  in
  Printf.printf "Sum of calibration values: %d\n" (loop 0)
