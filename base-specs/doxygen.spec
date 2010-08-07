#
# spec file for package doxygen
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:           doxygen
License:        GPL
Version:        1.7.1
URL:            http://www.doxygen.org/
Summary:        Doxygen is a documentation system for various programming languages
Source:         %{sf_download}/doxygen/doxygen-%{version}.src.tar.gz
Patch1:         doxygen-01-solaris-pkgtool.diff
%ifarch sparc
Patch2:		doxygen-02-solaris-tmake-sparc.diff
%else
Patch2:		doxygen-02-solaris-tmake-i386.diff
%endif
Patch3:         doxygen-03-tmake-g++.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_defaultdocdir}/doc

%package devel
Summary:	Header files, libraries and development documentation for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib"

%if %cc_is_gcc
%define platform solaris-g++
%else
%define platform solaris-cc
export CXX="$CXX -norunpath"
%endif

./configure --prefix %{_prefix}		\
	    --platform %platform	\
	    --docdir %{_datadir}/doc	\
	    --release			\
	    --shared

make CC="$CC" CXX="$CXX"

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sat Aug 07 2010 - brian.cameron@oracle.com
- Bump to 1.7.1.
* Sat Aug 16 2008 - nonsea@users.sourceforge.net
- Bump to 1.5.6.
- Use a live Source URL.
- Add solaris-pkgtool.diff.
- Add solaris-tmake-sparc.diff and solaris-tmake-i386.diff.
- Remove solaris-sparc.diff and solaris-i386.diff and reorder.
* Sun Feb 17 2008 - laca@sun.com
- build using the C/C++ compiler specified by the CC/CXX env variables.
* Fri Jan 18 2008 - moinak.ghosh@sun.com
- Bump version to 1.5.4.
- Change build configuration to solaris-g++ since SUN Studio compiled doxygen.
- dumps core while building documentation for SFEcppunit.
- Add patch for solaris-g++ config to include /usr/gnu/lib.
- Update nameconflict patch to remove additional conflicts.
* Mon Jul 30 2007 - markwright@internode.on.net
- bump to 1.5.3, remove patch1 as already applied, bump patch3.
* Sat Apr 21 2007 - dougs@truemail.co.th
- Initial version.
