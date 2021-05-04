
installs and configure an [Urbanterror](https://www.urbanterror.info/home) server.


[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/bodsch/ansible-urbanterror/CI)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-urbanterror)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-urbanterror)][releases]

[ci]: https://github.com/bodsch/ansible-urbanterror/actions
[issues]: https://github.com/bodsch/ansible-urbanterror/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-urbanterror/releases

## Operating systems

Tested on

* Debian 9 / 10
* Ubuntu 18.04 / 20.04

## usage

### default configration

```
urbanterror_admin_password: s3cr3T-are-p0ssiBL3

urbanterror_start_map: ut4_riyadh
urbanterror_game_type: CaptureTheFlag

urbanterror_bind_ip: "{{ ansible_default_ipv4.address }}"
urbanterror_bind_port: 27960

urbanterror_artifact: https://www.urbanterror.info/downloads/software/urt/43/UrbanTerror43_ded.tar.gz
urbanterror_binary: "Quake3-UrT-Ded.{{ ansible_machine }}"

urbanterror_directory: /opt/urbanterror

urbanterror_maps:
  - ut4_abbey
  - ut4_mandolin
  - ut4_uptown
  - ut4_algiers
  - ut4_austria
  - ut4_oildepot

urbanterror_custom_maps:
  - name: ut_park_avenue_fix
    src: http://downloads.urban-zone.org/maps/q3ut4/ut_park_avenue_fix.pk3
  - name: ut_maya_beta3
    src: http://downloads.urban-zone.org/maps/q3ut4/ut_maya_beta3.pk3
```

