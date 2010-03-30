%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use gtkimageview64 = gtkimageview.spec
%endif

%include base.inc
%use gtkimageview = gtkimageview.spec

Name:           SFEgtkimageview
Summary:        Image metadata library
Version:        %{default_pkg_version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:	SUNWgnome-common-devel

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%{_arch64}
%gtkimageview64.prep -d %name-%version/%{_arch64}
%endif

mkdir %name-%version/%{base_arch}
%gtkimageview.prep -d %name-%version/%{base_arch}


%build
%ifarch amd64 sparcv9
export PKG_CONFIG_PATH=%{_libdir}/%{_arch64}/pkgconfig
export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags"
%gtkimageview64.build -d %name-%version/%{_arch64}
%endif

export PKG_CONFIG_PATH=%{_libdir}/pkgconfig
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
%gtkimageview.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%gtkimageview64.install -d %name-%version/%{_arch64}
%endif

%gtkimageview.install -d %name-%version/%{base_arch}

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgtkimageview.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/gtkimageview.pc
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %dir %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/libgtkimageview.so*
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/gtkimageview.pc
%endif
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/gtkimageview/*.h
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc


%changelog
* Tue Mar 30 2010 - Milan Jurik
- add missing build dependency
* Fri Jan 22 2010 - jedy.wang@sun.com
- Add 64-bit support.
* Mon Dec 14 2009 - jedy.wang@sun.com
- Regenerate cofngiure before building.
* Sun Oct 11 2009 - Milan Jurik
- Initial spec
