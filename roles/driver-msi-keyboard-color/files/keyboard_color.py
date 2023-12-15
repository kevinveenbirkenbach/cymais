import sys
import datetime
import subprocess

def hex_to_rgb(hex_color):
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def calculate_color(start_color, end_color, ratio):
    start_r, start_g, start_b = hex_to_rgb(start_color)
    end_r, end_g, end_b = hex_to_rgb(end_color)

    current_r = round(start_r + (end_r - start_r) * ratio)
    current_g = round(start_g + (end_g - start_g) * ratio)
    current_b = round(start_b + (end_b - start_b) * ratio)

    return f"{current_r:02x}{current_g:02x}{current_b:02x}"

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
    for start_time, (start_color, end_color) in sorted(color_times.items()):
        start_time_obj = datetime.datetime.strptime(start_time, "%H:%M").time()
        if current_time >= start_time_obj:
            break

    next_time, next_colors = next(iter(color_times.items()))
    next_start_time_obj = datetime.datetime.strptime(next_time, "%H:%M").time()

    start_timestamp = datetime.datetime.combine(datetime.datetime.now().date(), start_time_obj).timestamp()
    end_timestamp = datetime.datetime.combine(datetime.datetime.now().date(), next_start_time_obj).timestamp()
    current_timestamp = datetime.datetime.now().timestamp()

    transition_ratio = (current_timestamp - start_timestamp) / (end_timestamp - start_timestamp)
    current_color = calculate_color(start_color, end_color, transition_ratio)

    print(f"Changing keyboard color to #{current_color}.")
    subprocess.run(["msi-perkeyrgb", "--model", "GS65", "-s", current_color, "--id", vendor_and_product_id])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Vendor and product ID is missing.")
        print("Usage: python keyboard_color.py <vendor_and_product_id>")
        sys.exit(1)

    vendor_and_product_id = sys.argv[1]
    main(vendor_and_product_id)
