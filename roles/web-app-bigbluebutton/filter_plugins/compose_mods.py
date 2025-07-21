import re
import yaml

def compose_mods(yml_text, docker_repository_path, env_file):
    yml_text = re.sub(r'\./data/postgres:/var/lib/postgresql/data', 'database:/var/lib/postgresql/data', yml_text)
    yml_text = re.sub(r'\./data/bigbluebutton:/var/bigbluebutton', 'bigbluebutton:/var/bigbluebutton', yml_text)
    yml_text = re.sub(r'\./data/freeswitch-meetings:/var/freeswitch/meetings', 'freeswitch:/var/freeswitch/meetings', yml_text)
    yml_text = re.sub(r'\./data/greenlight:/usr/src/app/storage', 'greenlight:/usr/src/app/storage', yml_text)
    yml_text = re.sub(r'\./data/mediasoup:/var/mediasoup', 'mediasoup:/var/mediasoup', yml_text)
    yml_text = re.sub(r'\./', docker_repository_path + '/', yml_text)
    yml_text = re.sub(
        r'(^\s*context:\s*)' + re.escape(docker_repository_path) + r'/mod/(.*)',
        r'\1' + docker_repository_path + r'/mod/\2',
        yml_text, flags=re.MULTILINE
    )
    yml_text = re.sub(
        r'(^\s*context:\s*)mod/(.*)',
        r'\1' + docker_repository_path + r'/mod/\2',
        yml_text, flags=re.MULTILINE
    )

    try:
        data = yaml.safe_load(yml_text)
        services = data.get('services', {})
        for name, svc in services.items():
            svc['env_file'] = [env_file]
            if name == 'redis':
                vols = svc.get('volumes')
                if not vols or not isinstance(vols, list):
                    svc['volumes'] = ['redis:/data']
                elif 'redis:/data' not in vols:
                    svc['volumes'].append('redis:/data')
            if name == 'coturn':
                vols = svc.get('volumes')
                if not vols or not isinstance(vols, list):
                    svc['volumes'] = ['coturn:/var/lib/coturn']
                elif 'coturn:/var/lib/coturn' not in vols:
                    svc['volumes'].append('coturn:/var/lib/coturn')
            if name == 'bbb-graphql-server':
                svc['healthcheck'] = {
                    'test': ['CMD', 'curl', '-f', 'http://localhost:8085/healthz'],
                    'interval': '30s',
                    'timeout': '10s',
                    'retries': 5,
                    'start_period': '10s'
                }
        data['services'] = services

        # **ADD THIS BLOCK:**
        # Only add volumes block if not present
        if 'volumes' not in data:
            data['volumes'] = {
                'database': None,
                'greenlight': None,
                'redis': None,
                'coturn': None,
                'freeswitch': None,
                'bigbluebutton': None,
                'mediasoup': None
            }

        yml_text = yaml.dump(data, default_flow_style=False, sort_keys=False)
    except Exception:
        pass

    return yml_text

class FilterModule(object):
    def filters(self):
        return {
            'compose_mods': compose_mods,
        }
