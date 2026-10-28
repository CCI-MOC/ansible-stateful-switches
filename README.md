# cci_moc.stateful_switches

An Ansible collection that keeps switches in line with YAML manifests of their
interfaces and VLANs. Each run makes the switch match the manifests: what is in them is
configured, and interfaces and VLANs that were removed from them are removed from the
switch.

## Supported Switch OSes

| Switch OS | `ansible_network_os` | Collection needed | Connection |
|-----------|----------------------|-------------------|------------|
| Dell OS9 (FTOS9) | `dellemc.os9.os9` | `dellemc.os9` | `ansible.netcommon.network_cli` |
| Cisco NXOS | `cisco.nxos.nxos` | `cisco.nxos` | `ansible.netcommon.network_cli` |
| NVIDIA Cumulus Linux 5.X (NVUE) | `nvidia.nvue` | none | any SSH connection, for example `ansible.netcommon.libssh` |

The switch collections are not dependencies of this collection, so install the ones for
the switches you have. NVUE switches are configured with `ansible.builtin.raw`, and
`nvidia.nvue` is only the value the `configure` role looks for. The
`ansible.netcommon.libssh` connection needs the `ansible-pylibssh` Python package.

On Dell OS9, if the switch account does not log in at privilege level 15, set
`ansible_become: true` and `ansible_become_method: enable` in the inventory.

## Installation

```
ansible-galaxy collection install cci_moc.stateful_switches
```

Or in `requirements.yml`:

```yaml
collections:
  - name: cci_moc.stateful_switches
```

## Usage

Inventory, where the groups are the fabrics VLANs are assigned to:

```ini
[core]
spine1 ansible_host=192.0.2.1 ansible_network_os=cisco.nxos.nxos ansible_connection=ansible.netcommon.network_cli
leaf1 ansible_host=192.0.2.11 ansible_network_os=nvidia.nvue ansible_connection=ansible.netcommon.libssh
```

`group_vars/all/vlans.yaml`:

```yaml
vlans:
  - id: 105
    name: PUBLIC
    description: Public VLAN
    fabrics:
      - core
  - id: 200
    name: STORAGE
    description: Storage VLAN
    fabrics:
      - core
```

`host_vars/leaf1/interfaces.yaml`:

```yaml
interfaces:
  swp1:
    description: server1
    portmode: access
    untagged: 105
  swp2:
    description: server2 port 1
  swp3:
    description: server2 port 2
  bond1:
    description: server2
    lacp-members-active:
      - swp2
      - swp3
    portmode: trunk
    tagged:
      - 105
      - 200
```

Playbook:

```yaml
- name: Configure switches
  hosts: all
  gather_facts: false
  roles:
    - cci_moc.stateful_switches.configure
```

On NVUE switches, run with `-e diff_only=true` to see the changes without applying them.

### Roles

| Role | Description |
|------|-------------|
| `configure` | Makes the switch match the `interfaces` and `vlans` manifests, then saves the configuration |
| `save` | Saves the running configuration to the startup configuration (Dell OS9) |
| `hwinfo` | Prints the switch serial number (Dell OS9) |

Run `ansible-doc -t role cci_moc.stateful_switches.configure` for the role variables.

### Filters

The roles are built on these filters, which you can use in your own tasks. They read the
current switch configuration and the manifests, and return the commands to apply.

| Filter | Switch OS | Returns |
|--------|-----------|---------|
| `filter_vlans` | all | The VLANs of the manifest that belong on a host, in the form the other filters take |
| `os9_fanoutcfg` | Dell OS9 | Commands that add and remove port fanouts |
| `os9_getconfig` | Dell OS9 | Configuration blocks of the interfaces that need changing |
| `os9_cleanintf` | Dell OS9 | Commands that delete VLAN interfaces and port channels that left the manifest |
| `nxos_getconfig` | Cisco NXOS | The whole configuration, for `configure replace` |
| `nvue_prepconfig` | Cumulus Linux | Commands that set the hostname, bridge and auto save |
| `nvue_getconfig` | Cumulus Linux | Commands that make the interfaces and bridge VLANs match the manifests |

Run `ansible-doc -t filter cci_moc.stateful_switches.<filter>` for the arguments and
examples.

## Interface Parameter Compatibility Matrix

