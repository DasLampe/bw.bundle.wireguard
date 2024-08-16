defaults = {}

@metadata_reactor
def add_iptables(metadata):
    if not node.has_bundle("iptables"):
        raise DoNotRunAgain

    iptables_rules = {}
    for name,conf in metadata.get('wireguard').items():
        if metadata.get('wireguard').get(name).get('port', False):
            iptables_rules += repo.libs.iptables.accept(). \
                input(conf.get('interface', 'main_interface')). \
                udp(). \
                dest_port(metadata.get('wireguard').get(name).get('port')). \
                comment(f'wireguard {name}')

    return iptables_rules
