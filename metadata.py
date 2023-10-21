defaults = {}

@metadata_reactor
def add_iptables(metadata):
    if not node.has_bundle("iptables"):
        raise DoNotRunAgain

    iptables_rules = {}
    for name,conf in metadata.get('wireguard').items():
        iptables_rules += repo.libs.iptables.accept(). \
            input('main_interface'). \
            udp(). \
            dest_port(metadata.get('wireguard').get(name).get('port')). \
            comment(f'wireguard {name}')

        # Ignore forward rules
        iptables_rules += repo.libs.iptables.jump('ACCEPT').chain('FORWARD').output(name).ignore()
        iptables_rules += repo.libs.iptables.jump('ACCEPT').chain('FORWARD').input(name).ignore()

    return iptables_rules
