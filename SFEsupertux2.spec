#
# spec file for package SFEsupertux.spec
#
# includes module(s): supertux
#
%include Solaris.inc

%define src_name	supertux
%define src_url		http://download.berlios.de/supertux

Name:                   SFEsupertux
Summary:                Super Tux Game
Version:                0.3.3
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2
Patch2:			supertux-02-infinity.diff
URL:			http://supertux.lethargik.org/
Group:			Amusements/Games

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEphysfs-devel
Requires: SFEphysfs
BuildRequires: SFEsdl-image-devel
Requires: SFEsdl-image
BuildRequires: SFEopenal-devel
Requires: SFEopenal
BuildRequires: SFEjam
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
BuildRequires: SFElibglew-devel
Requires: SFElibglew

%prep
%setup -q -c -n %{name}-%{version}
%patch2 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd %{src_name}-%{version}

export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
unset CFLAGS
unset CXXFLAGS
unset LDFLAGS

mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} ..
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
cd %{src_name}-%{version}/build
make install
mkdir -p $RPM_BUILD_ROOT%{_prefix}
mv ./sfw_stage/* $RPM_BUILD_ROOT%{_prefix}
mv $RPM_BUILD_ROOT%{_prefix}/games/supertux2 $RPM_BUILD_ROOT%{_bindir}
rmdir $RPM_BUILD_ROOT%{_prefix}/games

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/games/supertux2
%dir %attr (0755,root,other) %{_datadir}/doc
%dir %attr (0755,root,other) %{_datadir}/applications
%dir %attr (0755,root,other) %{_datadir}/pixmaps
%{_datadir}/doc/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*

%changelog
* Sat May 15 2010 - Milan Jurik
- update to 0.3.3 and rename to supertux2 because it is unstable yet
* Thu Feb 14 2008 - moinak.ghosh@sun.com
- Fix some kinks with latest SuperTux version.
* Sun May  6 2007 - dougs@truemail.co.th
- Initial version
