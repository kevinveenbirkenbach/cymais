import argparse
import subprocess
import time
import os
from datetime import datetime

def parse_time_to_seconds(time_str):
    """
    Convert a time string (e.g., '1h', '30min', '45s') to seconds.
    """
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
    """
    Check if a systemd service file of a given type exists for a service.
    """
    path = "/etc/systemd/system/"
    service_file_name = f"{service_name}.{service_type}"
    full_path = os.path.join(path, service_file_name)
    
    # Debug output for checking the service file existence
    print(f"Checking {full_path}")
    return os.path.isfile(full_path)

def check_service_active(service_name):
    """
    Check if a systemd service is currently active or activating.
    """
    result = subprocess.run(['systemctl', 'is-active', service_name], stdout=subprocess.PIPE)
    service_status = result.stdout.decode('utf-8').strip()
    is_active = service_status in ['active', 'activating']
    print(f"Service {service_name} is {'active' if is_active else 'not active'}.")
    return is_active

def check_any_service_active(services):
    """
    Check if any service in a given list is active or activating.
    """
    return any(check_service_active(service) for service in services)

def stop_timer(service):
    """
    Stop and disable a systemd timer for a service if it exists.
    """
    if service == "system-maintenance-service-defrost":
        print(f"Ignoring {service}. It's the initializer of freezer.")
    if service_file_exists(service, "timer"):
        timer_name = f"{service}.timer"
        subprocess.run(['systemctl', 'stop', timer_name])
        subprocess.run(['systemctl', 'disable', timer_name])
        print(f"{timer_name} stopped and disabled.")
    else:
        print("No timer to stop for service.")

def filter_services(services, ignored_services):
    """
    Filter out services that are in the ignored_services list from services list.
    """
    return [service for service in services if service not in ignored_services]

def stop_all_timers(services):
    """
    Stop and disable timers for all services in a given list.
    """
    for service in services:
        stop_timer(service)

def wait_for_all_services_to_stop(filtered_services, max_attempts, attempt, break_time_sec):
    """
    Wait until all services in the list have stopped, with a maximum number of attempts.
    """
    for service in filtered_services:
        while check_service_active(service):
            attempt += 1
            if attempt > max_attempts:
                raise Exception(f"Maximum attempts ({max_attempts}) reached. Exiting.")
            print(f"{datetime.now().isoformat()}#{attempt}/{max_attempts}: Waiting for {break_time_sec} seconds for {service} to stop...")
            time.sleep(break_time_sec)
    return attempt

def freeze(filtered_services, timeout_sec):
    """
    Freeze services by stopping them and their timers, waiting up to a timeout.
    """
    break_time_sec = 5
    attempt = 0
    max_attempts = timeout_sec / break_time_sec
    
    while check_any_service_active(filtered_services):
        stop_all_timers(filtered_services)
        attempt = wait_for_all_services_to_stop(filtered_services, max_attempts, attempt, break_time_sec)
    print("All required services have stopped.")

def defrost(filtered_services):
    """
    Defrost services by starting and enabling their timers.
    """
    break_time_sec = 5
    attempt = 0
    max_attempts = timeout_sec / break_time_sec
    wait_for_all_services_to_stop(filtered_services, max_attempts, attempt, break_time_sec)

    for service in filtered_services:
        print(f"Unfreezing: {service}")
        if service_file_exists(service, "timer"):
            timer_name = f"{service}.timer"
            subprocess.run(['systemctl', 'start', timer_name])
            subprocess.run(['systemctl', 'enable', timer_name])
            print(f"{timer_name} started and enabled.")
        else:
            print("No timer to activate for service.")
    print("All required services are started.")

def main(services, ignored_services, action, timeout_sec):
    """
    Main function to process the command-line arguments and perform actions.
    """
    
    # Ignoring the current running service
    running_service=f"system-maintenance-service-{action}"
    if running_service not in ignored_services:
        ignored_services.append(running_service)
        
    filtered_services = filter_services(services, ignored_services)
    print(f"Services to handle: {services}")
    print(f"Services to ignore: {ignored_services}")
    print(f"Services filtered: {filtered_services}")
    
    if action == 'freeze':
        print("Freezing services.")
        freeze(filtered_services, timeout_sec)
    elif action == 'defrost':
        print("Unfreezing services.")
        defrost(filtered_services, timeout_sec)
    print("Overview:")
    subprocess.run(['systemctl', 'list-timers'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Freezes and defrosts systemd services and timers.')
    parser.add_argument('action', choices=['freeze', 'defrost'], help='Action to perform: freeze or defrost services.')
    parser.add_argument('services', nargs='+', help='List of services to apply the action to.')
    parser.add_argument('--ignore', nargs='*', help='List of services to ignore in the action.', default=[])
    parser.add_argument('--timeout', help='Timeout for freezing services (e.g., 1h, 30min, 45s).', default='1h')
    args = parser.parse_args()
    services = args.services
    ignored_services = args.ignore if args.ignore else []
    timeout_seconds = parse_time_to_seconds(args.timeout)
    main(services, ignored_services, args.action, timeout_seconds)
