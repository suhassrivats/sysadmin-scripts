# RedHat Practice

**Q0: Configure Network **

```
Configure the network as follows:
- The IP address of your system should be : 172.25.X.10
- Subnet Mask : 255.255.255.0
- Name Server: 172.25.254.254
- Gateway: 172.25.X.254
- Note : X is your foundation number
```

**Solution:**

TBD

---



**Q1: CONFIGURE SELINUX**

```
Configure the selinux mode of your system as enforcing.
```

**Solution:  **

First, set to enforcing using `setenforce` command. This is only a temporary change. Meaning, will be changed after reboot.

```bash
[root@server2 ~]# setenforce enforcing
[root@server2 ~]# getenforce
Enforcing
```

To permanently change it, edit `/etc/selinux/config` file and type `SELINUX=enforcing`

```bash
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=enforcing
# SELINUXTYPE= can take one of these two values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected.
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted
```

---

**Q2: CONFIGURE YUM**

```
Configure your machine such that you are able to download exam softwares from http://content.example.com/rhel7.0/x86_64/dvd/
```

**Solution:  **

1. Create a file with `.repo` extension in `/etc/yum.repos.d/` folder. In this example, I have created a repo named `errata.repo` with the given link. 

   *Note*: Make sure that there is no spaces between []. For example [abc def] is incorrect and [abc-def] is correct. In this example, it is `[Packages]`

```bash
[root@server2 yum.repos.d]# pwd
/etc/yum.repos.d

[root@server2 yum.repos.d]# ls
errata.repo

[root@server2 yum.repos.d]# cat errata.repo
[Packages]
name=Redhat packages repo
baseurl=http://content.example.com/rhel7.0/x86_64/dvd/
enabled=1
gpgcheck=0
```

2. Verify if the repo is available

```bash
[root@server2 yum.repos.d]# yum repolist
Loaded plugins: langpacks
repo id                repo name                           status
Packages               Redhat packages repo                4,305
repolist: 4,305
```

3. Try to install some packages

```bash
[root@server2 yum.repos.d]# yum install sys*
Loaded plugins: langpacks
Package systemtap-sdt-devel-2.4-14.el7.x86_64 already installed and latest version
```

---

**Q3: CONFIGURE NTP** - To be discussed

1. Check if NTP is enabled. If not, enable it.

   ```bash
   [root@server2 yum.repos.d]# timedatectl status
         Local time: Wed 2018-07-25 01:16:02 IST
     Universal time: Tue 2018-07-24 19:46:02 UTC
           RTC time: Tue 2018-07-24 19:46:01
           Timezone: Asia/Kolkata (IST, +0530)
        NTP enabled: yes
   NTP synchronized: no
    RTC in local TZ: no
         DST active: n/a
   ```

   Get clarification about this task

---

**Q4: CREATE USERS**

```
Create the following users:
- Create a group sysadmin.
- Create a user alice who has sysadmin as a supplementary group.
- Create a user harry who also has sysadmin as his supplementary group.
- Create a user joy who does not have an interactive shell.
```

**Solution:**

```bash
# Groupadd
[root@server2 ~]# groupadd sysadmin

# Useradd to group
[root@server2 ~]# useradd alice -G sysadmin
[root@server2 ~]# useradd harry -G sysadmin
[root@server2 ~]# useradd joy -s /bin/nologin

# Add user to a group with no interactive shell
[root@server2 ~]# useradd john -s /bin/nologin -G sysadmin

# Verify
[root@server2 ~]# cat /etc/group |grep sysadmin
sysadmin:x:1001:alice,harry,john
```

---

**Q5: LVM CREATION**

```
- Create a logical volume with 20 extents where one extend is having the size of 16MiB.
- The logical volume has the name of database and volume group have the name of datastore.
- The logical volume should be mounted under the directory /mnt/database with a file system of ext3 and should be automatically available on reboot.
```

**Solution:**

1. Find out where to create the partition

```bash
# Right now we just have the 10GB hdd (vdb) with no partitions:
[root@server2 ~]# lsblk
NAME   MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
vda    253:0    0  10G  0 disk
└─vda1 253:1    0  10G  0 part /
vdb    253:16   0  10G  0 disk
```

