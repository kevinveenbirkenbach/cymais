#!/bin/bash

set -euo pipefail

# Check if the vendor and product ID is provided
if [ -z "${1-}" ]; then
    echo "Error: Vendor and product ID is missing."
    echo "Usage: /opt/keyboard_color.sh <vendor_and_product_id>"
    exit 1
fi

# Extract the vendor and product ID from the command-line argument
vendor_and_product_id=$1

# Define the color transition parameters
noon_color="ffffff"
twilight_color="ff00a8"
sunset_color="ff0000"
dawn_color="ff0000"
sunrise_color="00e4ff"

# Function to calculate the color based on the transition ratio
calculate_color() {
    local color_start=$1
    local color_end=$2
    local transition_ratio=$3

    local start_value=$((16#${color_start}))
    local end_value=$((16#${color_end}))

    local current_value=$(awk "BEGIN { value = ${start_value} + (${end_value} - ${start_value}) * ${transition_ratio}; printf(\"%.0f\", value) }")

    printf "%06x" "${current_value}"
}

# Get the current time in HH:MM format
current_time=$(date +%H:%M)

# Calculate the transition ratio based on the current time
if [[ "$current_time" > "21:00" || "$current_time" < "06:00" ]]; then
    # Transition from sunset to dawn (21:00 to 06:00)
    color_start="ff0000"
    color_end="ff0000"
    color_start_time="21:00"
    color_end_time="00:00"
elif [[ "$current_time" > "06:00" && "$current_time" < "09:00" ]]; then
    # Transition from dawn to sunrise (06:00 to 09:00)
    color_start="ff0000"
    color_end="00e4ff"
    color_start_time="06:00"
    color_end_time="09:00"
elif [[ "$current_time" > "09:00" && "$current_time" < "12:00" ]]; then
    # Transition from sunrise to noon (09:00 to 12:00)
    color_start="00e4ff"
    color_end="ffffff"
    color_start_time="09:00"
    color_end_time="12:00"
elif [[ "$current_time" > "12:00" && "$current_time" < "18:00" ]]; then
    # Transition from noon to twilight (12:00 to 18:00)
    color_start="ffffff"
    color_end="ff00a8"
    color_start_time="12:00"
    color_end_time="18:00"
else
    # Transition from twilight to sunset (18:00 to 21:00)
    color_start="ff00a8"
    color_end="ff0000"
    color_start_time="18:00"
    color_end_time="21:00"
fi

# Get the current date in YYYY-MM-DD format
current_date=$(date +%Y-%m-%d)

# Calculate the start and end timestamps based on the current date and time
start_timestamp=$(date -d "${current_date} ${color_start_time}" +%s)
end_timestamp=$(date -d "${current_date} ${color_end_time}" +%s)

# Get the current timestamp
current_timestamp=$(date +%s)

# Calculate the transition ratio
transition_ratio=$(awk "BEGIN { ratio = ($current_timestamp - $start_timestamp) / ($end_timestamp - $start_timestamp); print ratio }")

# Calculate the current color based on the transition ratio
current_color=$(calculate_color "$color_start" "$color_end" "$transition_ratio")

echo "changing keyboard color to #$current_color."

# Set the color using msi-perkeyrgb
msi-perkeyrgb --model GS65 -s "$current_color" --id "$vendor_and_product_id"