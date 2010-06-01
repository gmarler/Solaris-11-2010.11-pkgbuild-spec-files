#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEfreeradius
Summary:             FreeRADIUS - modular, high performance and feature-rich RADIUS suite
Version:             1.1.7
Source:              ftp://ftp.freeradius.org/pub/radius/freeradius-%{version}.tar.bz2
Patch1:              freeradius-01-types.diff
Patch2:              freeradius-02-makefiles.diff
URL:                 http://www.freeradius.org/

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWkrbu
BuildRequires: SUNWopenssl-include
BuildRequires: SUNWgnu-dbm
BuildRequires: SUNWmysqlu
BuildRequires: SUNWperl584core
Requires: SUNWkrbu
Requires: SUNWopenssl-libraries
Requires: SUNWgnu-dbm

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n freeradius-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags `krb5-config --cflags` -I/usr/sfw/include"
export LDFLAGS="%_ldflags `krb5-config --libs` -L/usr/sfw/lib -R/usr/sfw/lib"

./configure --prefix=%{_prefix}               \
            --bindir=%{_bindir}               \
            --sbindir=%{_sbindir}             \
            --mandir=%{_mandir}               \
            --libdir=%{_libdir}               \
            --datadir=%{_datadir}             \
            --libexecdir=%{_libexecdir}       \
            --sysconfdir=%{_sysconfdir}       \
            --localstatedir=%{_localstatedir} \
            --with-openssl-includes=/usr/sfw/include \
            --with-openssl-libraries=/usr/sfw/lib


make -j$CPUS

%install
rm -rf "$RPM_BUILD_ROOT"
R="$RPM_BUILD_ROOT" make install DESTDIR="$RPM_BUILD_ROOT"
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/freeradius
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*
%dir %attr (0755, root, sys) %{_localstatedir}/run
%dir %attr (0755, root, root) %{_localstatedir}/run/radiusd
%dir %attr (0755, root, sys) %{_localstatedir}/log
%attr (0755, root, sys) %{_localstatedir}/log/radius


%changelog
* Tue Jun 01 2010 - Milan Jurik
- SFEgdbm replaced by SUNWgnu-dbm
* Sun 19 Aug 2007 - trisk@acm.jhu.edu
- Initial version
