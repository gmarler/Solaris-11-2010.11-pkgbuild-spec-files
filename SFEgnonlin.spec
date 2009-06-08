#
# spec file for package SFEgnonlin
#
# includes module(s): gnonlin
#

%define         majmin          0.10

%include Solaris.inc
Name:                    SFEgnonlin
Summary:                 Non-linear editing elements for gstreamer
URL:                     http://gstreamer.freedesktop.org/src/gnonlin/
Version:                 0.10.11
Source:                  http://gstreamer.freedesktop.org/src/gnonlin/gnonlin-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SUNWglib2
Requires:                SUNWgnome-media
BuildRequires:           SUNWglib2-devel
BuildRequires:           SUNWgnome-media-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
%setup -q -n gnonlin-%version

%build
./configure --prefix=%{_prefix} --enable-gtk-doc
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majmin}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majmin}/*.a

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/gstreamer-%{majmin}
%{_libdir}/gstreamer-%{majmin}/libgnl.so

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%changelog
* Mon Jun 08 2009 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.10.11.
* Tue May 12 2009 - Brian Cameron  <brian.cameron@sun.com>
- Now install gtk-docs.
* Sun Mar 01 2009 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.10.10.
* Wed Aug 15 2007 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.10.9.
* Mon Jul 09 2007 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.10.8.
* Fri Feb 09 2007 - irene.huang@sun.com
- Created.
