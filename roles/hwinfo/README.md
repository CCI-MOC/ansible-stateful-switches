# cci_moc.stateful_switches.hwinfo

Prints the serial number of a switch.

Supports Dell OS9 (`ansible_network_os=dellemc.os9.os9`) and needs the `dellemc.os9`
collection. Other hosts are skipped.

## Example

```yaml
- name: Gather hardware information
  hosts: all
  gather_facts: false
  roles:
    - cci_moc.stateful_switches.hwinfo
```
