import colorsys

def adjust_color(hex_color, lightness_change=0, hue_shift=0, saturation_change=0):
    """
    Adjust a HEX color in HSL space.
    @See https://chatgpt.com/c/67b08ad4-eb58-800f-80cc-f1b22d8c64f3
    
    - lightness_change: Percentage points to add or subtract from lightness (0-100 => 0-1 in HSL).
    - hue_shift: Degrees to shift hue (e.g., +180 for complementary).
    - saturation_change: Percentage points to add or subtract from saturation (0-100 => 0-1 in HSL).
    
    Uses a 'cyclical' approach for lightness and saturation:
      If the new value goes above 1, it wraps around (subtract 1).
      If it goes below 0, it wraps around (add 1).
    This creates strong contrast when crossing boundaries.
    """

    # Strip leading '#' if present
    hex_color = hex_color.lstrip('#')
    
    # Parse the original RGB values
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # Convert from [0..255] range to [0..1] for colorsys
    r /= 255.0
    g /= 255.0
    b /= 255.0
    
    # Convert RGB -> HLS (note: in Python, it's Hue, Lightness, Saturation)
    # Hue, Lightness, Saturation are each in [0..1]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Shift hue by (hue_shift / 360)
    # e.g., hue_shift=180 => shift by 0.5 in HLS space
    h = (h + (hue_shift / 360.0)) % 1.0
    
    # Shift saturation (cyc wrap)
    # saturation_change is e.g. +20 => +0.20 in HLS
    s_new = s + (saturation_change / 100.0)
    if s_new > 1:
        s_new -= 1
    elif s_new < 0:
        s_new += 1
    
    # Shift lightness (cyc wrap)
    # lightness_change is e.g. +30 => +0.30 in HLS
    l_new = l + (lightness_change / 100.0)
    if l_new > 1:
        l_new -= 1
    elif l_new < 0:
        l_new += 1
    
    # Convert back to RGB
    new_r, new_g, new_b = colorsys.hls_to_rgb(h, l_new, s_new)
    
    # Scale back to [0..255]
    new_r = int(new_r * 255)
    new_g = int(new_g * 255)
    new_b = int(new_b * 255)
    
    return '#{:02x}{:02x}{:02x}'.format(new_r, new_g, new_b)

class FilterModule(object):
    '''Custom filters for Ansible'''
    def filters(self):
        return {
            'adjust_color': adjust_color,
        }