2. Use `fdisk` to create the partition

```bash
[root@server2 ~]# fdisk /dev/vdb
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table
Building a new DOS disklabel with disk identifier 0x06fbbd48.

Command (m for help): n
Partition type:
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p): p
Partition number (1-4, default 1): 2
First sector (2048-20971519, default 2048):
Using default value 2048
Last sector, +sectors or +size{K,M,G} (2048-20971519, default 20971519): +320M
Partition 2 of type Linux and of size 320 MiB is set

Command (m for help): p

Disk /dev/vdb: 10.7 GB, 10737418240 bytes, 20971520 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x06fbbd48

   Device Boot      Start         End      Blocks   Id  System
/dev/vdb2            2048      657407      327680   83  Linux

Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.
Syncing disks.

[root@server2 ~]# partprobe
```

3. Check if a partition is created using `lsblk`

```bash
[root@server2 ~]# lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
vda    253:0    0   10G  0 disk
└─vda1 253:1    0   10G  0 part /
vdb    253:16   0   10G  0 disk
└─vdb2 253:18   0  320M  0 part
```

4. We have now created a partition. However this partition is currently listed as standard Linux partition (type 83) as highlighted above. Therefore we need to switch this to the LVM partition type.

   **Note:** type “t” to change the partition type. Then choose “8e” for “Linux LVM”. Then, type “w” to save and “partprobe” to update the partition table.

```bash
[root@server2 ~]# fdisk /dev/vdb
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.


Command (m for help): m
Command action
   a   toggle a bootable flag
   b   edit bsd disklabel
   c   toggle the dos compatibility flag
   d   delete a partition
   g   create a new empty GPT partition table
   G   create an IRIX (SGI) partition table
   l   list known partition types
   m   print this menu
   n   add a new partition
   o   create a new empty DOS partition table
   p   print the partition table
   q   quit without saving changes
   s   create a new empty Sun disklabel
   t   change a partition's system id
   u   change display/entry units
   v   verify the partition table
   w   write table to disk and exit
   x   extra functionality (experts only)

Command (m for help): t
Selected partition 2
Hex code (type L to list all codes): L

 0  Empty           24  NEC DOS         81  Minix / old Lin bf  Solaris       
 1  FAT12           27  Hidden NTFS Win 82  Linux swap / So c1  DRDOS/sec (FAT-
 2  XENIX root      39  Plan 9          83  Linux           c4  DRDOS/sec (FAT-
 3  XENIX usr       3c  PartitionMagic  84  OS/2 hidden C:  c6  DRDOS/sec (FAT-
 4  FAT16 <32M      40  Venix 80286     85  Linux extended  c7  Syrinx        
 5  Extended        41  PPC PReP Boot   86  NTFS volume set da  Non-FS data   
 6  FAT16           42  SFS             87  NTFS volume set db  CP/M / CTOS / .
 7  HPFS/NTFS/exFAT 4d  QNX4.x          88  Linux plaintext de  Dell Utility  
 8  AIX             4e  QNX4.x 2nd part 8e  Linux LVM       df  BootIt        
 9  AIX bootable    4f  QNX4.x 3rd part 93  Amoeba          e1  DOS access    
 a  OS/2 Boot Manag 50  OnTrack DM      94  Amoeba BBT      e3  DOS R/O       
 b  W95 FAT32       51  OnTrack DM6 Aux 9f  BSD/OS          e4  SpeedStor     
 c  W95 FAT32 (LBA) 52  CP/M            a0  IBM Thinkpad hi eb  BeOS fs       
 e  W95 FAT16 (LBA) 53  OnTrack DM6 Aux a5  FreeBSD         ee  GPT           
 f  W95 Ext'd (LBA) 54  OnTrackDM6      a6  OpenBSD         ef  EFI (FAT-12/16/
10  OPUS            55  EZ-Drive        a7  NeXTSTEP        f0  Linux/PA-RISC b
11  Hidden FAT12    56  Golden Bow      a8  Darwin UFS      f1  SpeedStor     
12  Compaq diagnost 5c  Priam Edisk     a9  NetBSD          f4  SpeedStor     
14  Hidden FAT16 <3 61  SpeedStor       ab  Darwin boot     f2  DOS secondary 
16  Hidden FAT16    63  GNU HURD or Sys af  HFS / HFS+      fb  VMware VMFS   
17  Hidden HPFS/NTF 64  Novell Netware  b7  BSDI fs         fc  VMware VMKCORE
18  AST SmartSleep  65  Novell Netware  b8  BSDI swap       fd  Linux raid auto
1b  Hidden W95 FAT3 70  DiskSecure Mult bb  Boot Wizard hid fe  LANstep       
1c  Hidden W95 FAT3 75  PC/IX           be  Solaris boot    ff  BBT           
1e  Hidden W95 FAT1 80  Old Minix

# Type code 8e for Linux LVM
Hex code (type L to list all codes): 8e
Changed type of partition 'Linux' to 'Linux LVM'

# Verify if the changes are applied
Command (m for help): p

Disk /dev/vdb: 10.7 GB, 10737418240 bytes, 20971520 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x06fbbd48

   Device Boot      Start         End      Blocks   Id  System
/dev/vdb2            2048      657407      327680   8e  Linux LVM

# Save the configuration
Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.
Syncing disks.

# Update partition table
[root@server2 ~]# partprobe
```

