#
# spec file for package SFESimGear.spec
# Gilles Dauphin
#
# includes module(s): SimGear
#
%include Solaris.inc

%define src_name	SimGear
%define src_url		ftp://ftp.de.simgear.org/pub/simgear/Source

Name:                   SFESimGear20
Summary:                Simulator Construction Tools
Version:                2.0.0
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
#Source1:		SimGear_Props.cxx
SUNW_BaseDir:           %{_basedir}
Group:			Applications/Games
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:		SFEopenal-devel
Requires:		SFEopenal
BuildRequires:		SFEfreealut-devel
Requires:		SFEfreealut
Requires:		SFEplib-gpp
Requires:		SFEosg

# that's a nightmare with g++
#I patch the following file in the system:
#/usr/gcc/4.3/include/c++/4.3.3/i386-pc-solaris2.11/bits/c++config.h
#/usr/gcc/4.3/include/c++/4.3.3/i386-pc-solaris2.11/amd64/bits/c++config.h
#with the ending: #undef _GLIBCXX_CONCEPT_CHECKS
# if youy want to compile do it
# don't forget to reverse.

# Requires:		SFEgcc43-patch-WARNING

%prep
%setup -q -c -n  %{name}
#%patch1 -p0
#%patch2 -p0
# It does not compile if filename is props.cxx
# Maybe a bug in Studio12 or maybe, maybe, in openat(2)/readdir(3C)
# TODO: find the bug or what I don't understand...
#rm %{src_name}-%{version}/simgear/props/props.cxx
#cp %{SOURCE1} %{src_name}-%{version}/simgear/props/Props.cxx

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd %{src_name}-%{version}
export CC=/usr/gcc/4.3/bin/gcc
export CXX=/usr/gcc/4.3/bin/g++
export CFLAGS="-I%{_prefix}/X11/include -I%{_includedir}"
export CXXFLAGS="-I%{_prefix}/X11/include -I%{_includedir}"
export LDFLAGS="-L%{_libdir} -R%{_libdir}"
#/bin/bash ./autogen.sh --prefix=%{_prefix}
/bin/bash ./configure CONFIG_SHELL=/bin/bash --prefix=%{_prefix} \
	--with-osg=%{_prefix} \
	--with-boost=%{_prefix} \
	--with-boost-libdir=%{_libdir}

make  -j$CPUS 

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
%{_includedir}
%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/lib*.a*

%changelog
* May 2010 - Gilles Dauphin
- Initial version for 2.0
