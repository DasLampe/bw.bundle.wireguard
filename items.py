global node

owner = 'root'
group = 'root'

files = {}
actions = {}

pkg_apt = {
    'wireguard': {
        'installed': True,
    }
}

directories = {
    '/etc/wireguard': {
        'owner': 'root',
        'group': 'root',
        'mode': '0700',
    }
}

svc_systemd = {
}

for name, config in node.metadata.get('wireguard', {}).items():
    svc_systemd[f'wg-quick@{name}.service'] = {
        'enabled': config.get('start_at_boot', False),
        'running': None,
        'needs': [
            f'tag:wireguard_{name}_privatekey',
            f'pkg_apt:wireguard',
        ]
    }

    if config.get('private_key', ""):
        files[f"/etc/wireguard/{name}_privatekey"] = {
            'content': config.get('private_key'),
            'owner': owner,
            'group': group,
            'tags': [
                f'wireguard_{name}_privatekey',
            ],
            'needs': [
                'directory:/etc/wireguard',
            ],
        }
    else:
        actions[f"generate_wireguard_{name}_privatekey"] = {
            'command': f"wg genkey > /etc/wireguard/{name}_privatekey && chown {owner}:{group} /etc/wireguard/{name}_privatekey",
            'needs': [
                'pkg_apt:wireguard',
                'directory:/etc/wireguard',
            ],
            'tags': [
                f"wireguard_{name}_privatekey",
            ],
            'unless': f'test -f /etc/wireguard/{name}_privatekey',
        }

    files[f"/etc/wireguard/{name}.conf"] = {
        'source': 'etc/wireguard/wg.conf.jinja2',
        'content_type': 'jinja2',
        'context': {
            'name': name,
            'cfg': config,
        },
        'needs': [
            'directory:/etc/wireguard',
        ],
        'triggers': [
            f'svc_systemd:wg-quick@{name}.service:restart'
        ]
    }
