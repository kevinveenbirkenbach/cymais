import argparse
import subprocess
import time
import os

def service_file_exists(service_name, service_type="service"):
    """Check if a systemd service file exists."""
    # Paths where service files can be stored
    path = "/etc/systemd/system/"
    service_file_name = service_name + "." + service_type
    full_path = os.path.join(path, service_file_name)
    
    print(f"Checking {full_path}")  # Added debug output
    if os.path.isfile(full_path):
        return True
    else:
        print(f"File not found.")  # Debug output if file is not found

def check_service_active(service_name):
    """Check if a service is active or activating."""
    result = subprocess.run(['systemctl', 'is-active', service_name], stdout=subprocess.PIPE)
    service_status = result.stdout.decode('utf-8').strip()
    return service_status in ['active', 'activating', 'deactivating', 'reloading']

def freeze(services_to_wait_for, ignored_services):
    # Filter services that exist and are not in the ignored list
    for service in services_to_wait_for:
        print(f"\nFreezing: {service}")
        if service in ignored_services:
            print(f"{service} will be ignored.")
        else:
            
            while check_service_active(service):
                print(f"Waiting for 5 seconds for {service} to stop...")
                time.sleep(5)
                    
            # Stop and disable the corresponding timer, if it exists
            if service_file_exists(service,"timer"):
                timer_name = service + ".timer"
                subprocess.run(['systemctl', 'stop', timer_name])
                subprocess.run(['systemctl', 'disable', timer_name])
                print(f"{timer_name} stopped and disabled.")
            else:
                print(f"Skipped.")
                
    print("\nAll required services have stopped.")

def defrost(services_to_wait_for, ignored_services):
    for service in services_to_wait_for:
        print(f"\nUnfreezing: {service}")
        if service in ignored_services:
            print(f"{service} will be ignored.")
        elif service_file_exists(service,"timer"):
            # Start and enable the corresponding timer, if it exists
            timer_name = service + ".timer"
            subprocess.run(['systemctl', 'start', timer_name])
            subprocess.run(['systemctl', 'enable', timer_name])
            print(f"{timer_name} started and enabled.")
        else:
            print(f"Skipped.")
    print("\nAll required services are started.")

def main(services_to_wait_for, ignored_services, action):
    print(f"Services to wait for: {services_to_wait_for}")
    print(f"Services to ignore: {ignored_services}")
    if action == 'freeze':
        print("Freezing services.");
        freeze(services_to_wait_for, ignored_services)
    elif action == 'defrost':
        print("Unfreezing services.");
        defrost(services_to_wait_for, ignored_services)
    print('\nOverview:')
    subprocess.run(['systemctl', 'list-timers'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='freezes and defrost systemctl services and timers')
    parser.add_argument('action', choices=['freeze', 'defrost'], help='Action to perform: freeze or defrost services.')
    parser.add_argument('services', help='Comma-separated list of services to apply the action to')
    parser.add_argument('--ignore', help='Comma-separated list of services to ignore in the action', default='')
    args = parser.parse_args()
    services_to_wait_for = args.services.split(',')
    ignored_services = args.ignore.split(',') if args.ignore else []
    main(services_to_wait_for, ignored_services,args.action)
