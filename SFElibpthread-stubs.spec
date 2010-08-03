#
# spec file for package SFElibpthread-stubs
#
# includes module(s): libpthread-stubs
#
# bugdb: bugzilla.freedesktop.org
#

%include Solaris.inc
Name:                    SFElibpthread-stubs
Group:                   Libraries/Multimedia
Version:                 0.3
Source:                  http://xcb.freedesktop.org/dist/libpthread-stubs-%{version}.tar.gz
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
Summary:                 Map Viewer
URL:                     http://www.novopia.com/emerillon/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:            %{_basedir}

Requires: SFExcb-proto
BuildRequires: SFExcb-proto-devel

%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
%setup -q -n libpthread-stubs-%version

%build
#libtoolize --force
#aclocal $ACLOCAL_FLAGS
#autoheader
#automake -a -c -f
#autoconf
./configure \
   --prefix=%{_prefix} \
   --libexecdir=%{_libexecdir} \
   --sysconfdir=%{_sysconfdir}
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Thu Jul 29 2010 - Brian Cameron  <brian.cameron@oracle.com>
- Add new spec file.
