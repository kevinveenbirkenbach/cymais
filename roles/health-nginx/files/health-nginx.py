import os
import requests
import sys
import re

# Define the path to the nginx configuration directory
config_path = '/etc/nginx/conf.d/'

# Initialize the error counter
error_counter = 0

# Regex pattern to match domain.tld or subdomain.domain.tld
pattern = re.compile(r"^(?:[\w-]+\.)?[\w-]+\.[\w-]+\.conf$")

# Iterate over each file in the configuration directory
for filename in os.listdir(config_path):
    if filename.endswith('.conf') and pattern.match(filename):
        # Extract the domain and subdomain from the filename
        name = filename.replace('.conf', '')
        parts = name.split('.')
        
        # Prepare the URL and expected status codes
        url = f"http://{name}"
        
        # Determine expected status codes based on subdomain
        if len(parts) == 3 and parts[0] == 'www':
            expected_statuses = [200,301]
        elif len(parts) == 3 and parts[0] == 's':
            expected_statuses = [403]
        elif len(parts) <= 3:
            # For domain.tld where no specific subdomain is present
            expected_statuses = [200, 301]
        else:
            # Skip files that don't match the schema
            continue

        try:
            # Send a HEAD request to get only the response header
            response = requests.head(url, allow_redirects=True)

            # Check if the status code matches the expected statuses
            if response.status_code in expected_statuses:
                print(f"{name}: ok")
            else:
                print(f"{name}: error")
                error_counter += 1
        except requests.RequestException as e:
            # Handle exceptions for requests like connection errors
            print(f"{name}: error due to {e}")
            error_counter += 1

# Exit the script with the number of errors as the exit code
sys.exit(error_counter)
