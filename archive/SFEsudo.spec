#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define tarball_version 1.6.9p14

Name:                SFEsudo
Summary:             Provides limited super user privs to specific users
URL:                 http://www.sudo.ws/sudo/
Version:             1.6.9
Source:              http://www.sudo.ws/sudo/dist/sudo-%{tarball_version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: %{name}-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n sudo-%{tarball_version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --libexecdir=%{_libexecdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%attr(4111,root,root) %{_bindir}/sudo
%attr(4111,root,root) %{_bindir}/sudoedit
%dir %attr (0755, root, bin) %{_sbindir}
%attr(0111,root,root) %{_sbindir}/visudo
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1m
%{_mandir}/man1m/*
%dir %attr (0755, root, bin) %{_mandir}/man4
%{_mandir}/man4/*


%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%attr(0440,root,root)  %{_sysconfdir}/sudoers

%changelog
* Fri Aug 29 2008 - Pradhap Devarajan < pradhap (at) gmail (dot) com>
- update the file permissions
* Fri Mar 07 2008 - trisk@acm.jhu.edu
- Bump to 1.6.9p14, add URL
* Wed Feb 06 2008 - Ananth Shrinivas <ananth@sun.com>
- updated to sudo 1.6.9p12
* Sat Dec 15 2007 - Ananth Shrinivas <ananth@sun.com>
- updated to sudo 1.6.9p9
* Mon Sep 03 2007 - Ananth Shrinivas <ananth@sun.com>
- updated to new sudo version
* Thu Nov 09 2006 - Eric Boutilier
- Initial spec
