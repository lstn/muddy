# muddy

**muddy** is a python package and CLI tool for generating MUD files.

## Usage

There are multiple ways to generate MUD objects, depending on the level of abstraction:

```python
from muddy import maker
from muddy import models

mud = maker.make_mud(1,'https://lighting.example.com/lightbulb2000', 48, True, 'The BMS Example Light Bulb', 
'https://lighting.example.com/lightbulb2000/documentation', [models.Direction.TO_DEVICE,models.Direction.FROM_DEVICE],
 models.IPVersion.IPV4, 'test.example.com', models.Protocol.ANY, [88,443], [88,443], models.MatchType.IS_MYMFG)
```

or

```python
from muddy import maker
from muddy import models

support_info = maker.make_support_info(1,'https://lighting.example.com/lightbulb2000', 48, True,
 'The BMS Example Light Bulb', 'https://lighting.example.com/lightbulb2000/documentation')

mud = maker.make_mud(support_info , [models.Direction.TO_DEVICE,models.Direction.FROM_DEVICE],
 models.IPVersion.IPV4, 'test.example.com', models.Protocol.ANY, [88,443], [88,443], models.MatchType.IS_MYMFG)
```

or

```python
from muddy import maker
from muddy import models
import random

mud_name = f'mud-{random.randint(10000, 99999)}'
acl = []
policies = {}
for direction_initiated in [models.Direction.TO_DEVICE,models.Direction.FROM_DEVICE]:
    acl_names = maker.make_acl_names(mud_name, models.IPVersion.IPV4, direction_initiated)
    policies.update(maker.make_policy(direction_initiated, acl_names))
    acl.append(
        maker.make_acls([models.IPVersion.IPV4], 'test.example.com', models.Protocol.ANY, [88,443], [88,443], models.MatchType.IS_MYMFG, direction_initiated,
                  acl_names))

mud = maker.make_mud(policies, acl, 1,'https://lighting.example.com/lightbulb2000', 48, True, 'The BMS Example Light Bulb', 
'https://lighting.example.com/lightbulb2000/documentation')
```

or

```python
from muddy import maker
from muddy import models
import random

support_info = maker.make_support_info(1,'https://lighting.example.com/lightbulb2000', 48, True,
 'The BMS Example Light Bulb', 'https://lighting.example.com/lightbulb2000/documentation')


mud_name = f'mud-{random.randint(10000, 99999)}'
acl = []
policies = {}
for direction_initiated in [models.Direction.TO_DEVICE,models.Direction.FROM_DEVICE]:
    acl_names = maker.make_acl_names(mud_name, models.IPVersion.IPV4, direction_initiated)
    policies.update(maker.make_policy(direction_initiated, acl_names))
    acl.append(
        maker.make_acls([models.IPVersion.IPV4], 'test.example.com', models.Protocol.ANY, [88,443], [88,443], models.MatchType.IS_MYMFG, direction_initiated,
                  acl_names))

mud = maker.make_mud(support_info, policies, acl)
```

## Example output

```json
{
  "ietf-mud:mud": {
    "mud-version": 1,
    "mud-url": "https://lighting.example.com/lightbulb2000",
    "last-update": "2019-07-21T14:40:16",
    "cache-validity": 48,
    "is-supported": true,
    "systeminfo": "The BMS Example Light Bulb",
    "documentation": "https://lighting.example.com/lightbulb2000/documentation",
    "to-device-policy": {
      "access-lists": {
        "access-list": [
          "mud-56908-v4to"
        ]
      }
    },
    "from-device-policy": {
      "access-lists": {
        "access-list": [
          "mud-56908-v4fr"
        ]
      }
    }
  },
  "ietf-access-control-list:acls": {
    "acl": [
      {
        "name": "mud-56908-v4to",
        "type": "ipv4",
        "aces": {
          "ace": [
            {
              "name": "myman0-todev",
              "matches": {
                "ietf-mud:mud": {
                  "same-manufacturer": []
                }
              }
            }
          ]
        }
      },
      {
        "name": "mud-56908-v4fr",
        "type": "ipv4",
        "aces": {
          "ace": [
            {
              "name": "myman0-todev",
              "matches": {
                "ietf-mud:mud": {
                  "same-manufacturer": []
                }
              }
            }
          ]
        }
      }
    ]
  }
}
```
