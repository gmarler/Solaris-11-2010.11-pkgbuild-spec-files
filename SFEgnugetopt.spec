#
# spec file for package SFEgnugetopt
#
# includes module(s): getopt
#
# Owner: erwannc
#
 
%include Solaris.inc
%include usr-gnu.inc
 
Name:                   SFEgnugetopt
Summary:                getopt - a GNU getopt(3) compatible getopt utility
Version:                1.1.4
Group:			Utility
URL:                    http://software.frodo.looijaard.name/getopt/
Source:			http://software.frodo.looijaard.name/getopt/files/getopt-%{version}.tar.gz
Patch1:                 getopt-01-locale.h.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
rm -rf %name-%version
%setup -q -n getopt-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

make -j$CPUS CC="${CC}" CFLAGS="%optflags"

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix} mandir=%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%doc Changelog README
%doc(bzip2) COPYING
%dir %attr (0755, root, other) %{_docdir}

%changelog
* Sun Sep 19 2010 - Milan Jurik
- reintroducing as SFEgnugetopt
* Tue Oct 14 2008 - michal.bielicki@halokwadrat.de
- Recreated into SFE archive
* Wed Sep 17 2008 - matt.keenn@sun.com
- Update copyright
* Tue Feb 13 2007 - laca@sun.com
- create

