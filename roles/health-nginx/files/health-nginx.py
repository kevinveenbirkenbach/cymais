import os
import requests
import sys
import re

# Define the path to the nginx configuration directory
config_path = '{{nginx_servers_directory}}'

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
        url = f"https://{name}"
        
        # Default: Expect status code 200 for a domain
        expected_statuses = [200]
        
        # Determine expected status codes based on subdomain
        if len(parts) == 3:
            if parts[0] == 'listmonk':
                expected_statuses = [401]
            elif parts[0] == 'www':
                expected_statuses = [200,301]
            elif parts[0] == 's':
                expected_statuses = [403]

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
