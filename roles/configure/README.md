# cci_moc.stateful_switches.configure

Makes a switch match its interface and VLAN manifests, then saves the configuration.

Each run reads the switch configuration, generates the commands that make it match the
`interfaces` and `vlans` variables, and applies them. Interfaces and VLANs that were
removed from the manifests are removed from the switch.

## Supported Switches

The role picks the switch OS from `ansible_network_os` and skips other hosts.

| `ansible_network_os` | Switch OS | Needs |
|----------------------|-----------|-------|
| `dellemc.os9.os9` | Dell OS9 | the `dellemc.os9` collection |
| `cisco.nxos.nxos` | Cisco NXOS | the `cisco.nxos` collection |
| `nvidia.nvue` | NVIDIA Cumulus Linux 5 (NVUE) | any SSH connection, for example `ansible.netcommon.libssh` |

## Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `interfaces` | yes | The interface manifest, keyed by interface name |
| `vlans` | yes | The VLAN manifest. A VLAN is configured only on hosts in at least one of the inventory groups in its `fabrics` |
| `diff_only` | no, default `false` | Stage the changes and show the diff without applying them. Only NVUE switches honor this |

The manifest fields are listed in the
[collection README](https://github.com/CCI-MOC/ansible-stateful-switches#manifest-fields).

## Example

```yaml
- name: Configure switches
  hosts: all
  gather_facts: false
  roles:
    - cci_moc.stateful_switches.configure
```