5. Create Physical Volume (VG). But this volume is not added to Volume Group (VG) yet

```bash
# Create a Physcial Volume
[root@server2 ~]# pvcreate /dev/vdb2
  Physical volume "/dev/vdb2" successfully created
  
# List all the pvs that currently exists
[root@server2 ~]# pvs
  PV         VG   Fmt  Attr PSize   PFree
  /dev/vdb2       lvm2 a--  320.00m 320.00m
```

6. Create a Volume Group (VG) using `vgcreate`. To add more PVs to VG use `vgextend`. Example `vgextend vgdata1vg /dev/sdb3`

```bash
[root@server2 ~]# vgcreate datastore /dev/vdb2
  Physical volume "/dev/vdb2" successfully created
  Volume group "datastore" successfully created

# List all Volume Groups
[root@server2 ~]# vgs
  VG        #PV #LV #SN Attr   VSize   VFree
  datastore   1   0   0 wz--n- 316.00m 316.00m
  
# For more details about the volume group use vgdisplay
[root@server2 ~]# vgdisplay
  --- Volume group ---
  VG Name               datastore
  System ID
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  1
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               316.00 MiB
  PE Size               4.00 MiB
  Total PE              79
  Alloc PE / Size       0 / 0
  Free  PE / Size       79 / 316.00 MiB
  VG UUID               lNRcvo-YsN8-2kYB-osIR-iVOG-4gNt-Q1pZxE
```

7. Create a Logical Volume

```bash
# Create a LV named database of size 320M from VG datastore
[root@server2 ~]# lvcreate -n database -L 320M datastore
  Rounding up size to full physical extent 320.00 MiB
  Logical volume "database" created

# List Logical Volumes
[root@server2 ~]# lvs
  LV       VG        Attr       LSize   Pool Origin Data%  Move Log Cpy%Sync Convert
  database datastore -wi-a----- 320.00m                                       
```

8. Add the file system and mount it to directory. For permanent mount, add an entry in “/etc/fstab”

```bash
# Apply file system using mkfs command
[root@server2 ~]# mkfs.ext3 /dev/datastore/database
mke2fs 1.42.9 (28-Dec-2013)
Filesystem label=
OS type: Linux
Block size=1024 (log=0)
Fragment size=1024 (log=0)
Stride=0 blocks, Stripe width=0 blocks
79872 inodes, 319488 blocks
15974 blocks (5.00%) reserved for the super user
First data block=1
Maximum filesystem blocks=67633152
39 block groups
8192 blocks per group, 8192 fragments per group
2048 inodes per group
Superblock backups stored on blocks:
        8193, 24577, 40961, 57345, 73729, 204801, 221185

Allocating group tables: done
Writing inode tables: done
Creating journal (8192 blocks): done
Writing superblocks and filesystem accounting information: done
```

