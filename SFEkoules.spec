#
# spec file for package SFEkoules.spec
#
%include Solaris.inc

%define src_version 1.4

Name:                    	SFEkoules
Summary:                 	Battle for Earth - koules
Version:                 	%{src_version}
License:			GPLv2
URL:				http://www.ucw.cz/~hubicka/koules/
Source:                  	http://www.ucw.cz/~hubicka/koules/packages/koules%{src_version}-src.tar.gz
Patch1:				koules-01-Iconfig.diff
Patch2:				koules-02-sock.diff
Patch3:				koules-03-koulestcl.diff
Patch4:				koules-04-deb.diff

BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
SUNW_BaseDir:     /

%prep
%setup -q -n koules%{src_version}
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
# new xmkmf stuff does strange things with the manpage
# this is a workaround from Debian
if [ ! -s xkoules.man ]; then ln -sf xkoules.6 xkoules.man; fi

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

PATH=$PATH:/usr/X11/bin xmkmf -a
make

%install
rm -Rf $RPM_BUILD_ROOT/*

PATH=$PATH:/usr/X11/bin make install KOULESDIR=$RPM_BUILD_ROOT/usr/bin SOUNDDIR=$RPM_BUILD_ROOT/usr/share/koules MANDIR=$RPM_BUILD_ROOT/usr/share/man/man6

%clean
rm -Rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/xkoules
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/koules
%{_datadir}/koules/*
%defattr (0755, root, bin)
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%changelog
* Sun Aug 16 2009 - Milan Jurik
- Initial version
