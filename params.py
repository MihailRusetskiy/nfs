import ctypes
import posix

stat_map = {
    1: 'stat',
    2: 'lstat',
    3: 'fstat',
}

access_names = {
    posix.F_OK: 'F_OK',
    posix.R_OK: 'R_OK',
    posix.W_OK: 'W_OK',
    posix.X_OK: 'X_OK',
}

def access_str(mode):
    """Convert the access mode bitmap to its string representation."""
    list = []
    for perm in access_names:
        if perm & mode != 0:
            list.append(access_names[perm])
    if len(list) == 0:
        list.append(access_names[0])
    return '|'.join(list)

class DirEnt(ctypes.Structure):
    """
       struct dirent {
           ino_t          d_ino;       /* inode number */
           off_t          d_off;       /* offset to the next dirent */
           unsigned short d_reclen;    /* length of this record */
           unsigned char  d_type;      /* type of file; not supported
                                          by all file system types */
           char           d_name[256]; /* filename */
       };
    """
    _fields_ = [
        ("d_ino",    ctypes.c_ulong),
        ("d_off",    ctypes.c_ulong),
        ("d_reclen", ctypes.c_ushort),
        ("d_type",   ctypes.c_char),
        ("d_name",   ctypes.c_char*256),
    ]

class Flock(ctypes.Structure):
    """
       struct flock {
           short l_type;    /* Type of lock: F_RDLCK,
                               F_WRLCK, F_UNLCK */
           short l_whence;  /* How to interpret l_start:
                               SEEK_SET, SEEK_CUR, SEEK_END */
           off_t l_start;   /* Starting offset for lock */
           off_t l_len;     /* Number of bytes to lock */
           pid_t l_pid;     /* PID of process blocking our lock
                               (F_GETLK only) */

       };
    """
    _fields_ = [
        ("l_type",   ctypes.c_short),
        ("l_whence", ctypes.c_short),
        ("l_start",  ctypes.c_ulong),
        ("l_len",    ctypes.c_ulong),
        ("l_pid",    ctypes.c_int),
    ]

# OPEN flags
access_flag_list = [
    posix.O_RDONLY,
    posix.O_WRONLY,
    posix.O_RDWR,
]
open_flag_list = [
    posix.O_RDONLY,
    posix.O_WRONLY,
    posix.O_RDWR,
    posix.O_CREAT,
    posix.O_EXCL,
    posix.O_NOCTTY,
    posix.O_TRUNC,
    posix.O_APPEND,
    posix.O_ASYNC,
    # Linux-specific flags
    posix.O_DIRECTORY,
    posix.O_NOATIME,
    posix.O_NOFOLLOW,
]
open_flag_map = {
    posix.O_RDONLY:    'O_RDONLY',
    posix.O_WRONLY:    'O_WRONLY',
    posix.O_RDWR:      'O_RDWR',
    posix.O_CREAT:     'O_CREAT',
    posix.O_EXCL:      'O_EXCL',
    posix.O_NOCTTY:    'O_NOCTTY',
    posix.O_TRUNC:     'O_TRUNC',
    posix.O_APPEND:    'O_APPEND',
    posix.O_ASYNC:     'O_ASYNC',
    # Linux-specific flags
    posix.O_DIRECTORY: 'O_DIRECTORY',
    posix.O_NOATIME:   'O_NOATIME',
    posix.O_NOFOLLOW:  'O_NOFOLLOW',
}

perm_map = {
    00001: 'XOTH',
    00002: 'WOTH',
    00004: 'ROTH',
    00010: 'XGRP',
    00020: 'WGRP',
    00040: 'RGRP',
    00100: 'XUSR',
    00200: 'WUSR',
    00400: 'RUSR',
    01000: 'SVTX',
    02000: 'SGID',
    04000: 'SUID',
}

def oflag_str(flags):
    """Convert the open flags bitmap to its string representation."""
    flist = []
    flag_list = list(flags)
    if 0 in access_flag_list:
        # Flag with no bits set is in the access list
        found = False
        for flag in access_flag_list:
            if flag in flags:
                # At least one access flag is in flags
                found = True
                break
        if not found:
            flag_list = [0] + flag_list
    for flag in flag_list:
        flist.append(open_flag_map[flag])
    return '|'.join(flist)