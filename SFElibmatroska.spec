#
# spec file for package SFElibmatroska
#
# includes module(s): libmatroska
#

# NOTE: This must be built using Solaris Studio 12.2, since the compiler
# option "=-library=stdcxx4" used by the spec is new to that release.

%include Solaris.inc
%define srcname libmatroska

Name:		SFElibmatroska
License:	LGPL
Summary:	Matroska Video Container
Group:		System Environment/Libraries
URL:		http://www.matroska.org
Vendor:		Moritz Bunkus <moritz@bunkus.org>
Version:	1.0.0
Source:		http://dl.matroska.org/downloads/%srcname/%{srcname}-%{version}.tar.bz2
Patch1:		libmatroska-01-makefile.diff

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgmake
BuildRequires: SFElibebml-devel
Requires: SFElibebml

%description
Matroska aims to become THE Standard of Multimedia Container Formats.
It was derived from a project called MCF, but differentiates from it
significantly because it is based on  EBML (Extensible Binary Meta
Language), a binary derivative of XML. EBML enables the Matroska
Development Team to gain significant advantages in terms of future
format extensibility, without breaking file support in old parsers.
These libraries are used by mkvtoolnix.

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libmatroska-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -I%{_includedir}"
export CXXFLAGS="-library=stdcxx4 %optflags -I%{_includedir}"
export ACLOCAL_FLAGS="-I/usr/share/aclocal -I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"
export LDFLAGS="-library=stdcxx4 -R%{_libdir} -L%{_libdir}"

cd make/linux
gmake -j$CPUS  CXX=CC AR=CC  DEBUGFLAGS=-g WARNINGFLAGS="" \
ARFLAGS="-xar -o" LOFLAGS=-Kpic LIBSOFLAGS="-G -h "

%install
rm -rf $RPM_BUILD_ROOT
cd make/linux
gmake install_headers prefix=$RPM_BUILD_ROOT%{_prefix} INSTALL=ginstall
gmake install_sharedlib prefix=$RPM_BUILD_ROOT%{_prefix} INSTALL=ginstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Fri Oct  1 2010 - Alex Viskovatoff
- Update to 1.0.0; use stdcxx (requires Solaris Studio 12.2)
- Patch linux Makefile so that it works with Linux and Solaris
  instead of creating a new Makefile for Solaris.
* Mar 2010  - Gilles Dauphin
- look at install dir. Exemple search for /usr/SFE/include
- idem for _libdir
* Fri Jul 13 2007 - dougs@truemail.co.th
- Initial version
