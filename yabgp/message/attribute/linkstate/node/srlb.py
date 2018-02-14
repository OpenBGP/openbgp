# Copyright 2015-2018 Cisco Systems, Inc.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import struct

from yabgp.message.attribute.linkstate.linkstate import LinkState
from yabgp.tlv import TLV

# https://tools.ietf.org/html/draft-ietf-idr-bgp-ls-segment-routing-ext-03#section-2.1.4
#     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |               Type            |               Length          |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |      Flags    |   RESERVED    |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |                  Range Size                   |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    //                SID/Label sub-TLV (variable)                 //
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


@LinkState.register()
class SRLB(TLV):

    TYPE = 1036  # https://tools.ietf.org/html/draft-ietf-idr-bgp-ls-segment-routing-ext-03#section-2.1.4
    TYPE_STR = "srlb"

    @classmethod
    def unpack(cls, value):
        """
        """
        # flags = value[0]
        # F = struct.unpack('!B', flags)[0] >> 7
        # M = (struct.unpack('!B', flags)[0] << 1) >> 7
        # S = (struct.unpack('!B', flags)[0] << 2) >> 7
        # D = (struct.unpack('!B', flags)[0] << 3) >> 7
        # A = (struct.unpack('!B', flags)[0] << 4) >> 7
        value = value[2:]
        results = []
        while True:
            if len(value) == 0:
                break
            else:
                range_size = struct.unpack('!I', "\x00" + value[:3])[0]
                length = struct.unpack('!H', value[5:7])[0]
                if length == 3:
                    data = (struct.unpack('!I', "\x00" + value[7:7 + length])[0] << 12) >> 12
                    value = value[7 + length:]
                elif length == 4:
                    data = struct.unpack('!I', value[7:7 + length])[0]
                    value = value[7 + length:]
                results.append({"sid_or_label": data, "range-size": range_size})
        return cls(value=results)
        # results = dict()
        # if ord(value[0]) == 0x80:
        #     results['ipv4'] = True
        # else:
        #     results['ipv6'] = True
        # results['range-size'] = struct.unpack('!L', value[1:5])[0]
        # return cls(value=results)
