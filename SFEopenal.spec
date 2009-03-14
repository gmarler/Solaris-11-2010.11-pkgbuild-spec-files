#
# spec file for package SFEopenal_new.spec
#
# includes module(s): openal
# to become a official release of SFEopenal until other package that depend
# of me must work or not needed. Gilles Dauphin
#
%include Solaris.inc

%define src_name	openal-soft
%define src_url		http://www.openal.org/openal_webstf/downloads
%define src_url		http://connect.creativelabs.com/openal/Downloads
#http://connect.creativelabs.com/openal/Downloads/openal-soft-1.5.304.tar.bz2

%define SUNWcmake      %(/usr/bin/pkginfo -q SUNWcmake && echo 1 || echo 0)

Name:                   SFEopenal
Summary:                OpenAL is a cross-platform 3D audio API
Version:                1.5.304
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:			openal-new-01.diff
SUNW_BaseDir:           %{_basedir}
# GPL now
#SUNW_Copyright:		openal_license.txt
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %SUNWcmake
BuildRequires: SUNWcmake
%else
BuildRequires: SFEcmake
%endif

#%ifarch i386
#BuildRequires: SFEnasm
#%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -c -n %{name}
%patch1 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd %{src_name}-%{version}
CC=cc
export CC
mkdir build && cd build
cmake -DHAVE_GCC_VISIBILITY:INTERNAL=0 -DCMAKE_INSTALL_PREFIX:PATH=/usr -DHAVE_VISIBILITY_SWITCH:INTERNAL=0 ..
make

%install
rm -rf $RPM_BUILD_ROOT
cd %{src_name}-%{version}
cd build
#make install DESTDIR=$RPM_BUILD_ROOT
make install
mkdir $RPM_BUILD_ROOT
mv ./sfw_stage $RPM_BUILD_ROOT/%{_prefix}
#rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr(0755,root,bin) %{_libdir}
%dir %attr(0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Feb  8 2009 - Thomas Wagner
- quick fix for complaining make install about already defined "relative" installtarget (./sfw_stage)
* Mon Dec 22 2008 - Thomas Wagner
- make conditional BuildRequirement SUNWcmake / SFEcmake
* Sat Nov 15 2008 - dauphin@enst.fr
- change to new release of openal 1.5.304.
* Tue Jun  5 2007 - dougs@truemail.co.th
- Added patch for Sun Studio 12 builds - openal-03-packed.diff
* Tue May  1 2007 - dougs@truemail.co.th
- Initial version
