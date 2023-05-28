#!/bin/bash

# Check if the vendor and product ID is provided
if [ -z "$1" ]; then
    echo "Error: Vendor and product ID is missing."
    echo "Usage: /opt/keyboard_color.sh <vendor_and_product_id>"
    exit 1
fi

# Extract the vendor and product ID from the command-line argument
vendor_and_product_id=$1

# Define the color transition parameters
fade_duration=1800          # 30 minutes in seconds
transition_start="06:00"
transition_end="06:30"
red_start="18:00"
red_end="06:00"
red_color="ff0000"

# Get the current time in HH:MM format
current_time=$(date +%H:%M)

# Check if it's within the red period
if [[ "$current_time" > "$red_start" || "$current_time" < "$red_end" ]]; then
    # Set the color to red directly
    sudo msi-perkeyrgb --model GS65 -s "$red_color" --id "$vendor_and_product_id"
else
    # Check if it's within the fading period
    if [[ "$current_time" > "$transition_start" && "$current_time" < "$transition_end" ]]; then
        # Calculate the transition ratio within the fading period
        start_seconds=$(date -d "$transition_start" +%s)
        end_seconds=$(date -d "$transition_end" +%s)
        current_seconds=$(date -d "$current_time" +%s)
        transition_ratio=$(awk "BEGIN { ratio = ($current_seconds - $start_seconds) / ($end_seconds - $start_seconds); print ratio }")

        # Calculate the current color based on the transition ratio
        r=$(awk "BEGIN { value = 255 - 255 * $transition_ratio; printf(\"%.0f\", value) }")
        g=0
        b=0

        # Convert the RGB values to hexadecimal format
        current_color=$(printf '%02x%02x%02x' $r $g $b)

        # Set the color using msi-perkeyrgb
        sudo msi-perkeyrgb --model GS65 -s "$current_color" --id "$vendor_and_product_id"
    else
        # Calculate the transition ratio based on the time of day
        start_seconds=$(date -d "$transition_end" +%s)
        end_seconds=$(date -d "$red_start" +%s)
        current_seconds=$(date -d "$current_time" +%s)
        transition_ratio=$(awk "BEGIN { ratio = ($current_seconds - $start_seconds) / ($end_seconds - $start_seconds); print ratio }")

        # Calculate the current color based on the transition ratio
        r=$(awk "BEGIN { value = 255 * $transition_ratio; printf(\"%.0f\", value) }")
        g=$(awk "BEGIN { value = 0 + (255 - 0) * $transition_ratio; printf(\"%.0f\", value) }")
        b=$(awk "BEGIN { value = 0 + (255 - 0) * $transition_ratio; printf(\"%.0f\", value) }")

        # Convert the RGB values to hexadecimal format
        current_color=$(printf '%02x%02x%02x' $r $g $b)

        # Set the color using msi-perkeyrgb
        sudo msi-perkeyrgb --model GS65 -s "$current_color" --id "$vendor_and_product_id"
    fi
fi
