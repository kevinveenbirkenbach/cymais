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
morning_blue_color="5bc0eb" # Morning Blue Color
dawn_color="ff7f00" # Dawn Color
morning_golden_hour_color="f9c80e" # Morning Golden Hour Color
sunrise_color="ffd700" # Sunrise Color
noon_color="ffffff" # Noon Color
twilight_color="ff6f61" # Twilight Color
evening_golden_hour_color="fdbe51" # Evening Golden Hour Color
evening_blue_color="0000ff" # Evening Blue Color
sunset_color="ff4500" # Sunset Color
night_color="990000" # Night Color

# Function to calculate the color based on the transition ratio
calculate_color() {
    local color_start=$1
    local color_end=$2
    local transition_ratio=$3

    local start_r=$((16#${color_start:0:2}))
    local start_g=$((16#${color_start:2:2}))
    local start_b=$((16#${color_start:4:2}))

    local end_r=$((16#${color_end:0:2}))
    local end_g=$((16#${color_end:2:2}))
    local end_b=$((16#${color_end:4:2}))

    local current_r=$(awk "BEGIN { r = ${start_r} + (${end_r} - ${start_r}) * ${transition_ratio}; printf(\"%.0f\", r) }")
    local current_g=$(awk "BEGIN { g = ${start_g} + (${end_g} - ${start_g}) * ${transition_ratio}; printf(\"%.0f\", g) }")
    local current_b=$(awk "BEGIN { b = ${start_b} + (${end_b} - ${start_b}) * ${transition_ratio}; printf(\"%.0f\", b) }")

    local calculated_color=$(printf "%02x%02x%02x" "$current_r" "$current_g" "$current_b")

    if [ "$calculated_color" = "ffff100" ]; then
        calculated_color="ffffff"
    fi

    echo "$calculated_color"
}

# Get the current time in HH:MM format
current_time=$(date +%H:%M)

# Calculate the transition ratio based on the current time
if [[ "$current_time" > "22:00" || "$current_time" < "04:00" ]]; then
    # Night (22:00 to 04:00)
    color_start="$night_color"
    color_end="$night_color"
    color_start_time="22:00"
    color_end_time="04:00"
elif [[ "$current_time" > "21:00" ]]; then
    # Evening Blue Hour to Night (21:00 to 22:00)
    color_start="$evening_blue_color"
    color_end="$night_color"
    color_start_time="21:00"
    color_end_time="22:00"
elif [[ "$current_time" > "20:00" ]]; then
    # Evening Golden Hour to Evening Blue Hour (20:00 to 21:00)
    color_start="$evening_golden_hour_color"
    color_end="$evening_blue_color"
    color_start_time="20:00"
    color_end_time="21:00"
elif [[ "$current_time" > "19:30" ]]; then
    # Sunset to Evening Golden Hour (19:30 to 20:00)
    color_start="$sunset_color"
    color_end="$evening_golden_hour_color"
    color_start_time="19:30"
    color_end_time="20:00"
elif [[ "$current_time" > "12:00" ]]; then
    # Noon to Sunset (12:00 to 19:30)
    color_start="$noon_color"
    color_end="$sunset_color"
    color_start_time="12:00"
    color_end_time="19:30"
elif [[ "$current_time" > "07:30" ]]; then
    # Sunrise to Noon (07:30 to 12:00)
    color_start="$sunrise_color"
    color_end="$noon_color"
    color_start_time="07:30"
    color_end_time="12:00"
elif [[ "$current_time" > "07:00" ]]; then
    # Morning Golden Hour to Sunrise (07:00 to 07:30)
    color_start="$morning_golden_hour_color"
    color_end="$sunrise_color"
    color_start_time="07:00"
    color_end_time="07:30"
elif [[ "$current_time" > "06:00" ]]; then
    # Dawn to Morning Golden Hour (06:00 to 07:00)
    color_start="$dawn_color"
    color_end="$morning_golden_hour_color"
    color_start_time="06:00"
    color_end_time="07:00"
elif [[ "$current_time" > "05:00" ]]; then
    # Morning Blue Hour to Dawn (05:00 to 06:00)
    color_start="$morning_blue_color"
    color_end="$dawn_color"
    color_start_time="05:00"
    color_end_time="06:00"
elif [[ "$current_time" > "04:00" ]]; then
    # Night to Morning Blue Hour (22:00 to 04:00)
    color_start="$night_color"
    color_end="$morning_blue_color"
    color_start_time="04:00"
    color_end_time="05:00"
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

echo "Changing keyboard color to #$current_color."

# Set the color using msi-perkeyrgb
msi-perkeyrgb --model GS65 -s "$current_color" --id "$vendor_and_product_id"