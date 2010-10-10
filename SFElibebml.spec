#
# spec file for package SFElibebml
#
# includes module(s): libebml
#

# NOTE: This must be built using Solaris Studio 12.2, since the compiler
# option "=-library=stdcxx4" used by the spec is new to that release.

%include Solaris.inc

Name:		SFElibebml
License:	LGPL
Summary:	Extensible Binary Meta Language
Group:		System Environment/Libraries
URL:		http://ebml.sourceforge.net
Vendor:		Moritz Bunkus <moritz@bunkus.org>
Version:	1.0.0
Source:		http://dl.matroska.org/downloads/libebml/libebml-%{version}.tar.bz2
Patch1:		libebml-01-makefile.diff
Patch2:		libebml-02-headers.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: gnu-make
BuildRequires: gnu-coreutils
BuildRequires: text/locale

Requires:	stdcxx

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libebml-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS=-library=stdcxx4
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT=/usr/bin/msgfmt

cd make/linux
gmake -j$CPUS CXX=CC AR=CC  DEBUGFLAGS=-g WARNINGFLAGS="" \
ARFLAGS="-xar -o" LOFLAGS=-Kpic LIBSOFLAGS="-G -h "

%install
rm -rf $RPM_BUILD_ROOT
cd make/linux
gmake install prefix=$RPM_BUILD_ROOT%{_prefix} INSTALL=ginstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}/lib*.so*
%{_libdir}/lib*.a*

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Fri Oct  1 2010 - Alex Viskovatoff
- Update to 1.0.0; use stdcxx (requires Solaris Studio 12.2)
- Patch linux Makefile so that it works with Linux and Solaris
- instead of creating a new Makefile for Solaris.
* Fri Jul 13 2007 - dougs@truemail.co.th
- Initial version