9. Mount it to a directory

```bash
[root@server2 ~]# mkdir -p /mnt/database

[root@server2 mnt]# mount /dev/datastore/database /mnt/database

[root@server2 mnt]# cd /mnt/database
[root@server2 database]# df -h .
Filesystem                      Size  Used Avail Use% Mounted on
/dev/mapper/datastore-database  295M  2.1M  273M   1% /mnt/database
```

10. Update /etc/fstab

```bash
[root@server2 database]# tail -n1 /etc/fstab
/dev/datastore/database /mnt/database ext4 defaults 0 0
```

---

**Q6: COPY FILE**

```
Copy the file /etc/passwd to /var/tmp/hello.
The file should belong to the user root and group root.
The user alice should be able to read and write on the file.
The user harry should neither read nor write on the file.
All other users should have read permission on the file.
```

**Solution:**

```bash
# Copy the file /etc/passwd to /var/tmp/hello
[suhas@foundation2 ~]$ cp /etc/passwd /var/tmp/hello

# The file should belong to the user root and group root
[root@server2 ~]# chown root:root /var/tmp/hello
[root@server2 ~]# ls -l /var/tmp/hello
-rw-r--r--. 1 root root 2169 Aug  2 02:04 /var/tmp/hello

# User ACL restrictions
[root@server2 ~]# setfacl -m u:alice:rw /var/tmp/hello
[root@server2 ~]# setfacl -m u:harry:- /var/tmp/hello
[root@server2 ~]# setfacl -m u::--r-- /var/tmp/hello

# Verify
[root@server2 ~]# getfacl /var/tmp/hello
getfacl: Removing leading '/' from absolute path names
# file: var/tmp/hello
# owner: root
# group: root
user::rw-
user:alice:rw-
user:harry:---
group::r--
mask::rw-
```

---

**Q7: CREATE DIRECTORY**

```
Create a directory /wonderful.
The user alice and harry should be able to collaboratively work on this directory.
The files and directories created within this directory should automatically belong to the group sysadmin.
All members of the group should have read and write access. All other users should not have any permissions.
Note: By default, root user will have read and write access to all files and directories.
```

**Solution:**

```bash
# Make a directory
[root@server2 ~]# mkdir /wonderful

# Apply group permissions so that people in the group can access the directory
[root@server2 /]# chgrp sysadmin wonderful/
[root@server2 /]# ls -ld wonderful/
drwxr-xr-x. 2 root sysadmin 6 Aug  5 23:06 wonderful/

# Make sure newly created files within this directory inherits group permissions - setgid
[root@server2 /]# chmod g+s wonderful/
[root@server2 /]# ls -ld wonderful/
drwxr-sr-x. 3 root sysadmin 35 Aug  5 23:15 wonderful/

# All members of the group should have read and write access. All other users should not have any permissions.
[root@server2 /]# chmod 770 wonderful/
[root@server2 /]# ls -ld wonderful/
drwxrws---. 3 root sysadmin 35 Aug  5 23:15 wonderful/
```

---

**Q8: UPDATE KERNEL**

```
Update your kernel from http://content.example.com/rhel7.0/x86_64/errata/
```

**Solution:**

