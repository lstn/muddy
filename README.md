# muddy

[![PyPI version](https://badge.fury.io/py/muddy.svg)](https://badge.fury.io/py/muddy)

**muddy** is a python package and CLI tool for generating MUD files ([RFC8520](https://tools.ietf.org/html/rfc8520)).

## Usage

There are multiple ways to generate MUD objects, depending on the level of abstraction:

```python
from muddy.maker import make_mud
from muddy.models import Direction, IPVersion, Protocol, MatchType

mud = make_mud(1,'https://lighting.example.com/lightbulb2000', 48, True, 'The BMS Example Light Bulb', 
'https://lighting.example.com/lightbulb2000/documentation', [Direction.TO_DEVICE,Direction.FROM_DEVICE],
 IPVersion.IPV4, 'test.example.com', Protocol.ANY, MatchType.IS_MYMFG, [88,443], [88,443])
```

or

```python
from muddy.maker import make_mud, make_support_info
from muddy.models import Direction, IPVersion, Protocol, MatchType

support_info = make_support_info(1,'https://lighting.example.com/lightbulb2000', 48, True,
 'The BMS Example Light Bulb', 'https://lighting.example.com/lightbulb2000/documentation')

mud = make_mud(support_info , [Direction.TO_DEVICE,Direction.FROM_DEVICE],
 IPVersion.IPV4, 'test.example.com', Protocol.ANY, [88,443], [88,443], MatchType.IS_MYMFG)
```

or

```python
from muddy.maker import make_mud, make_acl_names, make_policy, make_acls
from muddy.models import Direction, IPVersion, Protocol, MatchType
import random

mud_name = f'mud-{random.randint(10000, 99999)}'
acl = []
policies = {}
for direction_initiated in [Direction.TO_DEVICE,Direction.FROM_DEVICE]:
    acl_names = make_acl_names(mud_name, IPVersion.IPV4, direction_initiated)
    policies.update(make_policy(direction_initiated, acl_names))
    acl.append(make_acls([IPVersion.IPV4], 'test.example.com', Protocol.ANY, [88,443], [88,443], MatchType.IS_MYMFG,
    direction_initiated, acl_names))

mud = make_mud(policies, acl, 1,'https://lighting.example.com/lightbulb2000', 48, True, 'The BMS Example Light Bulb', 
'https://lighting.example.com/lightbulb2000/documentation')
```

or

```python
from muddy.maker import make_mud, make_acl_names, make_policy, make_acls, make_support_info
from muddy.models import Direction, IPVersion, Protocol, MatchType
import random

support_info = make_support_info(1,'https://lighting.example.com/lightbulb2000', 48, True,
 'The BMS Example Light Bulb', 'https://lighting.example.com/lightbulb2000/documentation')


mud_name = f'mud-{random.randint(10000, 99999)}'
acl = []
policies = {}
for direction_initiated in [Direction.TO_DEVICE,Direction.FROM_DEVICE]:
    acl_names = make_acl_names(mud_name, IPVersion.IPV4, direction_initiated)
    policies.update(make_policy(direction_initiated, acl_names))
    acl.append(make_acls([IPVersion.IPV4], 'test.example.com', Protocol.ANY, [88,443], [88,443], MatchType.IS_MYMFG,
    direction_initiated,acl_names))

mud = make_mud(support_info, policies, acl)
```

To obtain JSON for a MUD object, you may just `json.dumps(mud)`.

## Example output

```json
{
  "ietf-mud:mud": {
    "mud-version": 1,
    "mud-url": "https://lighting.example.com/lightbulb2000",
    "last-update": "2019-07-23T19:54:24",
    "cache-validity": 48,
    "is-supported": true,
    "systeminfo": "The BMS Example Light Bulb",
    "documentation": "https://lighting.example.com/lightbulb2000/documentation",
    "to-device-policy": {
      "access-lists": {
        "access-list": [
          {
            "name": "mud-52892-v4to"
          }
        ]
      }
    },
    "from-device-policy": {
      "access-lists": {
        "access-list": [
          {
            "name": "mud-52892-v4fr"
          }
        ]
      }
    }
  },
  "ietf-access-control-list:acls": {
    "acl": [
      {
        "name": "mud-52892-v4to",
        "type": "ipv4",
        "aces": {
          "ace": [
            {
              "name": "myman0-todev",
              "matches": {
                "ietf-mud:mud": {
                  "same-manufacturer": []
                }
              },
              "actions": {
                "forwarding": "accept"
              }
            },
            {
              "name": "myman1-todev",
              "matches": {
                "ietf-mud:mud": {
                  "same-manufacturer": []
                }
              },
              "actions": {
                "forwarding": "accept"
              }
            },
            {
              "name": "myman1-todev",
              "matches": {
                "ietf-mud:mud": {
                  "same-manufacturer": []
                }
              },
              "actions": {
                "forwarding": "accept"
              }
            },
            {
              "name": "myman2-todev",
              "matches": {
                "ietf-mud:mud": {
                  "same-manufacturer": []
                }
              },
              "actions": {
                "forwarding": "accept"
              }
            }
          ]
        }
      },
      {
        "name": "mud-52892-v4fr",
        "type": "ipv4",
        "aces": {
          "ace": [
            {
              "name": "myman0-frdev",
              "matches": {
                "ietf-mud:mud": {
                  "same-manufacturer": []
                }
              },
              "actions": {
                "forwarding": "accept"
              }
            },
            {
              "name": "myman1-frdev",
              "matches": {
                "ietf-mud:mud": {
                  "same-manufacturer": []
                }
              },
              "actions": {
                "forwarding": "accept"
              }
            },
            {
              "name": "myman1-frdev",
              "matches": {
                "ietf-mud:mud": {
                  "same-manufacturer": []
                }
              },
              "actions": {
                "forwarding": "accept"
              }
            },
            {
              "name": "myman2-frdev",
              "matches": {
                "ietf-mud:mud": {
                  "same-manufacturer": []
                }
              },
              "actions": {
                "forwarding": "accept"
              }
            }
          ]
        }
      }
    ]
  }
}
```
