#===============================================================================
# Copyright 2014 NetApp, Inc. All Rights Reserved,
# contribution by Jorge Mora <mora@netapp.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#===============================================================================
"""
UDP module

Decode UDP layer.
"""
from packet.application.rpc import RPC
from utilites.baseobj import BaseObj

# Module constants
__author__    = 'Jorge Mora' 
__copyright__ = "Copyright (C) 2014 NetApp, Inc."
__license__   = "GPL v2"
__version__   = '1.0'

class UDP(BaseObj):
    """UDP object

       Usage:
           from packet.transport.udp import UDP

           x = UDP(pktt)

       Object definition:

       UDP(
           src_port = int,
           dst_port = int,
           length   = int,
           checksum = int,
           data     = string,    # raw data of payload if unable to decode
       )
    """
    # Class attributes
    _attrlist = ("src_port", "dst_port", "length", "checksum", "data")
    _strfmt1  = "UDP {0} -> {1}, len: {2}"
    _strfmt2  = "src port {0} -> dst port {1}, len: {2}, checksum: {3:#010x}"

    def __init__(self, pktt):
        """Constructor

           Initialize object's private data.

           pktt:
               Packet trace object (packet.pktt.Pktt) so this layer has
               access to the parent layers.
        """
        unpack = pktt.unpack

        # Decode the UDP layer header
        ulist = unpack.unpack(8, "!HHHH")
        self.src_port = ulist[0]
        self.dst_port = ulist[1]
        self.length   = ulist[2]
        self.checksum = ulist[3]

        pktt.pkt.udp = self
        self._decode_payload(pktt)

    def _decode_payload(self, pktt):
        """Decode UDP payload."""
        # Get RPC header
        rpc = RPC(pktt, proto=17)

        if rpc:
            # Save RPC layer on packet object
            pktt.pkt.rpc = rpc
            if rpc.type:
                # Remove packet call from the xid map since reply has
                # already been decoded
                pktt._rpc_xid_map.pop(rpc.xid, None)

            # Decode NFS layer
            rpc.decode_payload()