```bash
# Go to this path
[root@server2 yum.repos.d]# pwd
/etc/yum.repos.d

# Create a file with .repo extension and type repo details
[root@server2 yum.repos.d]# cat update_kernel.repo
[kernel_packages]
name=Kernel Repo
baseurl=http://content.example.com/rhel7.0/x86_64/errata/
enabled=1
gpgcheck=0

# lets go ahead and install the latest stable version of the kernel
[root@server2 yum.repos.d]# yum list kernel --showduplicates
Loaded plugins: langpacks
Installed Packages
kernel.x86_64                                          3.10.0-123.el7                                              installed
Available Packages
kernel.x86_64                                          3.10.0-123.el7                                              rhel_dvd
kernel.x86_64                                          3.10.0-123.1.2.el7                                          kernel_packages

# Check the current version of kernel
[root@server2 yum.repos.d]# uname -r
3.10.0-123.el7.x86_64

# Update the kernel. Note that the latest image from the newly created repo (kernel_packages) is picked and installed.
[root@server2 yum.repos.d]# yum update kernel
Loaded plugins: langpacks
Resolving Dependencies
--> Running transaction check
---> Package kernel.x86_64 0:3.10.0-123.1.2.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

==================================================================================================================================
 Package                  Arch                     Version                                Repository                         Size
==================================================================================================================================
Installing:
 kernel                   x86_64                   3.10.0-123.1.2.el7                     kernel_packages                    29 M

Transaction Summary
==================================================================================================================================
Install  1 Package

Total download size: 29 M
Installed size: 127 M
Is this ok [y/d/N]: y
Downloading packages:
No Presto metadata available for kernel_packages
kernel-3.10.0-123.1.2.el7.x86_64.rpm                                                                       |  29 MB  00:00:00
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : kernel-3.10.0-123.1.2.el7.x86_64                                                                               1/1
  Verifying  : kernel-3.10.0-123.1.2.el7.x86_64                                                                               1/1

Installed:
  kernel.x86_64 0:3.10.0-123.1.2.el7

Complete!

# Reboot the machine. We should now see the latest kernel version as default. We now see that both kernels are installed.
[root@server2 ~]# yum list kernel
Loaded plugins: langpacks
Installed Packages
kernel.x86_64                                         3.10.0-123.el7                                              installed
kernel.x86_64                                         3.10.0-123.1.2.el7                                          @kernel_packages

# Check which one is default. Yay! You now have the latest kernel version.
[root@server2 ~]# uname -r
3.10.0-123.1.2.el7.x86_64
```

---

**Q9: CRON JOB**

```
Alice must set a job to run every 7 minutes between 12 am and 2 am every day and the job is /bin/echo hi
```

**Solution:**

```bash
# Type crontab to open cron file
[root@server2 ~]# crontab -e

# Add this line in the crontab file
*/1 0-2 * * * /bin/echo hi >> /etc/myfirstcron
```

---

**Q10: CREATE USER WITH SPECIFIC UID**

```
Create a user ipsr with used id 3345.
```

**Solution:**

```bash
# Create a user with specific uid
[root@server2 ~]# useradd ipsr -u 3345

# Verify user's uid
[root@server2 ~]# cat /etc/passwd |grep ipsr
ipsr:x:3345:3345::/home/ipsr:/bin/bash
```

---

**Q11: SWAP PARTITION**

```
Create a swap partition of 256M and should be automatically available on reboot.
```

**Solution:**

1. Create a new partition with type swap.

