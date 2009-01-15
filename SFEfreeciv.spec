#
# spec file for package SFEfreeciv.spec
#
# includes module(s): freeciv
#
# bugdb: http://bugs.freeciv.org/Ticket/Display.html?id=
#
%include Solaris.inc

%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

Name:                    SFEfreeciv
Summary:                 freeciv - a multiplayer strategy game
URL:                     http://freeciv.wikia.com/
Version:                 2.1.8
Source:                  http://%{sf_mirror}/freeciv/freeciv-%{version}.tar.bz2
# date:2008-12-23 type:bug owner:halton bugid:40659
Patch1:                  freeciv-01-solaris-sh.diff
# date:2008-12-23 type:bug owner:halton bugid:40660
Patch2:                  freeciv-02-suncc-enum-array.diff
# date:2008-12-23 type:bug owner:halton bugid:40661
Patch3:                  freeciv-03-strlcpy.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%else
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%endif
Requires:       SFEsdl-mixer
Requires:       SFEggz-gtk
BuildRequires:  SFEsdl-mixer-devel
BuildRequires:  SFEggz-gtk-devel

%package root
Summary:       %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun-root

%prep
%setup -q -n freeciv-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%{optflags}"

libtoolize --force
aclocal $ACLOCAL_FLAGS -I . -I m4
autoheader
automake -a -c -f
autoconf

./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}		\
            --disable-nls			\
            --enable-shared			\
	    --disable-static

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/freeciv
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*.png
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*/apps
%{_datadir}/icons/hicolor/*/apps/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/ggz.modules

%changelog
* Thu Jan 15 2009 - halton.huo@sun.com
- Bump to 2.1.8
- Remove unused patch signedchar.diff
- Add pkg -root
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Enable building with either SUNWlibsdl or SFEsdl.
* Sun Apr 21 2006 - dougs@truemail.co.th
- Added SFEsdl-mixer and enabled sound
- A slight tidy up of spec file
* Sun Apr 21 2006 - dougs@truemail.co.th
- Bumped to 2.1.0-beta4
* Mon May  8 2006 - drdoug007@yahoo.com.au
- Initial version
