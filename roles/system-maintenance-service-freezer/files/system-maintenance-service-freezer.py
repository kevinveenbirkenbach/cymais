import argparse
import subprocess
import time
import os

def parse_time_to_seconds(time_str):
    """Convert time string to seconds."""
    units = {"s": 1, "min": 60, "h": 3600}
    number, unit = time_str[:-1], time_str[-1]
    if unit not in units:
        raise ValueError("Invalid time unit")
    return int(number) * units[unit]

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
    return service_status in ['active', 'activating']

def freeze(services_to_wait_for, ignored_services, timeout_sec):
    break_time_sec=5
    attempt=0
    max_attempts=timeout_sec/break_time_sec
    # Filter services that exist and are not in the ignored list
    for service in services_to_wait_for:
        print(f"\nFreezing: {service}")
        if service in ignored_services:
            print(f"{service} will be ignored.")
        else:
            while check_service_active(service):
                current_time_iso = datetime.now().isoformat()
                attempt += 1
                print(f"{current_time_iso}#{attempt}/{max_attempts}: Waiting for {break_time_sec} seconds for {service} to stop...")
                time.sleep(break_time_sec)
                if attempt > max_attempts:
                    raise Exception(f"Error: Maximum attempts ({max_attempts}) reached. Exit.")
                    
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

def main(services_to_wait_for, ignored_services, action, timeout_sec):
    print(f"Services to wait for: {services_to_wait_for}")
    print(f"Services to ignore: {ignored_services}")
    if action == 'freeze':
        print("Freezing services.");
        freeze(services_to_wait_for, ignored_services, timeout_sec)
    elif action == 'defrost':
        print("Unfreezing services.");
        defrost(services_to_wait_for, ignored_services)
    print('\nOverview:')
    subprocess.run(['systemctl', 'list-timers'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='freezes and defrost systemctl services and timers')
    parser.add_argument('action', choices=['freeze', 'defrost'], help='Action to perform: freeze or defrost services.')
    parser.add_argument('services', nargs='+', help='List of services to apply the action to')
    parser.add_argument('--ignore', nargs='*', help='List of services to ignore in the action', default=[])
    parser.add_argument('--timeout', help='Timeout for freezing services (e.g., 1h, 30min, 45s)', default='1h')

    args = parser.parse_args()
    services_to_wait_for = args.services
    ignored_services = args.ignore if args.ignore else []
    timeout_seconds = parse_time_to_seconds(args.timeout)
    main(services_to_wait_for, ignored_services, args.action, timeout_seconds)
