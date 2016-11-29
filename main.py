import os
import stat
import traceback
import conf as c
from time import sleep
from params import *
from nfstest.test_util import TestUtil


TESTNAMES = [
    'access_exist_file',
    'access_non_exist_file',
    'access_perm_read',
    'access_perm_write',
    'access_perm_del',
    'read',
    'write',
    'symlink',
]

class PosixTest(TestUtil):

    def __init__(self, **kwargs):
        """Constructor

           Initialize object's private data.
        """
        TestUtil.__init__(self, **kwargs)
        self.opts.version = "%prog " + c.__version__
        self.scan_options()

        # Make sure actimeo is set
        if 'actimeo' not in self.mtopts:
            self.mtopts += ",actimeo=0"

        # Get page size
        self.PAGESIZE = os.sysconf(os.sysconf_names['SC_PAGESIZE'])

        # Clear umask
        os.umask(0)

    def access(self, path, mode, test, msg=""):
        """Test file access.

           path:
               File system object to get access from
           mode:
               Mode access to check
           test:
               Expected output from access()
           msg:
               Message to be appended to test message
        """
        not_str = "" if test else "not "
        out = posix.access(path, mode)
        self.test(out == test, "access - file access %sallowed with mode %s%s" % (not_str, access_str(mode), msg))

    def access_exist_file_test(self):
        """
            Verify access for existing file
        """
        self.test_group("Verify access for existing file")
        self.create_file()
        self.access(self.absfile, posix.F_OK, True)

    def access_non_exist_file_test(self):
        """
            Verify access for non-existing file
        """
        self.test_group("Verify access for non-existing file")
        self.create_file()
        self.access(self.absfile + 'bogus', posix.F_OK, False, " for a non-existent file")

    def access_perm_read_test(self):
        """
            Verify access with mode R_OK for file with permissions 0777
        """
        self.test_group("Verify access with mode R_OK")
        self.create_file()
        perm = 0777
        msg = " for file with permissions %s" % oct(perm)
        os.chmod(self.absfile, perm)
        self.access(self.absfile, posix.R_OK, (perm&4)!=0, msg)

    def access_perm_write_test(self):
        """
            Verify access with mode W_OK for file with permissions 0777
        """
        self.test_group("Verify access with mode W_OK")
        self.create_file()
        perm = 0777
        msg = " for file with permissions %s" % oct(perm)
        os.chmod(self.absfile, perm)
        self.access(self.absfile, posix.W_OK, (perm&2)!=0, msg)

    def access_perm_del_test(self):
        """
            Verify access with mode X_OK for file with permissions 0777
        """
        self.test_group("Verify access with mode X_OK")
        self.create_file()
        perm = 0777
        msg = " for file with permissions %s" % oct(perm)
        os.chmod(self.absfile, perm)
        self.access(self.absfile, posix.X_OK, (perm&1)!=0, msg)

    def read_test(self):
        """
            Read data from a file.
        """
        self.test_group("Read data from a file")

        absfile = self.abspath(self.files[0])
        self.dprint('DBG3', "Open file %s for reading" % absfile)
        fd = posix.open(absfile, posix.O_RDONLY)
        fstat_b = os.stat(absfile)
        sleep(1)
        data = posix.read(fd, self.filesize)
        self.test(data == self.data_pattern(0, len(data)), "read - reading file should succeed")
        posix.close(fd)

    def symlink_test(self):
        """Verify creating a symbolic link and verify
           that the file type is slnk.
        """
        self.test_group("Verify creating a symbolic link")

        srcfile = self.abspath(self.files[0])
        self.get_filename()
        self.dprint('DBG3', "Create symbolic link %s -> %s using POSIX API symlink()" % (self.absfile, srcfile))
        posix.symlink(srcfile, self.absfile)
        lstat = os.lstat(self.absfile)
        rlink = os.readlink(self.absfile)
        self.test(stat.S_ISLNK(lstat.st_mode), "symlink - object type should be a symbolic link")

    def write_test(self):
        """Write a pattern the file and close the file. Open the file and read in both
           written patterns and verify that it is the correct pattern.
        """
        self.test_group("Write a pattern the file")

        self.get_filename()
        self.dprint('DBG3', "Open file %s for writing" % self.absfile)
        fd = posix.open(self.absfile, posix.O_WRONLY|posix.O_CREAT)
        sleep(1)

        self.dprint('DBG3', "Write data to file %s at offset = 0 using POSIX API write()" % self.absfile)
        count = posix.write(fd, self.data_pattern(0, self.filesize))
        self.test(count == self.filesize, "write - writing N bytes should return N")

        posix.close(fd)

#  Entry point
x = PosixTest(usage="", testnames=TESTNAMES, sid="POSIX")

try:
    x.setup(nfiles=2)
    x.umount()
    x.mount()

    # Run all the tests
    x.run_tests()
except Exception:
    x.test(False, traceback.format_exc())
finally:
    x.cleanup()
    x.exit()
