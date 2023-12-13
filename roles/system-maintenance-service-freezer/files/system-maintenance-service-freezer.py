import argparse
import subprocess
import time


def check_service_active(service_name):
    """Check if a service is active."""
    result = subprocess.run(['systemctl', 'is-active', service_name], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').strip() == 'active'

def service_exists(service_name):
    """Check if a service exists."""
    result = subprocess.run(['systemctl', 'status', service_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def freeze(services_to_wait_for, ignored_services):
    # Filter services that exist and are not in the ignored list
    active_services = [service for service in services_to_wait_for if service_exists(service) and service not in ignored_services]

    while active_services:
        for service in active_services:
            if not check_service_active(service):
                print(f"{service} stopped.")
                # Disable the service
                subprocess.run(['systemctl', 'disable', service])
                print(f"{service} disabled.")

                # Stop and disable the corresponding timer, if it exists
                timer_name = service + ".timer"
                timer_check = subprocess.run(['systemctl', 'list-timers', '--all', timer_name], stdout=subprocess.PIPE)
                if timer_name in timer_check.stdout.decode():
                    subprocess.run(['systemctl', 'stop', timer_name])
                    subprocess.run(['systemctl', 'disable', timer_name])
                    print(f"{timer_name} stopped and disabled.")
                active_services.remove(service)
            else:
                print(f"Waiting for {service} to stop...")
        time.sleep(5)
    print("All required services have stopped.")

def defrost(services_to_wait_for, ignored_services):
    for service in services_to_wait_for:
        if service not in ignored_services and service_exists(service):
            # Enable the service
            subprocess.run(['systemctl', 'enable', service])
            print(f"{service} enabled.")

            # Start and enable the corresponding timer, if it exists
            timer_name = service + ".timer"
            timer_check = subprocess.run(['systemctl', 'list-timers', '--all', timer_name], stdout=subprocess.PIPE)
            if timer_name in timer_check.stdout.decode():
                subprocess.run(['systemctl', 'start', timer_name])
                subprocess.run(['systemctl', 'enable', timer_name])
                print(f"{timer_name} started and enabled.")

def main(services_to_wait_for, ignored_services, action):
    if action == 'freeze':
        # Code to handle freeze action
        freeze(services_to_wait_for, ignored_services)
    elif action == 'defrost':
        defrost(services_to_wait_for, ignored_services)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='freezes and defrost systemctl services and timers')
    parser.add_argument('action', choices=['freeze', 'defrost'], help='Action to perform: freeze or defrost services.')
    parser.add_argument('services', help='Comma-separated list of services to apply the action to')
    parser.add_argument('--ignore', help='Comma-separated list of services to ignore in the action', default='')
    args = parser.parse_args()
    services_to_wait_for = args.services.split(',')
    ignored_services = args.ignore.split(',') if args.ignore else []
    main(services_to_wait_for, ignored_services,args.action)
