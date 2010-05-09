#
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# spec file for package SFElibmikmod
#
%include Solaris.inc

%define oss      %(/usr/bin/pkginfo -q oss && echo 1 || echo 0)

Name:                    SFEmikmod
Summary:                 Mikmod  - A module player using the sound library libmikmod
Version:                 3.2.2
%define tarball_version 3.2.2-beta1
Source:                  http://mikmod.raphnet.net/files/mikmod-%{tarball_version}.tar.gz
URL:                     http://mikmod.raphnet.net/
License:                 GPLv2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms
%if %oss
BuildRequires: oss
%else
BuildRequires: SUNWaudh
%endif
Requires: SFElibmikmod
BuildRequires: SFElibmikmod-devel

%prep
%setup -q -n mikmod-%tarball_version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CPPFLAGS="-I%{_includedir}"
export CFLAGS="%optflags"
export LDFLAGS="-L%{_libdir} -R%{_libdir} -lm"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_basedir}/info
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}/mikmod
%{_datadir}/mikmod/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Sun May 09 2010 - Milan Jurik
- dependency cleanup
* Thu May 29 2008 - river@wikimedia.org
- don't assume basedir is /usr
* Wed Feb 06 2008 - moinak.ghosh@sun.com
- Initial spec.
