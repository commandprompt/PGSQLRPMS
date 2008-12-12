##########################################################################
#    Kickstart file for Fedora PostgreSQL Spin, with PGDG packages. 	 #
#            Devrim GUNDUZ <devrim@commandprompt.com>		 	 #
#									 #
# $Id$									 #
#									 #
# Some parts of this ks file is based on livecd-fedora-8-base-desktop.ks #
##########################################################################

#platform=x86, AMD64, or Intel EM64T
# Network information
network  --bootproto=dhcp --device=eth0 --onboot=on
# Root password
rootpw --iscrypted $1$1QGU.fEd$ZVmp27WLFAyAGjpBZ4JNk0
# System authorization information
auth  --useshadow  --enablemd5
# Use graphical install
graphical
# Firewall configuration
firewall --disabled
firstboot --disable
# System keyboard
keyboard us
# System language
lang en_US.UTF-8
# SELinux configuration
selinux --disabled
# Install OS instead of upgrade
install
# Use CDROM installation media
cdrom
# System timezone
timezone  America/New_York
# X Window System configuration information
xconfig  --defaultdesktop=GNOME --depth=32 --resolution=1024x768 --startxonboot
# System bootloader configuration
bootloader --location=mbr
# Partition clearing information
clearpart --all  
part / --size 4096

# List of repositories. We want to stick to x86 builds only.

# These are the private mirror list for local builds (Devrim).
#repo --name=released --baseurl=http://fedora.mirror.homenet.dbitech.bc.ca/releases/10/Everything/i386/os/
#repo --name=updates --baseurl=http://fedora.mirror.homenet.dbitech.bc.ca/updates/10/i386/

# These are the public repositories
repo --name=released --mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=fedora-10&arch=i386
repo --name=updates --mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=updates-released-f10&arch=i386

# PGDG RPM Repository
repo --name=pgdg83  --baseurl=http://yum.pgsqlrpms.org/8.3/fedora/fedora-10-i386

%packages
@base-x
@base
@core
@admin-tools
@hardware-support
kernel
@gnome-desktop
@turkish-support
@base
@hardware-support
@sql-server
@graphical-internet
check_postgres
esc
evolution
evolution-webcal
dejavu-fonts
dejavu-fonts-experimental
dejavu-fonts
dejavu-fonts-experimental
httpd
ip4r
table_log
orafce
pagila
pam_pgsql
phpPgAdmin
pg_top
pg_filedump
pgadmin3
pgbouncer
pgfouine
pgloader
pgplsh
pgsphere
pgpool-II
plproxy
plruby
postgis
postgis-utils
postgis-jdbc
postgresql
postgresql-docs
postgresql-contrib
postgresql-jdbc
postgresql-odbc
postgresql-plperl
postgresql-plpython
postgresql-pltcl
postgresql-python
postgresql-server
postgresql-tcl
postgresql-test
prefix
python-psycopg2
ruby-pg
skytools
table_log
usda-r18

# Save some space
-bittorrent
-fetchmail
-slrn
-cadaver
-mutt
-tomboy
-vino
-zenity
-xdg-user-dirs-gtk
-gnome-power-manager
-alacarte
-gnome-backgrounds
-at-spi
-gnome-bluetooth
-gucharmap
-gok
-gnome-audio
-gnome-phone-manager
-nautilus-cd-burner
-bluez-gnome
-bug-buddy
-gnome-vfs2-obexftp
-nautilus-sendto
-gnome-media
-gnome-vfs2-smb
-gcalctool
-gnome-pilot
-orca
-sendmail
-rsh
-mtr
-transmission
-evolution-help
-ekiga
-smolt
-firstboot
-gutenprint
-foomatic
-gthumb
-foomatic
-system-config-printer-libs
-system-config-printer 
-gstreamer-plugins-base 
-gstreamer-plugins-good
-gstreamer
-nautilus-cd-burner
-isdn4k-utils
-system-config-printer 
-specspo
-esc
-samba-client
-a2ps
-mpage
-redhat-lsb
-sox
-hplip
-hpijs
-xsane
-xsane-gimp
-sane-backends
# smartcards won't really work on the livecd.
-coolkey
-ccid
# duplicate functionality
-pinfo
-vorbis-tools
# lose the compat stuff
-compat*
# qlogic firmwares
-ql2100-firmware
-ql2200-firmware
-ql23xx-firmware
-ql2400-firmware
# livecd bits to set up the livecd and be able to install
anaconda
isomd5sum

