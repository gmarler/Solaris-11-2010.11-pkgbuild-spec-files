#
# spec file for package SFElibpano13.spec
#
# includes module(s): libpano13
#
%include Solaris.inc

%define src_name libpano13

Name:		SFElibpano13
Summary:	Library for manipulating panoramic images
Version:	2.9.17
License:	GPLv2+
URL:		http://panotools.sourceforge.net/
Group:		Development/Libraries
Source:		%{sf_download}/panotools/%{src_name}-%{version}.tar.gz
Patch1:		libpano13-01-sunc.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWgawk

%description
Helmut Dersch's Panorama Tools library.  Provides very high quality
manipulation, correction and stitching of panoramic photographs.

Due to patent restrictions, this library has a maximum fisheye field-of-view
restriction of 179 degrees to prevent stitching of hemispherical photographs.

%package tools
Summary: Tools that use the libpano13 library
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}

%description tools
PTAInterpolate, interpolate between photos
PTcrop, create cropped TIFF files from uncropped TIFF
PTuncrop, create uncropped TIFF files from cropped TIFF
PTtiffdump
PTinfo
PToptimizer, a command-line interface for control-point optimisation
PTblender, match colour histograms of overlappng TIFF files
PTtiff2psd, convert TIFF files to PSD
panoinfo, a tool for querying pano13 library capabilities
PTmasker 
PTmender, remaps photos between projections
PTroller, merges multiple TIFF with alpha masks to a single TIFF

%package devel
Summary: Development tools for programs which will use the libpano13 library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The libpano13-devel package includes the header files necessary for developing
programs which will manipulate panoramas using the libpano13 library.

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags} -lm"
./configure --prefix=%{_prefix}	\
	--disable-static
make

%install
make install DESTDIR=%{buildroot}
rm %{buildroot}/%{_libdir}/libpano13.la
mkdir %{buildroot}/%{_datadir}
mv %{buildroot}/%{_prefix}/man %{buildroot}/%{_mandir}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%doc AUTHORS ChangeLog COPYING NEWS README README.linux
%{_libdir}/libpano13.so.2*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}

%files tools
%defattr(-, root, bin)
%doc doc/Optimize.txt doc/stitch.txt
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%dir %attr (0755, root, other) %{_docdir}

%files devel
%defattr(-, root, bin)
%doc COPYING
%{_includedir}/pano13
%{_libdir}/libpano13.so
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*


%changelog
* Sun Dec 19 2010 - Milan Jurik
- initial spec based on Fedora
