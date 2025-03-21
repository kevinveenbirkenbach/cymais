#!/bin/bash

# Check if correct number of arguments is given
if [[ $# -ne 3 ]]; then
  echo "Usage: $0 <input_file> <apt_output_file> <pip_output_file>"
  echo "Input: $0 <$1> <$2> <$3>"
  exit 1
fi

input_file="$1"
apt_file="$2"
pip_file="$3"

# Clear the output files
> "$apt_file"
> "$pip_file"

current_section=""

while IFS= read -r line; do
  [[ -z "$line" ]] && continue

  if [[ "$line" == apt:* ]]; then
    current_section="apt"
    continue
  elif [[ "$line" == pip:* ]]; then
    current_section="pip"
    continue
  fi

  package=$(echo "$line" | sed 's/^[[:space:]]*//')

  if [[ "$current_section" == "apt" ]]; then
    echo "$package" >> "$apt_file"
  elif [[ "$current_section" == "pip" ]]; then
    echo "$package" >> "$pip_file"
  fi
done < "$input_file"