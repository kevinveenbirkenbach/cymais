def adjust_color(hex_color, amount):
    # Remove the leading '#' if present
    hex_color = hex_color.lstrip('#')
    
    # Extract the RGB components
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # Adjust the values, ensuring they remain within the range 0-255
    r = max(0, min(255, r + amount))
    g = max(0, min(255, g + amount))
    b = max(0, min(255, b + amount))
    
    # Convert the values back into a hexadecimal string
    return '#{0:02x}{1:02x}{2:02x}'.format(r, g, b)

class FilterModule(object):
    '''Custom filters for Ansible'''
    def filters(self):
        return {
            'adjust_color': adjust_color,
        }