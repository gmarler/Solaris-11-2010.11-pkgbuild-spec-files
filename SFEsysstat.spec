# spec file for package SFEsysstat
#
# includes module(s): sysstat
#
%include Solaris.inc

Name:                SFEsysstat
Summary:             Most important perf metrics at a single glance
Version:             20090805
Source:              http://www.maier-komor.de/sysstat/sysstat-%{version}.tgz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWcsl
Requires: SUNWcsl

%prep
%setup -q -n sysstat-%{version}

%build


CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# Make configure find ncurses in /usr/gnu...
# perl -i.orig -lpe 'print "DIRS=/usr/gnu\n" if $. == 4' configure

./configure --prefix=/usr
make -j$CPUS

%install

rm -rf $RPM_BUILD_ROOT

install -D sysstat $RPM_BUILD_ROOT%{_bindir}/sysstat
install -D sysstat.1m $RPM_BUILD_ROOT%{_mandir}/man1m/sysstat.1m
mkdir $RPM_BUILD_ROOT/%{_sbindir}
ln $RPM_BUILD_ROOT/%{_bindir}/sysstat $RPM_BUILD_ROOT%{_sbindir}/sysstatd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/sysstat
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/sysstatd
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1m
%{_mandir}/man1m/sysstat.1m

%changelog

* Mon Aug 10 2009 - matt@greenviolet.net
- Bump version to 20090805
- Change dependency from ncurses to curses.
* Wed Apr 07 2007 - Eric Boutilier
- Initial spec
