#
# spec file for package SFExine-ui
#
# includes module(s): xine-ui
#

%include Solaris.inc

Name:         SFExine-ui
License:      GPL
Group:        System/Libraries
Version:      0.99.5
Summary:      xine-ui - Xlib based skinned front end for the xine video player
Source:       %{sf_download}/xine/xine-ui-%{version}.tar.gz
#Patch1:       xine-ui-01-gettext.diff
#Patch2:       xine-ui-02-glib-gettext-Makefile.diff
#Patch3:       xine-ui-03-glibc-compat.diff
Patch4:       xine-ui-04-configure.diff
URL:          http://xinehq.de/index.php/home
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
SUNW_BaseDir: %{_basedir}
Autoreqprov:  on
BuildRequires: SFExine-lib-devel
Requires: SFExine-lib

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n xine-ui-%version
#%patch1 -p1 -b .patch01
#%patch3 -p1 -b .patch03
%patch4 -p1 -b .patch04

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

glib-gettextize --force
#( cd po; gpatch -p1 < %{P:2} )
#cp po/Makefile.in.in src/xitk/xine-toolkit/po
export CXX=/usr/sfw/bin/gcc
export CC=/usr/sfw/bin/gcc
#export LD=/usr/sfw/bin/ld
export LD=/usr/bin/ld
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS -I m4
autoheader
automake -a -c -f 
autoconf
export CFLAGS="-O4 -fPIC -DPIC -I/usr/X11/include -I/usr/openwin/include -D_LARGEFILE64_SOURCE -I/usr/gnu/include -mcpu=pentiumpro -mtune=pentiumpro -msse2 -mfpmath=sse "
export LDFLAGS="-L/usr/X11/lib -R/usr/X11/lib -L/usr/sfw/lib -R/usr/sfw/lib -R/usr/lib -L/usr/lib -lXext"
./configure --prefix=%{_prefix} \
	    --libdir=%{_libdir}

#echo '#define strsep xine_private_strsep'   >> config.h
echo '#define getline xine_private_getline' >> config.h
echo '#define strndup xine_private_strndup' >> config.h

make -j $CPUS NCURSES_LIB=-lcurses

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_mandir}/??
%endif

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/xine-ui
%{_datadir}/doc/xitk
# FIXME: move to %{_datadir}/applications?
%{_datadir}/xine/desktop/xine.desktop
%{_datadir}/xine/visuals
%{_datadir}/xine/skins
%{_datadir}/xine/oxine
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/*.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps
%{_datadir}/icons/hicolor/22x22/apps/*.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/*.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/*.png
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%attr (-, root, bin) %{_mandir}/??
%endif

%changelog
* Aug 2009 - Gilles Dauphin
- add -lXext. 
- strsep is in B117
* Mon Nov 5 2007 - markwright@internode.on.net
- Bump to 0.99.5. Change to use SFEgcc 4.2.2 as now used for SFExine-lib.
- Commented patch1, patch2 and patch3.  Add patch4 for INADDR_NONE.
* Sun Jan  7 2007 - laca@sun.com
- create
