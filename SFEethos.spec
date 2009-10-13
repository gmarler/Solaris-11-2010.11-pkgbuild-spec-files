#
# spec file for package SFEethos
#
# includes module(s): ethos
#

%define pythonver 2.6

%include Solaris.inc
Name:                    SFEethos
License:                 LGPL v2.1
Group:                   Libraries/Multimedia
Version:                 0.2.0
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
Summary:                 GNOME Plugin Framework
Source:                  http://ftp.dronelabs.com/sources/ethos/0.2/ethos-%{version}.tar.gz
Patch1:                  ethos-01-nomono.diff
Patch2:                  ethos-02-example.diff
Patch3:                  ethos-03-loader.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:            %{_basedir}

%include default-depend.inc
Requires:                SUNWglib2
Requires:                SUNWgtk2
Requires:                SUNWdbus-glib
Requires:                SUNWgnome-python26-libs
Requires:                SFEgjs
Requires:                SFEvala
BuildRequires:           SUNWglib2-devel
BuildRequires:           SUNWgtk2-devel
BuildRequires:           SUNWdbus-glib-devel
BuildRequires:           SUNWgnome-python26-libs-devel
BuildRequires:           SFEgjs-devel
BuildRequires:           SFEvala-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
%setup -q -n ethos-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
export PYTHON="/usr/bin/python%{pythonver}"
aclocal $ACLOCAL_FLAGS -I ./m4
autoconf
automake -a -c -f
./configure \
	--prefix=%{_prefix}         \
	--libdir=%{_libdir}	    \
	--mandir=%{_mandir}	    \
	--disable-mono              \
	--disable-glibtest
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.pyo" -exec rm -f {} ';'

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/ethos
%dir %attr (0755, root, bin) %{_libdir}/ethos/plugin-loaders
%dir %attr (0755, root, bin) %{_libdir}/ethos/plugin-loaders/lib*.so*
%{_libdir}/python%{pythonver}/vendor-packages/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/ethos
%{_datadir}/pygtk
%{_datadir}/vala

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%changelog
* Tue Oct 13 2009 - Brian Cameron  <brian.cameron@sun.com>
- Do not install .pyo files.
* Sun Oct 11 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created with version 0.2.0.
