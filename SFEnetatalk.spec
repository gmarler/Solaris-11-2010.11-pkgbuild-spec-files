#
# spec file for package: netatalk
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# include module(s): 
#
%include Solaris.inc

Name:           SFEnetatalk
Summary:        Open Source AFP fileserver
Version:        2.1.2
Epoch:          1
License:        GPLv3
Copyright:	GPLv3
Source:         %{sf_download}/netatalk/netatalk-%{version}.tar.bz2
URL:            http://netatalk.sourceforge.net/
Group:          Network
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community
%include default-depend.inc
BuildRequires:  bdb
Requires:       bdb
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
SUNW_Basedir:   /
%define _sysconfdir /etc
SUNW_Copyright: %{name}.copyright

# OpenSolaris IPS Manifest Fields
Meta(info.upstream): http://netatalk.sourceforge.net/ 
Meta(info.repository_url): http://netatalk.cvs.sourceforge.net/viewvc/netatalk/netatalk/
Meta(info.maintainer): <netatalk-devel@lists.sourceforge.net>

%description
Netatalk is a freely-available, kernel level implementation of the AppleTalk Protocol Suite, originally for BSD-derived systems. A *NIX/*BSD system running netatalk is capable of serving many macintosh clients simultaneously as an AppleTalk router, AppleShare file server (AFP), *NIX/*BSD print server, and for accessing AppleTalk printers via Printer Access Protocol (PAP). Included are a number of minor printing and debugging utilities.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
%setup -q -n netatalk-%{version}

%build
export CFLAGS="%optflags -xc99=all "
#export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}                  \
            --bindir=%{_bindir}                  \
            --mandir=%{_mandir}                  \
            --infodir=%{_infodir}                \
            --libexecdir=%{_libexecdir}/netatalk \
            --sysconfdir=%{_sysconfdir}          \
            --with-uams-path=%{_libdir}/netatalk \
            --with-spooldir=/var/spool/netatalk  \
            --disable-ddp                        \
            --with-pam \
            --enable-nfsv4acls

make

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
  DESTDIR=$RPM_BUILD_ROOT \
  MANDIR=$RPM_BUILD_ROOT%{_mandir}

install -D -m 755 distrib/initscripts/rc.atalk.sysv $RPM_BUILD_ROOT%{_sysconfdir}/init.d/netatalk
rm -rf $RPM_BUILD_ROOT/var/tmp
rm -rf $RPM_BUILD_ROOT/usr/lib/security

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %name-%version

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/netatalk
%dir %attr (0755, root, sys) %{_sysconfdir}/init.d
%dir %attr (0755, root, bin) %{_libdir}/netatalk
%dir %attr (-,-,-) %{_datadir}
%dir %attr (-,-,-) %{_datadir}/aclocal
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/netatalk/AppleVolumes.default
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/netatalk/AppleVolumes.system
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/netatalk/afpd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/netatalk/atalkd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/netatalk/papd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/netatalk/netatalk.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/netatalk/afp_ldap.conf
%{_sysconfdir}/init.d/netatalk

%attr(755,root,bin) %{_sbindir}/*
%attr(755,root,bin) %{_bindir}/[!n]*
%attr(755,root,bin) %{_bindir}/n[!e]*
%attr(755,root,bin) %{_bindir}/netacnv
%{_mandir}/*/*

%attr(755,root,bin) %{_bindir}/netatalk-config
%{_libexecdir}/netatalk/ifwmpap
%{_libexecdir}/netatalk/ifpaprev
%{_libexecdir}/netatalk/ofwpap
%{_libexecdir}/netatalk/tfwmpaprev
%{_libexecdir}/netatalk/ifmpap
%{_libexecdir}/netatalk/tfmpap
%{_libexecdir}/netatalk/tfwpaprev
%{_libexecdir}/netatalk/ifpap
%{_libexecdir}/netatalk/tfpaprev
%{_libexecdir}/netatalk/ifwmpaprev
%{_libexecdir}/netatalk/ofmpap
%{_libexecdir}/netatalk/tfwmpap
%{_libexecdir}/netatalk/ifmpaprev
%{_libexecdir}/netatalk/ofwmpap
%{_libexecdir}/netatalk/ofpap
%{_libexecdir}/netatalk/etc2ps.sh
%{_libexecdir}/netatalk/tfmpaprev
%{_libexecdir}/netatalk/tfpap
%{_libexecdir}/netatalk/psf
%{_libexecdir}/netatalk/ifwpaprev
%{_libexecdir}/netatalk/tfwpap
%{_libexecdir}/netatalk/ifwpap
%{_libexecdir}/netatalk/psa
%{_libdir}/netatalk/*.so*
%{_prefix}/share/netatalk/*
%{_prefix}/share/aclocal/*
%dir /var/spool/netatalk


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/atalk
%dir %attr (0755, root, bin) %{_includedir}/netatalk
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/netatalk/*.a
%{_libdir}/netatalk/*.la
%{_includedir}/atalk/*
%{_includedir}/netatalk/*


%changelog
* Di Jun 29 2010 -  Michal Bielicki cypromis@opensolaris.org
- bumped up version to 2.1.2
- fixed some missing included
- fixed files
- added devel package
- created SFE version
- cleared some attributes
- added pam support
* Sun Apr 04 2010 - yabawock@gmail.com
- New upstream release
- Enable support for NFSv4 ACLs

* Wed Feb 17 2010 - sebastian.laubscher@interdose.com
- initial version
