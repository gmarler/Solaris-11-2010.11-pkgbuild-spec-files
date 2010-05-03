#
# spec file for package SFESimGear.spec
# Gilles Dauphin
#
# includes module(s): SimGear
#
%include Solaris.inc

%define src_name	SimGear
%define src_url		ftp://ftp.de.simgear.org/pub/simgear/Source
#ftp://ftp.de.simgear.org/pub/simgear/Source/SimGear-1.0.0.tar.gz
#ftp://ftp.simgear.org/pub/simgear/Source/SimGear-1.0.0.tar.gz

Name:                   SFESimGear
Summary:                Simulator Construction Tools
Version:                2.0.0
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Source1:		SimGear_Props.cxx
Patch1:			SimGear-01.diff
Patch2:			SimGear-02.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:		SFEopenal-devel
Requires:		SFEopenal
BuildRequires:		SFEfreealut-devel
Requires:		SFEfreealut
Requires:		SFEplib

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
#%setup -q -n -c %{src_name}-%{version}
%setup -q -c -n  %{name}
%patch1 -p0
%patch2 -p0
# It does not compile if filename is props.cxx
# Maybe a bug in Studio12 or maybe, maybe, in openat(2)/readdir(3C)
# TODO: find the bug or what I don't understand...
rm %{src_name}-%{version}/simgear/props/props.cxx
cp %{SOURCE1} %{src_name}-%{version}/simgear/props/Props.cxx

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd %{src_name}-%{version}
export CC=cc
export CXX=CC
export CFLAGS="-I%_prefix/X11/include"
export CXXFLAGS="-I%_prefix/X11/include"
#CC=cc CXX=CC ./configure --without-logging --prefix==%{_prefix}
/bin/bash ./configure CONFIG_SHELL=/bin/bash --prefix=%{_prefix}
make # -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd %{src_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
# TODO: make shared libs
#rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
#%{_bindir}
%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/lib*.a*

%files devel
%defattr (-, root, bin)
%{_includedir}
#%dir %attr(0755,root,bin) %{_libdir}
#%dir %attr(0755,root,other) %{_libdir}/pkgconfig
#%{_libdir}/pkgconfig/*

%changelog
* Mar 2010 - Gilles dauphin
- search includedir event if it is in /usr/SFE (exemple)
* Mon Nov 17 2008 - dauphin@enst.fr
- Initial version
