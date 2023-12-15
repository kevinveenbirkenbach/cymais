import sys
import datetime
import subprocess

def hex_to_rgb(hex_color):
    """Konvertiert Hex-Farbe in RGB-Tupel."""
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def calculate_color(start_color, end_color, ratio):
    """Berechnet interpolierte Farbe zwischen zwei Farben basierend auf Übergangsverhältnis."""
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)
    current_rgb = [round(start + (end - start) * ratio) for start, end in zip(start_rgb, end_rgb)]
    return ''.join(f"{value:02x}" for value in current_rgb)

def get_current_period(current_time, color_times):
    """
    Ermittelt die aktuelle Zeitperiode und gibt die zugehörigen Farben zurück.

    Args:
    current_time (datetime.time): Die aktuelle Uhrzeit.
    color_times (dict): Ein Wörterbuch, das Zeitperioden (als String im Format 'HH:MM') 
                        mit Farbpaaren verbindet.

    Returns:
    tuple: Ein Tupel der Start- und Endfarbe (als Hex-Codes) für die aktuelle Periode.
    """
    # Liste der Zeitperioden sortieren
    sorted_periods = sorted(color_times.items())

    # Über die sortierten Perioden iterieren, um die aktuelle Periode zu finden
    for i, (period_start_str, colors) in enumerate(sorted_periods):
        period_start_time = datetime.datetime.strptime(period_start_str, "%H:%M").time()

        # Wenn die aktuelle Zeit vor dem Beginn der nächsten Periode liegt
        if current_time < period_start_time:
            # Wenn wir uns in der ersten Periode befinden, ist die vorherige Periode die letzte des Tages
            previous_period_index = i - 1 if i > 0 else -1
            return sorted_periods[previous_period_index][1]

    # Falls die aktuelle Zeit nach der letzten definierten Periode liegt,
    # verwende die Farben der ersten Periode als Standard
    return sorted_periods[0][1]

def calculate_transition_ratio(current_time, start_time, end_time):
    """
    Berechnet das Übergangsverhältnis für eine Farbtransition.

    Args:
    current_time (datetime.time): Die aktuelle Uhrzeit.
    start_time (datetime.time): Die Startzeit der aktuellen Farbperiode.
    end_time (datetime.time): Die Endzeit der aktuellen Farbperiode.

    Returns:
    float: Das Übergangsverhältnis zwischen 0 und 1.
    """
    # Aktuelles Datum für die Zeitstempelberechnung verwenden
    today = datetime.datetime.now().date()

    # Zeitstempel für den Beginn und das Ende der aktuellen Periode berechnen
    start_timestamp = datetime.datetime.combine(today, start_time).timestamp()
    end_timestamp = datetime.datetime.combine(today, end_time).timestamp()

    # Aktuellen Zeitstempel berechnen
    current_timestamp = datetime.datetime.combine(today, current_time).timestamp()

    # Übergangsverhältnis berechnen
    transition_duration = end_timestamp - start_timestamp
    time_since_start = current_timestamp - start_timestamp

    # Verhältnis als Anteil der vergangenen Zeit an der gesamten Übergangsdauer
    return time_since_start / transition_duration


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
    start_color, end_color = get_current_period(current_time, color_times)

    next_time = list(color_times.keys())[0]
    next_start_time_obj = datetime.datetime.strptime(next_time, "%H:%M").time()

    transition_ratio = calculate_transition_ratio(current_time, start_color, next_start_time_obj)
    current_color = calculate_color(start_color, end_color, transition_ratio)

    print(f"Changing keyboard color to #{current_color}.")
    try:
        subprocess.run(["msi-perkeyrgb", "--model", "GS65", "-s", current_color, "--id", vendor_and_product_id], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error setting keyboard color: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Vendor and product ID is missing.")
        print("Usage: python keyboard_color.py <vendor_and_product_id>")
        sys.exit(1)

    vendor_and_product_id = sys.argv[1]
    main(vendor_and_product_id)