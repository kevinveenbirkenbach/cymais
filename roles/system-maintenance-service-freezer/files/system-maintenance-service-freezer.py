import argparse
import subprocess
import time
import os
from datetime import datetime

def parse_time_to_seconds(time_str):
    """Convert time string to seconds."""
    units = {"s": 1, "min": 60, "h": 3600}
    if time_str[-3:] in units:
        number, unit = time_str[:-3], time_str[-3:]
    elif time_str[-2:] in units:
        number, unit = time_str[:-2], time_str[-2:]
    elif time_str[-1:] in units:
        number, unit = time_str[:-1], time_str[-1:]
    else:
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
    return_value=service_status in ['active', 'activating']
    if return_value:
        print(f"Service {service_name} is active.");
    else:
        print(f"Service {service_name} is not active.");
    return return_value

def check_any_service_active(services):
    """Check if any service in the list is active or activating."""
    for service_name in services:
        if check_service_active(service_name):
            return True
    return False

def stop_timer(service):
    # Stop and disable the corresponding timer, if it exists
    if service_file_exists(service,"timer"):
        timer_name = service + ".timer"
        subprocess.run(['systemctl', 'stop', timer_name])
        subprocess.run(['systemctl', 'disable', timer_name])
        print(f"{timer_name} stopped and disabled.")
    else:
        print(f"No timer to stop.")

def filter_services(services, ignored_services):
    """
    Removes all services from the 'services' list that are contained in 'ignored_services'.
    
    :param services: List of services.
    :param ignored_services: List of services to be ignored.
    :return: Filtered list of services.
    """
    return [service for service in services if service not in ignored_services]

def stop_all_timers(services):
    for service in services:
        stop_timer(service)

def wait_for_all_services_to_stop(filtered_services,max_attempts,attempt,break_time_sec):
    for service in filtered_services:
        while check_service_active(service):
            attempt += 1
            if attempt > max_attempts:
                raise Exception(f"Error: Maximum attempts ({max_attempts}) reached. Exit.")
            print(f"{datetime.now().isoformat()}#{attempt}/{max_attempts}: Waiting for {break_time_sec} seconds for {service} to stop...")
            time.sleep(break_time_sec)
    return attempt

def freeze(filtered_services,timeout_sec):
    break_time_sec=5
    attempt=0
    max_attempts=timeout_sec/break_time_sec
    
    # This guaranties that no service will be started in the between time
    while check_any_service_active(filtered_services):
        stop_all_timers(filtered_services)
        attempt=wait_for_all_services_to_stop(filtered_services,max_attempts,attempt,break_time_sec)
        
    print("\nAll required services have stopped.")

def defrost(filtered_services):
    for service in filtered_services:
        print(f"\nUnfreezing: {service}")
        if service_file_exists(service,"timer"):
            # Start and enable the corresponding timer, if it exists
            timer_name = service + ".timer"
            subprocess.run(['systemctl', 'start', timer_name])
            subprocess.run(['systemctl', 'enable', timer_name])
            print(f"{timer_name} started and enabled.")
        else:
            print(f"No timer to activate.")
    print("\nAll required services are started.")

def main(services, ignored_services, action, timeout_sec):
    filtered_services=filter_services(services, ignored_services)
    print(f"Services to handle  : {services}")
    print(f"Services to ignore  : {ignored_services}")
    print(f"Services filtered   : {filtered_services}")
    
    if action == 'freeze':
        print("Freezing services.");
        freeze(filtered_services, timeout_sec)
    elif action == 'defrost':
        print("Unfreezing services.");
        defrost(filtered_services)
    print('\nOverview:')
    subprocess.run(['systemctl', 'list-timers'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='freezes and defrost systemctl services and timers')
    parser.add_argument('action', choices=['freeze', 'defrost'], help='Action to perform: freeze or defrost services.')
    parser.add_argument('services', nargs='+', help='List of services to apply the action to')
    parser.add_argument('--ignore', nargs='*', help='List of services to ignore in the action', default=[])
    parser.add_argument('--timeout', help='Timeout for freezing services (e.g., 1h, 30min, 45s)', default='1h')
    args = parser.parse_args()
    services = args.services
    ignored_services = args.ignore if args.ignore else []
    timeout_seconds = parse_time_to_seconds(args.timeout)
    main(services, ignored_services, args.action, timeout_seconds)