# Need to prevent conflicts
-rhdb-utils

# make sure debuginfo doesn't end up on the live image
-*debuginfo

%post
cat > /etc/rc.d/init.d/fedora-live << EOF
#!/bin/bash
#
# live: Init script for live image
#
# chkconfig: 345 00 99
# description: Init script for live image.

. /etc/init.d/functions

if ! strstr "\`cat /proc/cmdline\`" liveimg || [ "\$1" != "start" ] || [ -e /.liveimg-configured ] ; then
    exit 0
fi

exists() {
    which \$1 >/dev/null 2>&1 || return
    \$*
}

touch /.liveimg-configured

# mount live image
if [ -b /dev/live ]; then
   mkdir -p /mnt/live
   mount -o ro /dev/live /mnt/live
fi

# read some variables out of /proc/cmdline
for o in \`cat /proc/cmdline\` ; do
    case \$o in
    ks=*)
        ks="\${o#ks=}"
        ;;
    xdriver=*)
        xdriver="--set-driver=\${o#xdriver=}"
        ;;
    esac
done


# if liveinst or textinst is given, start anaconda
if strstr "\`cat /proc/cmdline\`" liveinst ; then
   /usr/sbin/liveinst \$ks
fi
if strstr "\`cat /proc/cmdline\`" textinst ; then
   /usr/sbin/liveinst --text \$ks
fi

# enable swaps unless requested otherwise
swaps=\`blkid -t TYPE=swap -o device\`
if ! strstr "\`cat /proc/cmdline\`" noswap -a [ -n "\$swaps" ] ; then
  for s in \$swaps ; do
    action "Enabling swap partition \$s" swapon \$s
  done
fi

# configure X, allowing user to override xdriver
exists system-config-display --noui --reconfig --set-depth=24 \$xdriver

# add set no password for postgres user. It is already created with postgresql-server RPM.
passwd -d postgres > /dev/null

# turn off firstboot for livecd boots
echo "RUN_FIRSTBOOT=NO" > /etc/sysconfig/firstboot

# don't start yum-updatesd for livecd boots
chkconfig --level 345 yum-updatesd off 2>/dev/null

# don't start cron/at as they tend to spawn things which are
# disk intensive that are painful on a live image
chkconfig --level 345 crond off 2>/dev/null
chkconfig --level 345 atd off 2>/dev/null
chkconfig --level 345 anacron off 2>/dev/null
chkconfig --level 345 readahead_early off 2>/dev/null
chkconfig --level 345 readahead_later off 2>/dev/null

# Disable cups,rpcbind and sshd for this spin
chkconfig cups off 2>/dev/null
chkconfig sshd off 2>/dev/null
chkconfig rpcbind off 2>/dev/null

# Enable NetworkManager for this spin
chkconfig NetworkManager on

# Start PostgreSQL and Apache for this spin.
# We need Apache for phpPgAdmin
chkconfig postgresql on 2>/dev/null
chkconfig httpd on 2>/dev/null
service httpd start
# PostgreSQL needs some additional interest on it
# Let's run our initdb. RPM runs initdb's with --auth='ident sameuser', 
# but we don't need/want it in the live CD.
su -l postgres -c "initdb -D /var/lib/pgsql/data"
service postgresql start

# Stopgap fix for RH #217966; should be fixed in HAL instead
touch /media/.hal-mtab

# workaround clock syncing on shutdown that we don't want (#297421)
sed -i -e 's/hwclock/no-such-hwclock/g' /etc/rc.d/init.d/halt

#Create Desktop directory for postgres user:
su -l postgres -c "mkdir /var/lib/pgsql/Desktop"

EOF

# workaround avahi segfault (#279301)
touch /etc/resolv.conf
/sbin/restorecon /etc/resolv.conf

chmod 755 /etc/rc.d/init.d/fedora-live
/sbin/restorecon /etc/rc.d/init.d/fedora-live
/sbin/chkconfig --add fedora-live

# save a little bit of space at least...
rm -f /boot/initrd*
# make sure there aren't core files lying around
rm -f /core*

# disable screensaver locking
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s -t bool /apps/gnome-screensaver/lock_enabled false >/dev/null
# set up timed auto-login for after 60 seconds
sed -i -e 's/\[daemon\]/[daemon]\nTimedLoginEnable=true\nTimedLogin=fedora\nTimedLoginDelay=60/' /etc/gdm/custom.conf
if [ -e /usr/share/icons/hicolor/96x96/apps/fedora-logo-icon.png ] ; then
    cp /usr/share/icons/hicolor/96x96/apps/fedora-logo-icon.png /home/fedora/.face
    chown fedora:fedora /home/fedora/.face
    # TODO: would be nice to get e-d-s to pick this one up too... but how?
fi

# Create a conf file for pgadmin3. 
cat > /var/lib/pgsql/.pgadmin3 << EOF
ShowTipOfTheDay=false
[Updates]
pgsql-Versions=8.3
[Servers]
Count=1
[Servers/1]
Server=localhost
Description=postgresql-livecd
ServiceID=
Port=5432
StorePwd=true
Restore=true
Database=postgres
Username=postgres
LastDatabase=
LastSchema=
DbRestriction=
SSL=-1
[Properties]
[Properties/Server]
Left=238
Top=160
[frmMain]
Perspective-6930=layout2|name=objectBrowser;caption=Object browser;state=16779260;dir=4;layer=1;row=0;pos=0;prop=100000;bestw=200;besth=450;minw=100;minh=200;maxw=-1;maxh=-1;floatx=236;floaty=222;floatw=-1;floath=-1|name=listViews;caption=Info pane;state=1020;dir=5;layer=0;row=0;pos=0;prop=100000;bestw=400;besth=200;minw=200;minh=100;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1|name=sqlPane;caption=SQL pane;state=16779260;dir=3;layer=0;row=0;pos=0;prop=100000;bestw=400;besth=200;minw=200;minh=100;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1|name=toolBar;caption=Tool bar;state=16788208;dir=1;layer=10;row=0;pos=0;prop=100000;bestw=525;besth=44;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1|dock_size(5,0,0)=202|dock_size(3,0,0)=228|dock_size(1,10,0)=46|dock_size(4,1,0)=233|
[frmQuery]
MaxRows=100
MaxColSize=256
ExplainVerbose=false
ExplainAnalyze=false
Font=monospace 12
[Export]
Unicode=false
QuoteChar="\""
ColSeparator=;
RowSeparator=LF
Quote=Strings
[Copy]
QuoteChar="\""
ColSeparator=;
Quote=Strings
EOF

chown postgres: /var/lib/pgsql/.pgadmin3

%end

%post --nochroot
cp $INSTALL_ROOT/usr/share/doc/*-release-*/GPL $LIVE_ROOT/GPL
cp $INSTALL_ROOT/usr/share/doc/HTML/readme-live-image/en_US/readme-live-image-en_US.txt $LIVE_ROOT/README

# only works on x86, x86_64
if [ "$(uname -i)" = "i386" -o "$(uname -i)" = "x86_64" ]; then
  cp /usr/bin/livecd-iso-to-disk $LIVE_ROOT/LiveOS
fi
%end
