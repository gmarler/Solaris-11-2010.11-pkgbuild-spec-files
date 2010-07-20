#
# spec file for package SFEMpc
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include usr-gnu.inc

%define cc_is_gcc 1

%define pkg_src_name     mpc
%define src_name         mpc
%define src_ver          0.8.2

##TODO## think on usr-gnu.inc define infodir inside /usr/gnu/share to avoid conflicts
%define _infodir           %{_datadir}/info

%ifarch amd64 sparcv9
%include arch64.inc
%define is64 1
%use Mpc_64 = Mpc.spec
%endif

%include base.inc
%define is64 0
%use Mpc = Mpc.spec

Name:                    SFEMpc
Summary:                 mpc - C library for the arithmetic of complex numbers
Version:                 %{src_ver}
Release:                 1
License:                 LGPL
Group:                   Development/Languages/Mpc
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
Source:                  http://www.multiprecision.org/mpc/download/%{pkg_src_name}-%{version}.tar.gz
Url:	    	         http://www.multiprecision.org/
SUNW_BaseDir:            %{_basedir}/%{_subdir}
BuildRoot:               %{_tmppath}/%{src_name}_%{src_ver}

%include default-depend.inc

Requires: 	SFEgcc

BuildRequires:  SFEgmp-devel
Requires:       SFEgmp

Requires:       SFEmpfr-devel
BuildRequires:  SFEmpfr

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}/%{_subdir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %{name}-%{version}
mkdir %{name}-%{version}
%ifarch amd64 sparcv9
mkdir %{name}-%{version}/%{_arch64}
%define is64 1
%Mpc_64.prep -d %{name}-%{version}/%{_arch64}
%endif

mkdir %{name}-%{version}/%{base_arch}
%define is64 0
%Mpc.prep -d %{name}-%{version}/%{base_arch}


%build
%ifarch amd64 sparcv9
%define is64 1
%Mpc_64.build -d %{name}-%{version}/%{_arch64}
%endif

%define is64 0
%Mpc.build -d %{name}-%{version}/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%define is64 1
%Mpc_64.install -d %{name}-%{version}/%{_arch64}
%endif

%define is64 0
%Mpc.install -d %{name}-%{version}/%{base_arch}

%clean
%ifarch amd64 sparcv9
%define is64 1
%Mpc_64.clean -d %{name}-%{version}/%{_arch64}
%endif

%define is64 0
%Mpc.clean -d %{name}-%{version}/%{base_arch}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_infodir}
%{_infodir}/*

%changelog
* Mon July 19 2010 - markwright@internode.on.net
- Initial spec
