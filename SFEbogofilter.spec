#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEbogofilter
Summary:             A Bayesian spam filter.
Version:             1.1.5
Source:              http://%{sf_mirror}/sourceforge/bogofilter/bogofilter-%{version}.tar.bz2
URL:                 http://bogofilter.sourceforge.net/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEbdb
Requires: SFEbdb

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n bogofilter-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir}

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
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/bogofilter.cf.example

%changelog
* Thu Mar 29 2007 - daymobrew@users.sourceforge.net
- Bump to 1.1.5.

* Fri Jan 05 2007 - daymobrew@users.sourceforge.net
- Bump to 1.1.3.

* Wed Dec 13 2006 - Eric Boutilier
- Initial spec
