#
# spec file for package SFEamanda
#
%include Solaris.inc

%define src_name	amanda

%define amanda_user	amandabackup
%define amanda_indexserver	amandahost
%define amanda_tapeserver	%{indexserver}

%define perl_version	5.8.4

Name:		SFEamanda
Summary:	A network-capable tape backup solution
Version:	3.1.0
Source:		%{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
License:	BSD
Group:		Applications/System
URL:		http://www.amanda.org
SUNW_BaseDir:	/
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

BuildRequires:	SUNWgnome-common-devel
Buildrequires:	SUNWgnu-readline

Requires:	SUNWgnuplot
Requires:	SUNWgnu-readline
#Requires:	SUNWmtx
BuildRequires:	SUNWperl584usr
Requires:	SUNWperl584usr

%description 
AMANDA, the Advanced Maryland Automatic Network Disk Archiver, is a
backup system that allows the administrator of a LAN to set up a
single master backup server to back up multiple hosts to one or more
tape drives or disk files.  AMANDA uses native dump and/or GNU tar
facilities and can back up a large number of workstations running
multiple versions of Unix.  Newer versions of AMANDA (including this
version) can use SAMBA to back up Microsoft(TM) Windows95/NT hosts.
The amanda package contains the core AMANDA programs and will need to
be installed on both AMANDA clients and AMANDA servers.  Note that you
will have to install the amanda-client and/or amanda-server packages as
well.

%package client
Name:		%{name}-client
Summary:	The client component of the AMANDA tape backup system
Group:		Applications/System
Requires:	%{name}

%description client
The Amanda-client package should be installed on any machine that will
be backed up by AMANDA (including the server if it also needs to be
backed up).  You will also need to install the amanda package on each
AMANDA client machine.

%package server
Name:		%{name}-server
Summary:	The server side of the AMANDA tape backup system
Group:		Applications/System
Requires:	%{name}

%description server
The amanda-server package should be installed on the AMANDA server,
the machine attached to the device(s) (such as a tape drive) where backups
will be written. You will also need to install the amanda package on
the AMANDA server machine.  And, if the server is also to be backed up, the
server also needs to have the amanda-client package installed.

%package devel
Name:		%{name}-devel
Summary:	Libraries and documentation of the AMANDA tape backup system
Group:		Development/Libraries
Requires:	%{name}

%description devel
The amanda-devel package should be installed on any machine that will
be used to develop amanda applications.

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
./autogen

./configure --prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir}	\
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--enable-threads=solaris	\
	--disable-s3-device		\
	--enable-shared			\
	--disable-static		\
	--disable-dependency-tracking	\
	--disable-installperms		\
	--with-user=%amanda_user	\
	--with-group=sys		\
	--with-gnutar=/usr/bin/gtar	\
	--with-tmpdir=/var/log/amanda	\
	--with-fqdn			\
	--with-gnuplot=/usr/bin/gnuplot	\
	--with-index-server=%{amanda_indexserver}	\
	--with-tape-server=%{amanda_tapeserver}	\
	--with-amperldir=%{_prefix}/perl5/vendor_perl/%{perl_version} \
	--with-bsdtcp-security		\
	--with-bsdudp-security		\
	--with-rsh-security		\
	--with-amandahosts		\
	--with-smbclient=%{_bindir}/smbclient	\
	--with-readline
	
make -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT

make install BINARY_OWNER=%(id -un) SETUID_GROUP=%(id -gn) DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/amanda
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/amanda
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/amanda

find $RPM_BUILD_ROOT -name \*.la | xargs rm

rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias

%clean 
rm -rf ${RPM_BUILD_ROOT}

%pre
test -x /usr/lib/postrun || exit 0
(
  echo '/usr/sbin/useradd -d %{_localstatedir}/lib/amanda -s /bin/bash -g sys %{amanda_user}';
) | /usr/lib/postrun -i -a

%postun
test -x /usr/lib/postrun || exit 0
(
  echo '/usr/sbin/userdel %{amanda_user}';
) | /usr/lib/postrun -i -a

%actions
user ftpuser=false gcos-field="Amanda Reserved UID" username="%{amanda_user}" password=NP group="sys"