| Parameter | Dell OS9 | Cisco NXOS | Cumulus Linux 5 |
|-----------|----------|------------|-----------------|
| description | ✅ | ✅ | ✅ |
| state | ✅ | ✅ | ✅ |
| mtu | ✅ | ✅ | ✅ |
| fec | ✅ | ✅ | ✅ |
| autoneg | ✅ | ✅ | ✅ |
| speed | ❌ | ✅ | ✅ |
| stp/edgeport | ✅ | ✅ | ✅ |
| stp/bpduguard | ✅ | ✅ | ✅ |
| stp/rootguard | ✅ | ✅ | ✅ |
| stp/disabled | ✅ | ✅ | ✅ |
| fanout | ✅ | ✅ | ✅ |
| managed | ✅ | ✅ | ✅ |
| allowlist | ✅ | ❌ | ❌ |
| blocklist | ✅ | ❌ | ❌ |
| portmode | ✅ | ✅ | ✅ |
| untagged | ✅ | ✅ | ✅ |
| tagged | ✅ | ✅ | ✅ |
| ip4 | ✅ | ✅ | ✅ |
| ip6 | ✅ | ✅ | ✅ |
| gateway | ❌ | ❌ | ✅ |
| lag-members | ✅ | ✅ | ✅ |
| lacp-members-active | ✅ | ✅ | ✅ |
| lacp-members-passive | ✅ | ✅ | ❌ |
| lacp-rate | ✅ | ✅ | ✅ |
| lacp-bypass | ❌ | ❌ | ✅ |
| mlag | ✅ | ✅ | ✅ |

## Manifest Fields

### VLAN

* `id` VLAN 802.1q tag (Integer)
* `name` Identifying name for the vlan (String)
* `description` Description for the vlan (String)
* `managed` Don't create nor destroy this VLAN (Boolean)
* `fabrics` Inventory groups whose hosts get this VLAN. A VLAN without fabrics is not configured anywhere (List of strings)

### Interface

* `description` Sets the description of the interface. (String)
* `state` Sets the admin state of the mode ("up", or "down")
* `mtu` Sets the MTU of the interface (Integer 576-9416, 552-9216 on Cumulus)
* `fec` If false, forward-error-correction is disabled on the interface (Boolean)
* `autoneg` If false, auto-negotiation is disabled on the interface (Boolean)
* `speed` Sets the link speed of the interface (Cumulus: String such as `"25G"`, `"200G"`, `"100M"` or `"auto"`)
* `stp` Sets STP Parameters
  * `edgeport` Sets whether port should be an edge port (Boolean)
  * `bpduguard` Enables BPDUguard on an interface (Boolean)
  * `rootguard` Enables Rootguard on an interface (Boolean)
  * `disabled` Disables STP on the interface (Boolean)
* `fanout` Sets fanout configuration
  * `type` Sets the fanout type (`single`, `dual`, or `quad`, and `octal` on Cumulus)
  * `speed` Sets the fanout speed (`10G`, `25G`, or `40G`)
* `managed` If true, this interface will not be configured by ansible. Works for both VLANs and interfaces (Boolean)
* `allowlist` Only allow modification of these fields (List of Strings)
* `blocklist` Block modification of these fields (List of Strings)
* `portmode` L2 portmode of an interface (String "access", "trunk", or "hybrid")
* `untagged` Single vlan to untag, requires portmode access or hybrid (Integer 2-4094)
* `tagged` List of vlans to tag, requires portmode trunk or hybrid (List of Integers 2-4094)
* `ip4` Sets the IPv4 address of the interface (String "X.X.X.X/YY")
* `ip6` Sets the IPv6 address of the interface (String)
* `gateway` Sets the default gateway of the interface (String, or List of Strings for an IPv4 and an IPv6 gateway)
* `lag-members` List of non-LACP lag members for a port channel (List of Strings, interface names)
* `lacp-members-active` List of LACP active members for a port channel (List of Strings, interface names)
* `lacp-members-passive` List of LACP passive members for a port channel (List of Strings, interface names)
* `lacp-rate` Sets the switch rate for LACP only (String "fast" or "slow")
* `lacp-bypass` If true, an LACP port channel forwards before LACP comes up, for example while a server PXE boots (Boolean)
* `mlag` Set the label of the peer port-channel for a paired switch (String interface name)

## Development

ansible-test only runs from a checkout inside an `ansible_collections/cci_moc/stateful_switches`
directory:

```
git clone git@github.com:CCI-MOC/ansible-stateful-switches.git ansible_collections/cci_moc/stateful_switches
cd ansible_collections/cci_moc/stateful_switches
ansible-test units --venv --requirements
ansible-test sanity --venv --requirements --skip-test pep8
```

The `pep8` sanity test is skipped because ruff checks style through
[pre-commit](https://pre-commit.com) (`pre-commit install`), and pep8 rejects the
column-aligned test tables.

## Releasing

Every push to `main` runs the tests and, if the `version` in `galaxy.yml` is not on
Galaxy yet, publishes it and creates a `v<version>` GitHub release. To release, bump the
version in `galaxy.yml` following [semantic versioning](https://semver.org).

Publishing needs a `GALAXY_API_KEY` repository secret with an API token from an owner of
the `cci_moc` namespace on [Galaxy](https://galaxy.ansible.com/ui/token/).

## License

GNU General Public License v3.0, see [LICENSE](LICENSE).
