#!/usr/bin/env bash

set -euo pipefail

input_path=${1?:Expected input as first arg}

sum_points=0;

while read line; do
  line1=$(echo "$line" | sed 's/:/|/')
  winning=$(echo "$line1" | cut -d '|' -f 2);
  # spaces are so grep works below
  numbers=" $(echo "$line1" | cut -d '|' -f 3) ";

  points=0;

  for w in $winning; do
    if echo "$numbers" | grep " $w " >/dev/null; then
      if [[ $points -eq 0 ]]; then
        points=1;
      else
        points=$(( points * 2 ));
      fi
    fi
  done

  sum_points=$(( sum_points + points ));
done < $input_path

echo "Sum of points: $sum_points"
