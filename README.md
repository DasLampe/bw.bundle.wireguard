# Wireguard via Bundlewrap
Install and configure wireguard via bundlewrap, for client and server side.

If you specify a `port` and use the [iptables-Bundle](https://github.com/shorst/bw.bundle.iptables), we will create an iptables allow rule for forwarding traffic and open the `port` @ `interface`.

# Example Config
```python
{
    'wireguard': {
        'wg0': {
            'start_at_boot': False, # disable start at boot time
            'address': '10.10.10.1/24',
            'interface': 'main_interface',
            'port': '1337',
            'private_key': vault.decrypt('[yourEncryptedKey]').value,
            'options': {
                'PostUp': 'iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT',
                'PostDown': 'iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT',
            },
            'peers': {
                'server2': {
                    'public_key': 'SnvN1rvQIxqB4KUhbRePdzbrZzk7jKSHMdcYiTUfw1M=',
                    'allowed_ips': ['0.0.0.0/0'],
                    'endpoint': '192.168.1.1:51820',
                    'keepalive': 0,
                },
                'laptop': {
                    'public_key': 'eu2FEMZc0PH00IX42LiWTjV4tCuBWp9L8OJs2WSYuCg=',
                    'allowed_ips': ['10.10.10.10/32'],
                },
            },
        },
    },
}
```