#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define tarball_version 1.02rc1

Name:                SFElzop
Summary:             File compressor -- similar to, but faster than gzip
Version:             1.2
Source:              http://www.lzop.org/download/lzop-%{tarball_version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFElzo

%prep
%setup -q -n lzop-%{tarball_version}

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi


export CFLAGS="%optflags -I%{_includedir}"
export LDFLAGS="%{_ldflags} -L%{_libdir} -R%{_libdir}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Mars 25 2010 - Gilles dauphin
- compat IPS versioning
* Wed Sep 27 2006 - Eric Boutilier
- Initial spec
