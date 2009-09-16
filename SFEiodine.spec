#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEiodine
Summary:             iodine - IP over DNS is now easy
Version:             0.5.2
Source:              http://code.kryo.se/iodine/iodine-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWzlib
Requires: SFEtun

%prep
%setup -q -n iodine-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lsocket -lnsl -lz"

make -j$CPUS CC="$CC" CFLAGS="-c $CFLAGS" LDFLAGS="$LDFLAGS"

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
cp bin/iodine $RPM_BUILD_ROOT%{_sbindir}/iodine
cp bin/iodined $RPM_BUILD_ROOT%{_sbindir}/iodined
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
cp man/iodine.8 $RPM_BUILD_ROOT%{_mandir}/man8/iodine.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%changelog
* Tue Sep 15 2009 - trisk@acm.jhu.edu
- Bump to 0.5.2
* Fri May 23 2008 - trisk@acm.jhu.edu
- Bump to 0.4.1
* Wed Nov 28 2007 - trisk@acm.jhu.edu
- Initial spec