```bash
# Swap disks are a special type of storage that are used to act like extra system ram. This is handy if your machine is running low on ram, although using swap can degrade performance. To see your ram info, you use the free command:

[root@server2 ~]# free -m
             total       used       free     shared    buffers     cached
Mem:          1841        795       1045         16          0        316
-/+ buffers/cache:        478       1362
Swap:            0          0          0

# Create a new parition with swap type
[root@server2 ~]# fdisk /dev/vdb
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table
Building a new DOS disklabel with disk identifier 0xd012e3a0.

Command (m for help): n
Partition type:
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p): p
Partition number (1-4, default 1): 1
First sector (2048-20971519, default 2048):
Using default value 2048
Last sector, +sectors or +size{K,M,G} (2048-20971519, default 20971519): +256M
Partition 1 of type Linux and of size 256 MiB is set

Command (m for help): p

Disk /dev/vdb: 10.7 GB, 10737418240 bytes, 20971520 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0xd012e3a0

   Device Boot      Start         End      Blocks   Id  System
/dev/vdb1            2048      526335      262144   83  Linux

Command (m for help): t
Selected partition 1
Hex code (type L to list all codes): L

 0  Empty           24  NEC DOS         81  Minix / old Lin bf  Solaris
 1  FAT12           27  Hidden NTFS Win 82  Linux swap / So c1  DRDOS/sec (FAT-
 2  XENIX root      39  Plan 9          83  Linux           c4  DRDOS/sec (FAT-
 3  XENIX usr       3c  PartitionMagic  84  OS/2 hidden C:  c6  DRDOS/sec (FAT-
 4  FAT16 <32M      40  Venix 80286     85  Linux extended  c7  Syrinx
 5  Extended        41  PPC PReP Boot   86  NTFS volume set da  Non-FS data
 6  FAT16           42  SFS             87  NTFS volume set db  CP/M / CTOS / .
 7  HPFS/NTFS/exFAT 4d  QNX4.x          88  Linux plaintext de  Dell Utility
 8  AIX             4e  QNX4.x 2nd part 8e  Linux LVM       df  BootIt
 9  AIX bootable    4f  QNX4.x 3rd part 93  Amoeba          e1  DOS access
 a  OS/2 Boot Manag 50  OnTrack DM      94  Amoeba BBT      e3  DOS R/O
 b  W95 FAT32       51  OnTrack DM6 Aux 9f  BSD/OS          e4  SpeedStor
 c  W95 FAT32 (LBA) 52  CP/M            a0  IBM Thinkpad hi eb  BeOS fs
 e  W95 FAT16 (LBA) 53  OnTrack DM6 Aux a5  FreeBSD         ee  GPT
 f  W95 Ext'd (LBA) 54  OnTrackDM6      a6  OpenBSD         ef  EFI (FAT-12/16/
10  OPUS            55  EZ-Drive        a7  NeXTSTEP        f0  Linux/PA-RISC b
11  Hidden FAT12    56  Golden Bow      a8  Darwin UFS      f1  SpeedStor
12  Compaq diagnost 5c  Priam Edisk     a9  NetBSD          f4  SpeedStor
14  Hidden FAT16 <3 61  SpeedStor       ab  Darwin boot     f2  DOS secondary
16  Hidden FAT16    63  GNU HURD or Sys af  HFS / HFS+      fb  VMware VMFS
17  Hidden HPFS/NTF 64  Novell Netware  b7  BSDI fs         fc  VMware VMKCORE
18  AST SmartSleep  65  Novell Netware  b8  BSDI swap       fd  Linux raid auto
1b  Hidden W95 FAT3 70  DiskSecure Mult bb  Boot Wizard hid fe  LANstep
1c  Hidden W95 FAT3 75  PC/IX           be  Solaris boot    ff  BBT
1e  Hidden W95 FAT1 80  Old Minix

# Choose option 82 for Linux swap type
Hex code (type L to list all codes): 82
Changed type of partition 'Linux' to 'Linux swap / Solaris'

# Save the changes
Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.
Syncing disks.

# Update partition table
[root@server2 ~]# partprobe
```

2. Run the command **mkswap** against the device/partition created earlier using fdisk/parted. Optionally **-L** can be used to set **LABEL** on the swap partition.

```  bash
# Use mkswap to create a swap space. -L is optional
[root@server2 ~]# mkswap -L swap1 /dev/vdb1
Setting up swapspace version 1, size = 262140 KiB
LABEL=swap1, UUID=42ba7017-096e-4fe7-a967-3f5589f1f348
```

3. Modify the `/etc/fstab` file to mount the new swap device on boot.

```bash
[root@server2 ~]# cat /etc/fstab

#
# /etc/fstab
# Created by anaconda on Wed May  7 01:22:57 2014
#
# Accessible filesystems, by reference, are maintained under '/dev/disk'
# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
#
UUID=9bf6b9f7-92ad-441b-848e-0257cbb883d1 /                       xfs     defaults        1 1
/dev/vdb1 swap swap defaults 0 0
```

4. Run the swapon command to enable all swap devices listed in the /etc/fstab file and verify the added swap using “swap -s”.

```bash
[root@server2 ~]# swapon -a
[root@server2 ~]# swapon -s
Filename                                Type            Size    Used    Priority
/dev/vdb1                               partition       262140  0       -1
```

5. Verify if swap space is applied

```bash
[root@server2 ~]# free -m
             total       used       free     shared    buffers     cached
Mem:          1841        799       1041         16          0        317
-/+ buffers/cache:        481       1360
Swap:          255          0        255
```

---

**Q12: LOCATE FILES**

