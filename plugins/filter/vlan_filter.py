def FILTER_VLANS(vlans, cur_groups=None):
    """
    Filter VLANs based on the current groups.

    :param vlans: List of VLANs to filter.
    :param cur_groups: Current groups to filter against. If None, all VLANs are returned.
    :return: Filtered list of VLANs.
    """

    outVLANs = {}

    for vlan in vlans:
        if (
            cur_groups is not None
            and "fabrics" not in vlan
            or not (set(vlan["fabrics"]) & set(cur_groups))
        ):
            continue

        if vlan["id"] in outVLANs:
            # Throw exception
            raise ValueError(
                f"Duplicate VLAN ID not allowed in the same fabric: {vlan['id']}"
            )

        outVLANs[int(vlan["id"])] = {
            "name": str(vlan["name"]),
            "description": str(vlan["description"]),
        }

        # add managed if exists
        if "managed" in vlan:
            outVLANs[int(vlan["id"])]["managed"] = bool(vlan["managed"])

    return outVLANs


class FilterModule(object):
    def filters(self):
        return {"filter_vlans": FILTER_VLANS}
