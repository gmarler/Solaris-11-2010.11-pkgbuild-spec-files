#
# spec file for package SFElibnids.spec
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define src_name libnids

Summary:	NIDS E-component.
Name:		SFElibnids
Version:	1.23
License:	GPL
Group:		System Environment/Libraries
URL:		http://libnids.sourceforge.net
Source:		%{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%name-%version

Requires: SUNWlibpcap
BuildRequires: SUNWlibpcap
Requires: SUNWlibnet
BuildRequires: SUNWlibnet

%description
libnids is an implementation of an E-component of Network Intrusion
Detection System.  It emulates the IP stack of Linux 2.0.x.  libnids
offers IP defragmentation, TCP stream assembly, and TCP port scan
detection.

%package devel
Summary: Development libraries, header files, and documentation for libnids.
Group: Development/Libraries
Requires: %name

%description devel
This package contains development libraries and C header files needed for
building applications which use libnids, as well as documentation on libnids.

%prep
%setup -q -n %{src_name}-%{version}

%build
CC=gcc
./configure		\
    --prefix=%{_prefix}	\
    --bindir=%{_bindir}	\
    --libdir=%{_libdir}	\
    --mandir=%{_mandir}	\
    --enable-shared

make

%install
rm -rf $RPM_BUILD_ROOT
make install install_prefix=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libnids.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%_libdir/libnids.so
%_libdir/libnids.so.*

%files devel
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_includedir}
%_includedir/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%_mandir/man3/*

%changelog
* Sun Sep 13 2009 - Milan Jurik
- Initial version
