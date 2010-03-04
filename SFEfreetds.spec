#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEfreetds
Summary:             Implementation of the TDS (SQL Server/Sybase) protocol
Version:             0.82
Source:              http://ibiblio.org/pub/Linux/ALPHA/freetds/stable/freetds-%{version}.tar.gz
Patch:               freetds-01-shell.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: %name-root

Requires: SUNWopenssl-commands
BuildRequires: SUNWopenssl-commands
# The line above pretty much guarantees that the other SUNWopenssl*
# packages will be installed as well

Requires: SUNWgccruntime

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n freetds-%version
%patch -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=/usr/sfw/bin/gcc
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"
export LDFLAGS="%_ldflags"

./configure \
        --prefix=%{_prefix}         \
        --mandir=%{_mandir}         \
        --enable-static=no          \
        --sysconfdir=%{_sysconfdir} \
        --infodir=%{_datadir}/info  \
        --with-openssl="/usr/sfw"

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm ${RPM_BUILD_ROOT}%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*.5

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*.conf

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Wed Mar 03 2010 - matt@greenviolet.net
- Update man page packaging
- Fix configure to work with old Solaris /bin/sh
* Tue Oct 22 2008  - Pradhap Devarajan <pradhap (at) gmail.com>
- Bump to 0.82
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Mon Mar 13 2007 - Eric Boutilier
- Initial spec
