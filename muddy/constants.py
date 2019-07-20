MUD_MODEL_DEF = {
    "mud-version": "This node specifies the integer version of the MUD specification.",
    "mud-url": "This URL identifies the MUD file.",
    "to-device-policy": "The policies that should be enforced on traffic going to the device.",
    "from-device-policy": "The policies that should be enforced on traffic coming from the device.",
    "last-update": "This is a date-and-time value of when the MUD file was generated.",
    "cache-validity": "This uint8 is the period of time in hours that a network management station MUST wait since its last retrieval before checking for an update.",
    "is-supported": "This boolean is an indication from the manufacturer to the network administrator as to whether or not the Thing is supported. ",
    "systeminfo": "This is a textual UTF-8 description of the Thing to be connected.",
    "mfg-name": "These optional fields are filled in as specified by [RFC8348]",
    "software-rev": "These optional fields are filled in as specified by [RFC8348]",
    "model-name": "These optional fields are filled in as specified by [RFC8348]",
    "firmware-rev": "These optional fields are filled in as specified by [RFC8348]",
    "documentation": "This URI consists of a URL that points to documentation relating to the device and the MUD file.",
    "extensions": "A list of extension names that are used in this MUD file.  Each name is registered with the IANA and described in an RFC."
}

DOMAIN_NAME_REGEX = r'[a-zA-Z0-9.-]+\.[a-zA-Z]{2,3}$'
HTTP_URL_REGEX = r'/^(http|https):\\/\\/[a-zA-Z0-9_]+([\\-\\.]{1}[a-zA-Z_0-9]+)*\\.[_a-zA-Z]{2,5}((:[0-9]{1,5})?\\/.*)?$/i'
URN_URL_REGEX = '^urn:[a-zA-Z0-9][a-zA-Z0-9-]{0,31}:[a-zA-Z0-9()+,\-.:=@;$_!*\'%/?#]+$^'
