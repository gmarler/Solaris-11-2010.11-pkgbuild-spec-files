#
# OpenSolaris has excellent support for modern, open print standards and
# related FOSS software, so I can't think of any reason -- except maybe
# compatibility with other UNIX/Linux systems -- why anybody would want
# to install apsfilter on an OpenSolaris system. But it was easy to include 
# here, so I did. If you do install apsfilter via this spec file and the Sun 
# SVR4 package it generates, it is not ready to go yet. Read the INSTALL file 
# and related docs (SETUP, README, FAQ, etc.) to learn how to finish the
# installation and setup.
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEapsfilter
Summary:             Flexible magic filter for printing under Unix environment
Version:             7.2.8
Source:              http://www.apsfilter.org/download/apsfilter-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:       SUNWsndm
Requires:            SUNWsndm

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n apsfilter

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
            --sysconfdir=%{_sysconfdir}

# Nothing to make, all the executables are sh/bash/perl scripts.
#make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT%{_sysconfdir}/apsfilter
rm -f basedir
ln -s ../..%{_datadir}/apsfilter basedir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/apsfilter
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man?
%{_mandir}/man?/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%changelog
* Sun May 09 2010 - Milan Jurik
- added missing build dependency
* Fri Oct 13 2006 - laca@sun.com
- fix datadir attributes
* Wed Oct 11 2006 - laca@sun.com
- make the /etc/apsfilter/basedir symlink relative
* Sat Sep 30 2006 - Eric Boutilier
- Initial spec