```
Find all files owned by the user root and group mail, copy the output files to /root/findings.
```

**Solution:**

```bash
# Create a destination directory if it does not exist
[root@server2 /]# mkdir -p /root/findings

# Find all files owned by the user root and group mail
[root@server2 /]# find / -user root -group mail
find: ‘/proc/29915/task/29915/fd/6’: No such file or directory
find: ‘/proc/29915/task/29915/fdinfo/6’: No such file or directory
find: ‘/proc/29915/fd/6’: No such file or directory
find: ‘/proc/29915/fdinfo/6’: No such file or directory
/var/spool/mail

# Find all files owned by the user root and (-a option) group mail, copy the output files to /root/findings
[root@server2 /]# find / -user root -a -group mail -exec cp -r {} /root/findings \;
find: ‘/proc/29947/task/29947/fd/6’: No such file or directory
find: ‘/proc/29947/task/29947/fdinfo/6’: No such file or directory
find: ‘/proc/29947/fd/6’: No such file or directory
find: ‘/proc/29947/fdinfo/6’: No such file or directory

# Make sure the files are copied the destination directory
[root@server2 findings]# pwd
/root/findings
[root@server2 findings]# ll
total 0
drwxr-xr-x. 2 root root 75 Aug  6 00:51 mail
[root@server2 findings]# cd mail/
[root@server2 mail]# ll
total 0
-rw-r-----. 1 root root 0 Aug  6 00:51 alice
-rw-r-----. 1 root root 0 Aug  6 00:51 harry
-rw-r-----. 1 root root 0 Aug  6 00:51 ipsr
-rw-r-----. 1 root root 0 Aug  6 00:51 joy
-rw-r-----. 1 root root 0 Aug  6 00:51 rpc
-rw-r-----. 1 root root 0 Aug  6 00:51 student
```

---

**Q13: SEARCH WORDS**

```
Display the matches for the words which begin with "ns" in the /usr/share/dict/words and save the output to a file /home/student/locate.txt.
```

**Solution:**

```bash
# Use ^ for starting
[root@server2 dict]# grep ^ns words > /home/student/locate.txt
[root@server2 dict]# cat /home/student/locate.txt
ns
ns-a-vis
nsec
```

---

**Q14: AUTOFS**

```
- Bind your system to the LDAP server provided at classroom.example.com
- The base DN is dc=example,dc=com.
- You can download the TLS certificate from <http://classroom.example.com/pub/example-ca.crt>
- Use LDAP password for authentication and obtaining user information.
- Log in as ldapuserX, (where X is your foundation number) with password 'password'.
```

**Solution:**

***Note:*** LDAP should be configured before this step. Refer to **Q17**

1. Install `autofs` using `yum install autofs`

2. Create a new file in `/etc/auto.master.d` named `home.autofs`

   ```bash
   [root@server2 ~]# getent passwd ldapuser2
   ldapuser2:*:1702:1702:LDAP Test User 2:/home/guests/ldapuser2:/bin/bash
   
   [root@server2 auto.master.d]# vi home.autofs
   [root@server2 auto.master.d]# cat home.autofs
   /home/guests /etc/auto.home
   ```

3. Update `/etc/auto.home` with mount-point information from a different server and directory

   ```bash
   [root@server2 auto.master.d]# cat /etc/auto.home
   ldapuser2 -rw,sync,nfsvrs=3 classroom.example.com:/home/guests/ldapuser2
   ```

4. Start  `autofs` service and verify if it is active

   ```bash
   [root@server2 auto.master.d]# systemctl start autofs
   
   [root@server2 auto.master.d]# systemctl status autofs
   autofs.service - Automounts filesystems on demand
      Loaded: loaded (/usr/lib/systemd/system/autofs.service; disabled)
      Active: active (running) since Sun 2018-06-24 02:10:20 IST; 7s ago
     Process: 30292 ExecStart=/usr/sbin/automount $OPTIONS --pid-file /run/autofs.pid (code=exited, status=0/SUCCESS)
    Main PID: 30294 (automount)
      CGroup: /system.slice/autofs.service
              └─30294 /usr/sbin/automount --pid-file /run/autofs.pid
   
   Jun 24 02:10:20 server2.example.com systemd[1]: Starting Automounts filesystems on demand...
   Jun 24 02:10:20 server2.example.com automount[30294]: setautomntent: lookup(sss): setautomntent: No such file or directory
   Jun 24 02:10:20 server2.example.com systemd[1]: Started Automounts filesystems on demand.
   ```

