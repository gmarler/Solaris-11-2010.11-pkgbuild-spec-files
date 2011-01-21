#
# spec file for package SFEncmpcpp
#
# includes module: ncmpcpp
#

%include Solaris.inc
%define srcname ncmpcpp

Name:		SFEncmpcpp
Summary:	ncurses based mpd client
URL:		http://unkart.ovh.org/ncmpcpp
Vendor:		Andrzej Rybczak <electricityispower.gmail.com>
Version:	0.5.5
License:	GPLv2
Source:		http://unkart.ovh.org/%srcname/%{srcname}-%{version}.tar.bz2

%include default-depend.inc
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires:	SUNWgmake
BuildRequires:	SUNWgcc
BuildRequires:	SUNWncurses-devel
Requires:	SUNWncurses
BuildRequires:	SFElibmpdclient-devel
Requires:	SFElibmpdclient


%prep
%setup -q -n %srcname-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi
export CFLAGS="%gcc_optflags"

# configure doesn't find libpthread with Sun Studio 
export CC=gcc
export CXX=g++
export CXXFLAGS="%gcc_cxx_optflags -I/usr/include/ncurses -L/usr/gnu/lib -R/usr/gnu/lib"
export LIBS=-lsocket
export LDFLAGS="-L/usr/gnu/lib -R/usr/gnu/lib"
./configure --prefix=%_prefix


gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir/%srcname
%dir %attr (-, root, sys) %_datadir
%_mandir
%dir %attr (-, root, other) %_docdir
%_docdir/%srcname


%changelog
* Thu Oct 21 2010 - Alex Viskovatoff
- Initial spec
