#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEnrg2iso
Summary:             Convert Nero nrg files into ISO 9660 images
Version:             0.4
Source:              http://gregory.kokanosky.free.fr/v4/linux/nrg2iso-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n nrg2iso-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags} -R/usr/sfw/lib"
export CPPFLAGS="-I/usr/sfw/include"

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

/usr/ucb/install -d -m 0755 $RPM_BUILD_ROOT/%{_prefix}/bin
/usr/ucb/install -o root -g sys -m 0755 nrg2iso $RPM_BUILD_ROOT/%{_prefix}/bin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Tue Apr 30 2008 - river@wikimedia.org
- Initial spec