%files
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%attr(-,%amanda_user, sys)	%{_libdir}/amanda/lib*-*.so
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/amanda-sh-lib.sh
%attr(-,%amanda_user, sys)	%{_prefix}/perl5/vendor_perl/%{perl_version}/auto/Amanda/
%attr(-,%amanda_user, sys)	%{_prefix}/perl5/vendor_perl/%{perl_version}/Amanda/
%attr(-,%amanda_user, sys)	%{_sbindir}/amrestore
%attr(-,%amanda_user, sys)	%{_sbindir}/amarchiver
%{_mandir}/man8/amrestore.8
%{_mandir}/man8/amarchiver.8
%{_mandir}/man8/script-email.8
%{_mandir}/man8/amraw.8 
%{_mandir}/man8/amsuntar.8 
%{_mandir}/man8/ampgsql.8
%{_mandir}/man5/amanda-archive-format.5
%{_mandir}/man7/amanda-auth.7
%{_mandir}/man7/amanda-scripts.7
%{_mandir}/man7/amanda-compatibility.7 

%dir %attr(-, root, sys) %{_localstatedir}
%dir %attr(-, root, sys) %{_localstatedir}/log
%dir %attr(02700,%amanda_user, sys) %{_localstatedir}/log/amanda
%dir %attr(-, root, other) %{_localstatedir}/lib
%dir %attr(-,%amanda_user, sys)	%{_localstatedir}/lib/amanda/
%dir %attr(-, root, sys) %{_sysconfdir}
%dir %attr(-,%amanda_user, sys)	%{_sysconfdir}/amanda/

%{_mandir}/man5/amanda.conf*

%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/amanda/ChangeLog
%{_datadir}/amanda/ReleaseNotes
%{_datadir}/amanda/COPYRIGHT
%{_datadir}/amanda/NEWS

%files server
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/amidxtaped
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/amindexd
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/amlogroll
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/amtrmidx
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/amtrmlog
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/driver
%attr(4750,root, sys)		%{_libexecdir}/amanda/dumper
%attr(4750,root, sys)		%{_libexecdir}/amanda/planner
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/taper
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/chunker
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/amcleanupdisk
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/chg-chio
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/chg-chs
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/chg-juke
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/chg-manual
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/chg-mcutil
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/chg-mtx
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/chg-multi
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/chg-null
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/chg-rait
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/chg-rth
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/chg-scsi
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/chg-zd-mtx
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/chg-disk
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/chg-iomega
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/chg-lib.sh
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/amcat.awk
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/amplot.awk
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/amplot.g
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/amplot.gp
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/ndmjob
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/amndmjob
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/amcheck-device

%attr(-,%amanda_user, sys)	%{_sbindir}/amaespipe
%attr(-,%amanda_user, sys)	%{_sbindir}/amaddclient
%attr(-,%amanda_user, sys)	%{_sbindir}/amadmin
%attr(4750,root, sys)		%{_sbindir}/amcheck
%attr(-,%amanda_user, sys)	%{_sbindir}/amcheckdump
%attr(-,%amanda_user, sys)	%{_sbindir}/amcrypt
%attr(-,%amanda_user, sys)	%{_sbindir}/amcryptsimple
%attr(-,%amanda_user, sys)	%{_sbindir}/amcrypt-ossl
%attr(-,%amanda_user, sys)	%{_sbindir}/amcrypt-ossl-asym
%attr(-,%amanda_user, sys)	%{_sbindir}/amdevcheck
%attr(-,%amanda_user, sys)	%{_sbindir}/amflush
%attr(-,%amanda_user, sys)	%{_sbindir}/amgetconf
%attr(-,%amanda_user, sys)	%{_sbindir}/amgpgcrypt
%attr(-,%amanda_user, sys)	%{_sbindir}/amlabel
%attr(-,%amanda_user, sys)	%{_sbindir}/amtape
%attr(-,%amanda_user, sys)	%{_sbindir}/amreport
%attr(-,%amanda_user, sys)	%{_sbindir}/amcheckdb
%attr(-,%amanda_user, sys)	%{_sbindir}/amcleanup
%attr(-,%amanda_user, sys)	%{_sbindir}/amdump
%attr(-,%amanda_user, sys)	%{_sbindir}/amoverview
%attr(-,%amanda_user, sys)	%{_sbindir}/amrmtape
%attr(-,%amanda_user, sys)	%{_sbindir}/amtoc
%attr(-,%amanda_user, sys)	%{_sbindir}/amserverconfig
%attr(-,%amanda_user, sys)	%{_sbindir}/amstatus
%attr(-,%amanda_user, sys)	%{_sbindir}/amplot
%attr(-,%amanda_user, sys)	%{_sbindir}/amtapetype
%attr(-,%amanda_user, sys)	%{_sbindir}/amservice
%attr(-,%amanda_user, sys)	%{_sbindir}/amvault

