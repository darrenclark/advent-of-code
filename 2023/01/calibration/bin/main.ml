let non_digits = Str.regexp "[^0-9]"

let calibration_value line =
  let digits = Str.global_replace non_digits "" line in
  let len = String.length digits in
  let first = String.sub digits 0 1 in
  let last = String.sub digits (len - 1) 1 in
    int_of_string (first ^ last)

let () =
  let rec loop acc =
    try
      let line = read_line () in
      let v = calibration_value line in
        loop acc + v
    with
      End_of_file -> acc
  in
    Printf.printf "Sum of calibration values: %d\n" (loop 0)
