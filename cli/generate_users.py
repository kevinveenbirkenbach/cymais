#!/usr/bin/env python3
import os
import sys
import argparse
import yaml
import glob
from collections import OrderedDict


def build_users(defs, primary_domain, start_id, become_pwd):
    """
    Build user entries with auto-incremented uid/gid, default username/email, and optional description.

    Args:
        defs (OrderedDict): Keys are user IDs, values are dicts with optional overrides.
        primary_domain (str): e.g., 'example.com'.
        start_id (int): Starting uid/gid (e.g., 1001).
        become_pwd (str): Password string for all users.

    Returns:
        OrderedDict: Merged user definitions with full fields.

    Raises:
        ValueError: If duplicate override uids/gids or conflicts in generated values.
    """
    users = OrderedDict()
    used_uids = set()
    
    # Pre-collect any provided uids/gids and check for duplicates
    for key, overrides in defs.items():
        if 'uid' in overrides:
            uid = overrides['uid']
            if uid in used_uids:
                raise ValueError(f"Duplicate uid {uid} for user '{key}'")
            used_uids.add(uid)

    next_free = start_id
    def allocate_free_id():
        nonlocal next_free
        # find next free id not in used_uids
        while next_free in used_uids:
            next_free += 1
        free = next_free
        used_uids.add(free)
        next_free += 1
        return free

    # Build entries
    for key, overrides in defs.items():
        username = overrides.get('username', key)
        email = overrides.get('email', f"{username}@{primary_domain}")
        description = overrides.get('description')
        password = overrides.get('password',become_pwd)
        # UID assignment
        if 'uid' in overrides:
            uid = overrides['uid']
        else:
            uid = allocate_free_id()
        gid = overrides.get('gid',uid)

        entry = {
            'username': username,
            'email':    email,
            'password': password,
            'uid':      uid,
            'gid':      gid
        }
        if description is not None:
            entry['description'] = description
        if overrides.get('is_admin', False):
            entry['is_admin'] = True

        users[key] = entry

    # Validate uniqueness of username, email, and gid
    seen_usernames = set()
    seen_emails = set()
    seen_gids = set()
    for key, entry in users.items():
        un = entry['username']
        em = entry['email']
        gd = entry['gid']
        if un in seen_usernames:
            raise ValueError(f"Duplicate username '{un}' in merged users")
        if em in seen_emails:
            raise ValueError(f"Duplicate email '{em}' in merged users")
        seen_usernames.add(un)
        seen_emails.add(em)
        seen_gids.add(gd)

    return users


def load_user_defs(roles_dir):
    """
    Scan all roles/*/meta/users.yml files and extract 'users:' sections.

    Raises an exception if conflicting definitions are found.

    Args:
        roles_dir (str): Path to the directory containing role subdirectories.

    Returns:
        OrderedDict: Merged user definitions.

    Raises:
        ValueError: On invalid format or conflicting field values.
    """
    pattern = os.path.join(roles_dir, '*/meta/users.yml')
    files = sorted(glob.glob(pattern))
    merged = OrderedDict()

    for filepath in files:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f) or {}
        users = data.get('users', {})
        if not isinstance(users, dict):
            continue

        for key, overrides in users.items():
            if not isinstance(overrides, dict):
                raise ValueError(f"Invalid definition for user '{key}' in {filepath}")

            if key not in merged:
                merged[key] = overrides.copy()
            else:
                existing = merged[key]
                for field, value in overrides.items():
                    if field in existing and existing[field] != value:
                        raise ValueError(
                            f"Conflict for user '{key}': field '{field}' has existing value "
                            f"'{existing[field]}', tried to set '{value}' in {filepath}"
                        )
                existing.update(overrides)

    return merged


def dictify(data):
    """
    Recursively convert OrderedDict to regular dict before YAML dump.
    """
    if isinstance(data, OrderedDict):
        return {k: dictify(v) for k, v in data.items()}
    if isinstance(data, dict):
        return {k: dictify(v) for k, v in data.items()}
    if isinstance(data, list):
        return [dictify(v) for v in data]
    return data


def parse_args():
    parser = argparse.ArgumentParser(
        description='Generate a users.yml by merging all roles/*/meta/users.yml users sections.'
    )
    parser.add_argument(
        '--roles-dir', '-r', required=True,
        help='Directory containing roles (e.g., roles/*/meta/users.yml).'
    )
    parser.add_argument(
        '--output', '-o', required=True,
        help='Path to the output YAML file (e.g., users.yml).'
    )
    parser.add_argument(
        '--start-id', '-s', type=int, default=1001,
        help='Starting uid/gid number (default: 1001).'
    )
    parser.add_argument(
        '--extra-users', '-e',
        help='Comma-separated list of additional usernames to include.',
        default=None
    )
    return parser.parse_args()


def main():
    args = parse_args()
    primary_domain = '{{ primary_domain }}'
    become_pwd = '{{ lookup("password", "/dev/null length=42 chars=ascii_letters,digits") }}'

    try:
        user_defs = load_user_defs(args.roles_dir)
    except ValueError as e:
        print(f"Error merging user definitions: {e}", file=sys.stderr)
        sys.exit(1)

    # Add extra users if any
    if args.extra_users:
        for name in args.extra_users.split(','):
            user = name.strip()
            if not user:
                continue
            if user in user_defs:
                print(f"Warning: extra user '{user}' already defined; skipping.", file=sys.stderr)
            else:
                user_defs[user] = {}

    try:
        users = build_users(
            defs=user_defs,
            primary_domain=primary_domain,
            start_id=args.start_id,
            become_pwd=become_pwd
        )
    except ValueError as e:
        print(f"Error building user entries: {e}", file=sys.stderr)
        sys.exit(1)

    default_users = {'default_users': users}
    plain_data = dictify(default_users)

    # Ensure strings are represented without Python-specific tags
    yaml.SafeDumper.add_representer(
        str,
        lambda dumper, data: dumper.represent_scalar('tag:yaml.org,2002:str', data)
    )

    with open(args.output, 'w') as f:
        yaml.safe_dump(
            plain_data,
            f,
            default_flow_style=False,
            sort_keys=False,
            width=120
        )

if __name__ == '__main__':
    main()