5. ssh as `ldapuser2` into `localhost` and verify

   ```bash
   [root@server2 auto.master.d]# ssh ldapuser2@localhost
   The authenticity of host 'localhost (::1)' can't be established.
   ECDSA key fingerprint is 65:4d:ac:8a:c9:58:82:b5:0c:91:c4:ef:a5:e6:f6:65.
   Are you sure you want to continue connecting (yes/no)? yes
   Warning: Permanently added 'localhost' (ECDSA) to the list of known hosts.
   ldapuser2@localhost's password: 
   
   [ldapuser2@server2 ~]$ pwd
   /home/guests/ldapuser2
   
   [ldapuser2@server2 ~]$ df -h .
   Filesystem                                    Size  Used Avail Use% Mounted on
   classroom.example.com:/home/guests/ldapuser2   10G  3.7G  6.4G  37% /home/guests/ldapuser2
   ```

---

**Q15: LVMRESIZE**

```
Resize the logical volume 'm7_storage' to 900M which belongs to the volume group 'vgroup'.
```

**Solution:**

```bash
# Check how much space VG has
[root@server2 ~]# vgs
  VG     #PV #LV #SN Attr   VSize VFree
  vgroup   2   1   0 wz--n- 2.99g 1.72g

# Check the original size of LV
[root@server2 ~]# lvs
  LV         VG     Attr       LSize   Pool Origin Data%  Move Log Cpy%Sync Convert
  m7_storage vgroup -wi-a----- 500.00m

# Evaluate by how should you increase/decrease. In this case, increase by 400M.
[root@server2 ~]# lvresize --size +400M /dev/vgroup/m7_storage
  Extending logical volume m7_storage to 900.00 MiB
  Logical volume m7_storage successfully resized

# Verify
[root@server2 ~]# lvs
  LV         VG     Attr       LSize   Pool Origin Data%  Move Log Cpy%Sync Convert
  m7_storage vgroup -wi-a----- 900.00m

```

---

**Q16: BACKUP FILES**

```
Create an bzip2 archive /root/today_backup.tar.bz2 which stores the backup of /etc .
```

**Solution:**

```bash
# Tar using bzip2 (j)
[root@server2 etc]# tar -jcf /root/today_backup.tar.bz2 /etc
tar: Removing leading `/' from member names

# Verify if the tarred file exists
[root@server2 etc]# ls -ld /root/today_backup.tar.bz2
-rw-r--r--. 1 root root 7309242 Aug  7 00:05 /root/today_backup.tar.bz2

[root@server2 etc]# cd /root/
[root@server2 ~]# ll
total 7152
-rw-------. 1 root root    8619 May  7  2014 anaconda-ks.cfg
-rw-r--r--. 1 root root 7309242 Aug  7 00:05 today_backup.tar.bz2
```

---

**Q17: ACCESS NETWORK USERS**

```
- Bind your system to the LDAP server provided at classroom.example.com
- The base DN is `dc=example,dc=com`.
- You can download the TLS certificate from <http://classroom.example.com/pub/example-ca.crt>
- Use LDAP password for authentication and obtaining user information.
- Log in as ldapuserX, (where X is your foundation number) with password 'password'.
```

**Solution:  **

1. Install `authconfig-gtk` and `sssd` packages using `yum -y install authconfig-gtk sssd`.

2. You will get a pop-up window, fill all LDAP details in the window and apply the changes.

   ![Authconfig Popup Window](Redhat Images/authconfig-gtk.png)

3. Verify if the user is added to LDAP.

   ```bash
   [root@server2 ~]# getent passwd ldapuser2
   ldapuser2:*:1702:1702:LDAP Test User 2:/home/guests/ldapuser2:/bin/bash
   ```



