# cci_moc.stateful_switches.save

Saves the running configuration of a switch to its startup configuration.

Supports Dell OS9 (`ansible_network_os=dellemc.os9.os9`) and needs the `dellemc.os9`
collection. Other hosts are skipped. The `configure` role already saves after it makes
changes, so this role is for saving changes made by hand.

## Example

```yaml
- name: Save switch configuration
  hosts: all
  gather_facts: false
  roles:
    - cci_moc.stateful_switches.save
```
