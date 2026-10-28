# cci_moc.stateful_switches.hwinfo

Prints the serial number of a switch.

The role picks the switch OS from `ansible_network_os` and skips other hosts.

| `ansible_network_os` | Switch OS | Needs |
|----------------------|-----------|-------|
| `dellemc.os9.os9` | Dell OS9 | the `dellemc.os9` collection |
| `cisco.nxos.nxos` | Cisco NXOS | the `cisco.nxos` collection |
| `nvidia.nvue` | NVIDIA Cumulus Linux 5 (NVUE) | any SSH connection, for example `ansible.netcommon.libssh` |

## Example

```yaml
- name: Gather hardware information
  hosts: all
  gather_facts: false
  roles:
    - cci_moc.stateful_switches.hwinfo
```
