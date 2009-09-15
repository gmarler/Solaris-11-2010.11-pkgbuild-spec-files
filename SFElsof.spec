#
# spec file for package SFElsof
#
# includes module(s): lsof
#
# Risk alert: This package's main exectuable, /usr/bin/lsof, is set 
# gid (2755), with group-owner sys so it can read /dev/kmem.
#

%include Solaris.inc

Name:                SFElsof
Summary:             List open files
Version:             4.83K
Source:              http://ftp.cerias.purdue.edu/pub/tools/unix/sysutils/lsof/NEW/lsof_%{version}.sun.tar.bz2

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n lsof_%version.sun

%build 

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

(echo y y y y y n y n y) | ./Configure solariscc

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
install -D lsof $RPM_BUILD_ROOT%{_bindir}/lsof
install -D lsof.8   $RPM_BUILD_ROOT%{_mandir}/man8/lsof.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%attr (2755, root, sys) %{_bindir}/lsof
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/lsof.8

%changelog
* Tue Sep 15 2009 - Olivier Mauras <oliver.mauras@gmail.com>
- Version bump to 4.83K
- Add automated default configuration
* Jul 27 2007 - Gilles Dauphin
- update http source path.
- TODO: does not compile on B117 because need additional source.
  (extdirent.h)
* Wed Apr 23 2008 - Thomas Wagner
- Bump to 4.79
* Mon Nov 5 2007 - markwright@internode.on.net
- Bump to 4.78.
* Sun Mar 18 2007 - Eric Boutilier
- Initial spec
