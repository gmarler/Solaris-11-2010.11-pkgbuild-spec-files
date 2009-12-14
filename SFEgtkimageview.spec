%include Solaris.inc

%define src_name gtkimageview

Name:		SFEgtkimageview
Summary:	Image metadata library
Version:	1.6.4
URL:		http://trac.bjourne.webfactional.com/chrome/common/releases/
Source:		%{url}%{src_name}-%{version}.tar.gz
Patch1:		gtkimageview-01-cflags.diff 
Patch2:		gtkimageview-02-void.diff 
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"

export LDFLAGS="%_ldflags"

aclocal $ACLOCAL_FLAGS
glib-gettextize --force --copy
intltoolize --force --automake
gtkdocize

automake -a -f -c --gnu
autoconf
./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --mandir=%{_mandir}		\
            --enable-compile-warnings=no\
            --disable-static

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc/html
%attr(755, root, root) %{_datadir}/gtk-doc/html/gtkimageview/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*


%changelog
* Mon Dec 14 2009 - jedy.wang@sun.com
- Regenerate cofngiure before building.
* Sun Oct 11 2009 - Milan Jurik
- Initial spec