%dir %attr(-, root, sys) %{_sysconfdir}
%attr(-,%amanda_user, sys)	%dir %{_sysconfdir}/amanda

%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/amanda/template.d
%{_datadir}/amanda/example/amanda.conf
%{_datadir}/amanda/example/xinetd.amandaserver
%{_datadir}/amanda/example/inetd.conf.amandaserver
%{_datadir}/amanda/example/chg-multi.conf
%{_datadir}/amanda/example/chg-scsi.conf
%{_datadir}/amanda/example/label-templates
%{_datadir}/amanda/example/disklist

%{_mandir}/man8/amadmin.8
%{_mandir}/man8/amaespipe.8
%{_mandir}/man8/amaddclient.8
%{_mandir}/man8/amanda.8
%{_mandir}/man8/amcheck.8
%{_mandir}/man8/amcheckdb.8
%{_mandir}/man8/amcheckdump.8
%{_mandir}/man8/amcleanup.8
%{_mandir}/man8/amcrypt.8
%{_mandir}/man8/amcryptsimple.8
%{_mandir}/man8/amdevcheck.8
%{_mandir}/man8/amdump.8
%{_mandir}/man8/amflush.8
%{_mandir}/man8/amgetconf.8
%{_mandir}/man8/amgpgcrypt.8
%{_mandir}/man8/amlabel.8
%{_mandir}/man8/amservice.8
%{_mandir}/man8/amvault.8
%{_mandir}/man8/amoverview.8
%{_mandir}/man8/amplot.8
%{_mandir}/man8/amreport.8
%{_mandir}/man8/amrmtape.8
%{_mandir}/man8/amserverconfig.8
%{_mandir}/man8/amstatus.8
%{_mandir}/man8/amtape.8
%{_mandir}/man8/amtapetype.8
%{_mandir}/man8/amtoc.8
%{_mandir}/man8/amcrypt-ossl.8
%{_mandir}/man8/amcrypt-ossl-asym.8
%{_mandir}/man7/amanda-changers.7
%{_mandir}/man7/amanda-devices.7
%{_mandir}/man7/amanda-taperscan.7 
%{_mandir}/man5/disklist.5
%{_mandir}/man5/tapelist.5

%files client
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/amandad
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/application/
%attr(4750,root, sys)		%{_libexecdir}/amanda/calcsize
%attr(4750,root, sys)		%{_libexecdir}/amanda/killpgrp
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/noop
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/patch-system
%attr(4750,root, sys)		%{_libexecdir}/amanda/rundump
%attr(4750,root, sys)		%{_libexecdir}/amanda/runtar
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/selfcheck
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/sendbackup
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/sendsize
%attr(-,%amanda_user, sys)	%{_libexecdir}/amanda/teecount
%attr(-,%amanda_user, sys)	%{_sbindir}/amfetchdump
%{_mandir}/man8/amfetchdump.8
%attr(-,%amanda_user, sys)	%{_sbindir}/amrecover
%attr(-,%amanda_user, sys)	%{_sbindir}/amoldrecover
%{_mandir}/man8/amrecover.8
%{_mandir}/man8/amgtar.8
%{_mandir}/man8/amsamba.8
%{_mandir}/man8/amstar.8
%{_mandir}/man8/amzfs-sendrecv.8
%{_mandir}/man8/amzfs-snapshot.8
%{_mandir}/man5/amanda-client.conf.5
%{_mandir}/man7/amanda-applications.7

%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/amanda/example/xinetd.amandaclient
%{_datadir}/amanda/example/inetd.conf.amandaclient
%{_datadir}/amanda/example/amanda-client-postgresql.conf
%{_datadir}/amanda/example/amanda-client.conf


%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%{_includedir}/amanda/
%{_libdir}/amanda/libamanda.so
%{_libdir}/amanda/libamdevice.so
%{_libdir}/amanda/libamclient.so
%{_libdir}/amanda/libamserver.so
%{_libdir}/amanda/libamandad.so
%{_libdir}/amanda/libamar.so
%{_libdir}/amanda/libamxfer.so
%{_libdir}/amanda/libamglue.so
%{_libdir}/amanda/libndmjob.so
%{_libdir}/amanda/libndmlib.so


%changelog
* Sun Jul 11 2010 - Milan Jurik
- Initial spec based on Fedora
