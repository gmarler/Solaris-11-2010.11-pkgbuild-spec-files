#
# spec file for package SFElibmatroska
#
# includes module(s): libmatroska
#
%include Solaris.inc

Name:		SFElibmatroska
License:	LGPL
Summary:        Matroska Video Container
Group:          System Environment/Libraries
URL:            http://www.matroska.org/
Vendor:         Moritz Bunkus <moritz@bunkus.org>
Version:	0.8.1
Source:		http://dl.matroska.org/downloads/libmatroska/libmatroska-%{version}.tar.bz2
Patch1:		libmatroska-01-makefile.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFElibebml-devel
Requires: SFElibebml

%description
Matroska aims to become THE Standard of Multimedia Container Formats.
It was derived from a project called MCF, but differentiates from it
significantly because it is based on  EBML (Extensible Binary Meta
Language), a binary derivative of XML. EBML enables the Matroska
Development Team to gain significant advantages in terms of future
format extensibility, without breaking file support in old parsers.

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libmatroska-%version
cd make
mkdir solaris
cp linux/Makefile solaris
%patch1 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -I%{_includedir}"
export CXXFLAGS="%optflags -I%{_includedir}"
export ACLOCAL_FLAGS="-I/usr/share/aclocal -I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"
export LDFLAGS="-R%{_libdir} -L%{_libdir}"

cd make/solaris
make -j$CPUS PREFIX=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
cd make/solaris
make install_headers DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix}
make install_sharedlib DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mar 2010  - Gilles Dauphin
- look at install dir. Exemple search for /usr/SFE/include
- idem for _libdir
* Fri Jul 13 2007 - dougs@truemail.co.th
- Initial version
