#!/usr/bin/env bash

set -euo pipefail

input_path=${1?:Expected input as first arg}

# start with zero, since rest of code is 1 based
declare -a copies=(0);

# pre-populate copies array
card_number=1;
while read line; do
  copies+=(1);
  card_number=$(( card_number + 1));
done < $input_path

# process
card_number=1;
while read line; do
  line1=$(echo "$line" | sed 's/:/|/')
  winning=$(echo "$line1" | cut -d '|' -f 2);
  # spaces are so grep works below
  numbers=" $(echo "$line1" | cut -d '|' -f 3) ";

  copies_this=${copies[$card_number]};
  copies_i=$(( card_number + 1 ));

  for w in $winning; do
    if echo "$numbers" | grep " $w " >/dev/null; then
      current=${copies[copies_i]};
      copies[$copies_i]=$(( current + copies_this ));
      copies_i=$(( copies_i + 1 ));
    fi
  done

  card_number=$(( card_number + 1));
done < $input_path

# sum
sum=0;
for c in "${copies[@]}"; do
  sum=$(( sum + c ));
done

echo "Total scratchcards: $sum";
