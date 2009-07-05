
# spec file for package SFEx264
#
# includes module(s): x264
#

%include Solaris.inc

%define         snap    20090704
%define         snaph   2245
%define src_name x264-snapshot
%define src_url	 http://download.videolan.org/pub/videolan/x264/snapshots/

Name:                    SFElibx264
Summary:                 H264 encoder library
Version:                 20090704
Source:                  %{src_url}/%{src_name}-%{snap}-%{snaph}.tar.bz2
URL:                     http://www.videolan.org/developers/x264.html
#Patch1:			 libx264-01-gccisms.diff
Patch2:                  libx264-02-version.diff
Patch3:                  libx264-03-ld.diff
Patch4:                  libx264-04-ginstall.diff
Patch5:                  libx264-05-ssse3.diff
Patch6:                  libx264-06-gpac.diff
Patch7:                  libx264-07-soname.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEgpac-devel
Requires: SFEgpac
BuildRequires: SFEyasm

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%{snap}-%{snaph}
#%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=/usr/sfw/bin/gcc
export CFLAGS="-D__C99FEATURES__"
export LDFLAGS="%_ldflags -lm"
bash ./configure	\
    --prefix=%{_prefix} \
    --enable-mp4-output	\
    --enable-pthread	\
    --enable-pic	\
    --enable-shared

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Mon Mar 16 2009 - andras.barna@gmail.com
- Add patch7
* Sun Mar 15 2009 - Milan Jurik
- the latest snapshot
* Mon Jun 30 2008 - andras.barna@gmail.com
- Force SFWgcc
* Fri May 23 2008 - michal.bielicki <at> voiceworks.pl
- h26x chokes on optflags, fix by Giles Dauphin
* tue Jan 08 2008 - moinak.ghosh@sun.com
- Build with gcc and enable C99FEATURES.
* Tue Nov 20 2007 - daymobrew@users.sourceforge.net
- Bump to 20071119 and add Url.
* Sun Aug 12 2007 - dougs@truemail.co.th
- Added SFEgpac as Required
* Fri Aug  3 2007 - dougs@truemail.co.th
- initial version
