import os

__version__   = "1.0"

bin_dirs = [
    '/usr/bin',
    '/usr/sbin',
    '/bin',
    '/sbin',
]

def _find_exec(command):
    for bindir in bin_dirs:
        bincmd = os.path.join(bindir, command)
        if os.path.exists(bincmd):
            return bincmd
    return command

# Default values
NFSTEST_NFSVERSION   = 4.0
NFSTEST_NFSPROTO     = 'tcp'
NFSTEST_NFSPORT      = 2049
NFSTEST_NFSSEC       = 'sys'
NFSTEST_EXPORT       = '/'
NFSTEST_MTPOINT      = '/mnt/t'
NFSTEST_MTOPTS       = 'hard,rsize=4096,wsize=4096'
NFSTEST_INTERFACE    = 'eth0'
NFSTEST_SUDO         = _find_exec('sudo')
NFSTEST_IPTABLES     = _find_exec('iptables')
NFSTEST_TCPDUMP      = _find_exec('tcpdump')
NFSTEST_MESSAGESLOG  = '/var/logs/messages'
NFSTEST_LOG          = 'logs'
NFSTEST_DEBUGLEVEL   = 'none'  # all
NFSTEST_TMPDIR       = '/tmp'
NFSTEST_TESTDIR = 'test'
NFSTEST_CONFIG  = '/etc/nfstest'
NFSTEST_HOMECFG = os.path.join(os.environ.get('HOME',''), '.nfstest')
NFSTEST_CWDCFG  = '.nfstest'
