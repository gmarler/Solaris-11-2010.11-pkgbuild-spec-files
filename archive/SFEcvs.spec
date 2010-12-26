#
# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:			SFEcvs
Version:		1.12.13
Summary:		CVS - concurrent versions system
Source:			http://ftp.gnu.org/non-gnu/cvs/source/feature/%{version}/cvs-%{version}.tar.bz2
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires:               SUNWperl584core

%description
CVS: concurrent versions system.
Open Source de-facto standard version control system.

%prep
%setup -q -n cvs-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
CFLAGS="$RPM_OPT_FLAGS"			\
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir}
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_prefix}/info

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/*
%{_datadir}/cvs

%changelog
* Wed Nov 15 2006  <eric.boutilier@sun.com>
- Copied and transposed CBEcvs to SFEcvs
* Sat Aug 19 2006  <laca@sun.com>
- move to /opt/jdsbld by default
- update default attributes
* Wed Aug 16 2006  <laca@sun.com>
- add missing deps
- bump to 1.12.13
* Wed Oct 12 2005  <laca@sun.com>
- add datadir to %files as bin/rcs2log is a link to a file in share
* Fri Sep 02 2004  <laca@sun.com>
- remove unpackaged files
* Sun Sep 05 2004  <laca@sun.com>
- enable parallel build
* Fri Mar 05 2004  <laca@sun.com>
- fix %files
- change the pkg category
