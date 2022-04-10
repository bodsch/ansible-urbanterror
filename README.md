
# Ansible Role:  `urbanterror`


installs and configure an [Urbanterror](https://www.urbanterror.info/home) server.


[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/bodsch/ansible-urbanterror/CI)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-urbanterror)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-urbanterror)][releases]

[ci]: https://github.com/bodsch/ansible-urbanterror/actions
[issues]: https://github.com/bodsch/ansible-urbanterror/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-urbanterror/releases

## Operating systems

Tested on

* Debian based
    - Debian 10 / 11
    - Ubuntu 20.04

## usage

### default configration

```yaml
urbanterror_admin_password: s3cr3T-are-p0ssiBL3

urbanterror_start_map: ut4_riyadh
urbanterror_game_type: CaptureTheFlag

urbanterror_bind_ip: "{{ ansible_default_ipv4.address | default('127.0.0.1') }}"
urbanterror_bind_port: 27960

urbanterror_artifact: https://www.urbanterror.info/downloads/software/urt/43/UrbanTerror43_ded.tar.gz
urbanterror_binary: "Quake3-UrT-Ded.{{ ansible_machine }}"

urbanterror_config:
  # intition version: 4.0.3
  current_version: '4.0.3'
  # id: 2 =
  download_server: '2'
  # id: 1 = Quake3-UrT (default)
  # id: 2 = ioq3-m9 (BETA)
  game_engine: '1'
  ask_before_updating: false

urbanterror_directory: /opt/urbanterror

urbanterror_server_title: "UrbanTerror Server"
urbanterror_server_join_message: "Welcome to Urban Terror"
urbanterror_server_motd: "Urban Terror, Presented by FrozenSand"

urbanterror_server_admin: "darth.vader"
urbanterror_server_clan: "Imperial Force"
urbanterror_server_email: "darth.vader@imperial.force"
urbanterror_server_location: "Coruscant"

urbanterror_server_auth:
  enable: false
  # Minimum notoriety level to be able to connect to your server.
  # 0 allows everyone to join
  notoriety: 0
  # Set this to 'true' to prevent clan tag thieves from joining your server
  tags: true
  # Set this to 'true' to block the officially banned cheaters from your server
  cheaters: true
  # 0 = no authentication message to everyone when a player connects
  # 1 = message on the top of the screen
  # 2 = message in the chat box
  verbosity: 1
  # Set this to 'true' to draw the account information in the userinfo of each player in the server logs
  log: true

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

#### Game Types

- `FreeForAll`
- `LastManStanding`
- `TeamDeathMatch`
- `TeamSurvivor`
- `FollowTheLeader`
- `CaptureAndHold`
- `CaptureTheFlag`
- `BombMode`
- `JumpTraining`
- `FreezeTag`
- `GunGame`

```yaml
urbanterror_game_type: CaptureTheFlag
```
