#
# spec file for package SFEmemphis
#
# includes module(s): memphis
#

%include Solaris.inc
Name:                    SFEmemphis
Summary:                 Map Rendering Application
URL:                     https://trac.openstreetmap.ch/trac/memphis/
Version:                 0.2.3
License:                 LGPL
Source:                  http://wenner.ch/files/public/mirror/memphis/memphis-%{version}.tar.gz
Patch1:                  memphis-01-configure.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWglib2
Requires:                SUNWcairo
BuildRequires:           SUNWglib2-devel
BuildRequires:           SUNWcairo-devel
BuildRequires:           SUNWgtk-doc
BuildRequires:           SUNWvala-devel
Requires:                SUNWvala

%include default-depend.inc

%package devel
Summary:		 %{summary} - development files
SUNW_BaseDir:		 %{_basedir}
%include default-depend.inc
Requires: SFEhippo-canvas

%prep
%setup -q -n memphis-%version
%patch1 -p1

%build
./configure --prefix=%{_prefix} \
	--enable-vala		\
	--enable-gtk-doc	\
	--disable-static

make 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Clean up unpackaged files
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%if %{!?_without_gtk_doc:0}%{?_without_gtk_doc:1}
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc
%endif

rm $RPM_BUILD_ROOT%{_bindir}/example
rmdir $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/gir*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gir*
%{_datadir}/vala
%{_datadir}/gtk-doc
%{_datadir}/memphis

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%if %{!?_without_gtk_doc:1}%{?_without_gtk_doc:0}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%endif

%changelog
* Fri Jan 07 2011 - Milan Jurik
- bump to 0.2.3
* Wed Mar 10 2010 - brian.cameron@sun.com
- Created with version 0.1.0.
