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
# Generated by process_xdr.py from portmap2.x on Sun Oct 04 08:09:28 2015
"""
PORTMAPv2 constants module
"""
import conf as c

# Module constants
__author__    = "Jorge Mora" 
__copyright__ = "Copyright (C) 2014 NetApp, Inc."
__license__   = "GPL v2"
__version__   = "2.0"

# Enum proto2
TCP = 6   # protocol number for TCP/IP
UDP = 17  # protocol number for UDP/IP

proto2 = {
     6 : "TCP",
    17 : "UDP",
}

# Enum portmap_proc2
PMAPPROC_NULL    = 0
PMAPPROC_SET     = 1
PMAPPROC_UNSET   = 2
PMAPPROC_GETPORT = 3
PMAPPROC_DUMP    = 4
PMAPPROC_CALLIT  = 5

portmap_proc2 = {
    0 : "PMAPPROC_NULL",
    1 : "PMAPPROC_SET",
    2 : "PMAPPROC_UNSET",
    3 : "PMAPPROC_GETPORT",
    4 : "PMAPPROC_DUMP",
    5 : "PMAPPROC_CALLIT",
}
