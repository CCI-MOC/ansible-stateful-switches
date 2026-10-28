# cci_moc.stateful_switches.save

Saves the running configuration of a switch to its startup configuration.

The role picks the switch OS from `ansible_network_os` and skips other hosts.

| `ansible_network_os` | Switch OS | Needs |
|----------------------|-----------|-------|
| `dellemc.os9.os9` | Dell OS9 | the `dellemc.os9` collection |
| `cisco.nxos.nxos` | Cisco NXOS | the `cisco.nxos` collection |
| `nvidia.nvue` | NVIDIA Cumulus Linux 5 (NVUE) | any SSH connection, for example `ansible.netcommon.libssh` |

On NVUE switches this saves the applied configuration, so pending changes that were never
applied are not saved. The `configure` role already saves after it makes changes, so this
role is for saving changes made by hand.

## Example

```yaml
- name: Save switch configuration
  hosts: all
  gather_facts: false
  roles:
    - cci_moc.stateful_switches.save
```
