import sys
import datetime
import subprocess

def hex_to_rgb(hex_color):
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def calculate_color(start_color, end_color, ratio):
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)
    current_rgb = [round(start + (end - start) * ratio) for start, end in zip(start_rgb, end_rgb)]
    return ''.join(f"{value:02x}" for value in current_rgb)

def get_time_period(current_time, color_times):
    for period_start, colors in sorted(color_times.items()):
        period_start_time = datetime.datetime.strptime(period_start, "%H:%M").time()
        if current_time < period_start_time:
            return colors
    return next(iter(color_times.values()))  # Fallback to first item if no match

def main(vendor_and_product_id):
    color_times = {
        "22:00": ("990000", "990000"),  # Night
        "21:00": ("0000ff", "990000"),  # Evening Blue to Night
        "20:00": ("fdbe51", "0000ff"),  # Evening Golden to Blue
        "19:30": ("ff4500", "fdbe51"),  # Sunset to Golden
        "12:00": ("ffffff", "ff4500"),  # Noon to Sunset
        "07:30": ("ffd700", "ffffff"),  # Sunrise to Noon
        "07:00": ("f9c80e", "ffd700"),  # Morning Golden to Sunrise
        "06:00": ("ff7f00", "f9c80e"),  # Dawn to Golden
        "05:00": ("5bc0eb", "ff7f00"),  # Morning Blue to Dawn
        "04:00": ("990000", "5bc0eb"),  # Night to Blue
    }

    current_time = datetime.datetime.now().time()
    start_color, end_color = get_time_period(current_time, color_times)

    transition_ratio = (current_timestamp - start_timestamp) / (end_timestamp - start_timestamp)
    current_color = calculate_color(start_color, end_color, transition_ratio)

    print(f"Changing keyboard color to #{current_color}.")
    try:
        subprocess.run(["msi-perkeyrgb", "--model", "GS65", "-s", current_color, "--id", vendor_and_product_id], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error setting keyboard color: {e}")
        exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Vendor and product ID is missing.")
        print("Usage: python keyboard_color.py <vendor_and_product_id>")
        sys.exit(1)

    vendor_and_product_id = sys.argv[1]
    main(vendor_and_product_id)
