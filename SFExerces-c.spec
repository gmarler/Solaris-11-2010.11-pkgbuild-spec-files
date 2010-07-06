#
# spec file for package SFExerces-c
#
# includes module(s): Xerces-C++
#

%include Solaris.inc

Name:         SFExerces-c
License:      Other
Group:        System/Libraries
Version:      2.8.0
%define tarball_version 2_8_0
Summary:      Xerces-C++ - validating XML parser
Source:       http://www.apache.org/dist/xerces/c/2/sources/xerces-c-src_%{tarball_version}.tar.gz
URL:          http://xerces.apache.org/index.html
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
SUNW_Copyright: %{name}.copyright
SUNW_BaseDir: %{_basedir}
Autoreqprov:  on
%include default-depend.inc
BuildRequires: SUNWdoxygen
BuildRequires: SUNWgnu-findutils
BuildRequires: SUNWgnu-coreutils

%description
Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

The parser provides high performance, modularity, and scalability. Source
code, samples and API documentation are provided with the parser. For
portability, care has been taken to make minimal use of templates, no RTTI,
and minimal use of #ifdefs.

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%prep
%setup -q -n xerces-c-src_%{tarball_version}

%build
# don't try to parallel build this
CPUS=1

# 32-bit build
%define rcopts -b 32

%if %cc_is_gcc
%else
export LDFLAGS="-norunpath"
%endif

export XERCESCROOT=`pwd`
cd $XERCESCROOT/src/xercesc
./runConfigure %{rcopts} -c `basename ${CC}` -x `basename ${CXX}` -p solaris -C \
    --libdir="%{_libdir}" -minmem -nsocket -tnative -r pthread \
    -P%{_prefix}
make -j $CPUS DESTDIR=$RPM_BUILD_ROOT
cd $XERCESCROOT/samples
./runConfigure %{rcopts} -c ${CC} -x "${CXX}" -p solaris -r pthread
make -j $CPUS DESTDIR=$RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
export XERCESCROOT=`pwd`
cd $XERCESCROOT/src/xercesc
make DESTDIR=$RPM_BUILD_ROOT TARGET=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT%{_prefix}/bin
#we don't want obj directory
install `/usr/gnu/bin/find $XERCESCROOT/bin -maxdepth 1 -type f` \
    $RPM_BUILD_ROOT%{_prefix}/bin
mkdir -p $RPM_BUILD_ROOT%{_datadir}/xerces-c
/usr/gnu/bin/cp -a $XERCESCROOT/samples $RPM_BUILD_ROOT%{_datadir}/xerces-c

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755, root, bin)
%{_bindir}/*
%{_libdir}/libxerces-*.so.*
%{_libdir}/libxerces-*.so

%files devel
%defattr(-, root, bin)
%{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/xerces-c/samples

%changelog
* Tue Jul 06 2010 - Milan Jurik
- fix build
* Sun Feb 17 2008 - laca@sun.com
- create based on xerces-c.spec distributed with Xerces-C-2.8.0
