#
# spec file for package: Xaw3d
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# include module(s): Xaw3d
#

%include Solaris.inc
%define X11_DIR %{_prefix}/X11

%define src_name	Xaw3d

Name:           SFEXaw3d
Summary:        X Window toolkit with 3D appearance
Version:        1.5
Release:        E
License:        X11
Source:         ftp://ftp.visi.com/users/hawkeyd/X/%{src_name}-%{version}%{release}.tar.gz
URL:            http://freshmeat.net/projects/xaw3d/
Group:          System/Libraries
Distribution:	OpenSolaris
Vendor:		OpenSolaris Community
%include default-depend.inc

BuildRequires:  SUNWxwopt
BuildRequires:  SUNWxwinc
BuildRequires:  SUNWbtool
BuildRequires:  SUNWgnu-coreutils

BuildRoot:      %{_tmppath}/%{name}-%{version}%{release}-build
SUNW_Basedir:   %{_basedir}
SUNW_Copyright: %{src_name}.copyright


# OpenSolaris IPS Manifest Fields
Meta(info.upstream):            D.J. Hawkey Jr.<hawkeyd@visi.com>
Meta(info.repository_url):      ftp://ftp.visi.com/users/hawkeyd/X/Xaw3d-1.5E.tar.gz
Meta(info.maintainer):          Federico Beffa<beffa at ieee dot org>
Meta(info.detailed_url):        http://freshmeat.net/projects/xaw3d
Meta(info.classification):      org.opensolaris.category.2008:System/Libraries


Patch: %{src_name}-0-xorg-imake.diff

%description 
Xaw3d is a general-purpose replacement for the Athena toolkit which
adds a 3D appearance and support for XPM images.

%package devel
Summary: Header files and static libraries for development using Xaw3d
Group: Development/X11

%prep
rm -rf %{src_name}-%{version}%{release}
%setup -q -c -n %{src_name}-%{version}%{release}
pushd xc/lib/Xaw3d
ln -s .. X11
%patch -p0 -b .config
popd

%build
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
export PATH=${PATH}:/usr/X11/bin
pushd xc/lib/Xaw3d
xmkmf
make
popd

%install
rm -rf $RPM_BUILD_ROOT
#make install DESTDIR=$RPM_BUILD_ROOT SHLIBDIR=%{_libdir} INCDIR=%{_includedir} INSTALL=/opt/dtbld/bin/install -C xc/lib/Xaw3d
make install DESTDIR=$RPM_BUILD_ROOT SHLIBDIR=%{X11_DIR}/lib INCDIR=%{X11_DIR}/include INSTALL=/usr/bin/ginstall -C xc/lib/Xaw3d
pushd xc/lib/Xaw3d
mkdir -p $RPM_BUILD_ROOT/%{_pkg_docdir}-%{version}%{release}
install -c -m 0444 README.XAW3D $RPM_BUILD_ROOT/%{_pkg_docdir}-%{version}%{release}
popd

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%doc /%{_pkg_docdir}-%{version}%{release}/README.XAW3D
%{X11_DIR}/lib/*.so.*

%files devel
%defattr(-,root, bin)
%dir %attr (0755, root, bin) %{X11_DIR}/lib
%{X11_DIR}/lib/*.so
%dir %attr (0755, root, bin) %{X11_DIR}/include
%{X11_DIR}/include/X11/Xaw3d

%changelog
* May 2010  - Gilles DAuphin
- import in SFE
- Name is SFE
* Sat Aug 29 2009 - bld
- touch file to initiate build
* Sat Aug 29 2009 - beffa at ieee dot org
- moved into real X11 directory
* Sat Jul 25 2009 - beffa at ieee dot org
- initial version
## Re-build 24/09/09
