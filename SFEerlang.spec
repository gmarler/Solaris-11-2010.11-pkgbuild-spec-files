#
# spec file for package SFEerlang 
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define cc_is_gcc 1

%ifarch amd64 sparcv9
%include arch64.inc
%define is64 1
%use erlang_64 = erlang.spec
%endif

%include base.inc
%define is64 0
%use erlang = erlang.spec

%define pkg_src_name     otp_src
%define src_name         erlang
%define src_ver          R13B04

Name:                    SFEerlang 
Summary:                 erlang - Erlang programming language and OTP libraries (g++-built)
Version:                 %{src_ver}
Release:                 1
License:                 ERLANG PUBLIC LICENSE
Group:                   Development/Languages/Erlang
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://www.erlang.org
Source:                  http://erlang.org/download/%{pkg_src_name}_%{src_ver}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{src_name}_%{src_ver}

%define SFEgd            %(/usr/bin/pkginfo -q SUNWgd && echo 0 || echo 1)
%define SFEunixodbc      %(/usr/bin/pkginfo -q SUNWunixodbc && echo 0 || echo 1)

%include default-depend.inc

%define src2_name crypto_lib_makefile.patch
%define src3_name erts_configure.patch
%define src4_name inet_drv.c.patch
%define src5_name libs_makefile.patch64
%define src6_name orber_lib_makefile.patch
%define src7_name ssl_examples_makefile.patch

Source2:                 http://src.opensolaris.org/source/raw/sfw/usr/src/cmd/erlang/Patches/%{src2_name}
Source3:                 http://src.opensolaris.org/source/raw/sfw/usr/src/cmd/erlang/Patches/%{src3_name}
Source4:                 http://src.opensolaris.org/source/raw/sfw/usr/src/cmd/erlang/Patches/%{src4_name}
Source5:                 http://src.opensolaris.org/source/raw/sfw/usr/src/cmd/erlang/Patches/%{src5_name}
Source6:                 http://src.opensolaris.org/source/raw/sfw/usr/src/cmd/erlang/Patches/%{src6_name}
Source7:                 http://src.opensolaris.org/source/raw/sfw/usr/src/cmd/erlang/Patches/%{src7_name}

Requires: 	SFEgcc

Requires:       SFEwxwidgets-gnu
BuildRequires:  SFEwxwidgets-gnu-devel

%if %SFEgd
BuildRequires: SFEgd-devel
Requires: SFEgd
%else
BuildRequires: SUNWgd2
Requires: SUNWgd2
%endif

%if %SFEunixodbc
BuildRequires: SFEunixodbc-devel
Requires: SFEunixodbc
%else
BuildRequires: SUNWunixodbc
Requires: SUNWunixodbc
%endif

BuildRequires: SUNWgtar
BuildRequires: SUNWesu

%prep
rm -rf %{name}-%{version}
mkdir %{name}-%{version}
%ifarch amd64 sparcv9
mkdir %{name}-%{version}/%{_arch64}
%define is64 1
%erlang_64.prep -d %{name}-%{version}/%{_arch64}
%endif

mkdir %{name}-%{version}/%{base_arch}
%define is64 0
%erlang.prep -d %{name}-%{version}/%{base_arch}


%build
%ifarch amd64 sparcv9
%define is64 1
%erlang_64.build -d %{name}-%{version}/%{_arch64}
%endif

%define is64 0
%erlang.build -d %{name}-%{version}/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%define is64 1
%erlang_64.install -d %{name}-%{version}/%{_arch64}
%endif

%define is64 0
%erlang.install -d %{name}-%{version}/%{base_arch}


# Prepare lists of files for packaging
cd %{_builddir}/%{name}-%{version}
touch SFEerlang-all.files

find $RPM_BUILD_ROOT%{_prefix} \( -type f -o -type l \) -name "*" > SFEerlang-all.files
sort SFEerlang-all.files > SFEerlang-all-sort.files
# Clean up syntax for %files section
sed -i -e 's:'"$RPM_BUILD_ROOT"'::' SFEerlang-all-sort.files

%clean
%ifarch amd64 sparcv9
%define is64 1
%erlang_64.clean -d %{name}-%{version}/%{_arch64}
%endif

%define is64 0
%erlang.clean -d %{name}-%{version}/%{base_arch}

%files -f SFEerlang-all-sort.files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, bin) %{_libdir}

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%endif

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/erlang/erts-5.7.5/man
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/erlang/erts-5.7.5/doc
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/erlang/lib/kernel-2.13.5/examples/uds_dist/ebin
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/erlang/lib/kernel-2.13.5/examples/uds_dist/priv
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/erlang/lib/erl_interface-3.6.5/src/auxdir
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/erlang/lib/inets-5.3/examples/server_root/htdocs/secret/top_secret
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/erlang/lib/inets-5.3/examples/server_root/htdocs/mnesia_secret/top_secret
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/erlang/lib/inets-5.3/examples/server_root/logs
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/erlang/lib/mnesia-4.4.13/include
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/erlang/lib/ssl-3.10.8/examples/certs/etc/otpCA/certs
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/erlang/lib/ssl-3.10.8/examples/certs/etc/otpCA/crl
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/erlang/lib/ssl-3.10.8/examples/certs/etc/erlangCA/crl
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/erlang/lib/ssl-3.10.8/examples/certs/etc/erlangCA/certs
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/erlang/lib/common_test-1.4.7/priv/bin
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/erlang/lib/percept-0.8.4/priv/logs
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/erlang/lib/odbc-2.10.7/priv/obj
%endif

%dir %attr (0755, root, bin) %{_libdir}/erlang/erts-5.7.5/man
%dir %attr (0755, root, bin) %{_libdir}/erlang/erts-5.7.5/doc
%dir %attr (0755, root, bin) %{_libdir}/erlang/lib/kernel-2.13.5/examples/uds_dist/priv
%dir %attr (0755, root, bin) %{_libdir}/erlang/lib/kernel-2.13.5/examples/uds_dist/ebin
%dir %attr (0755, root, bin) %{_libdir}/erlang/lib/erl_interface-3.6.5/src/auxdir
%dir %attr (0755, root, bin) %{_libdir}/erlang/lib/inets-5.3/examples/server_root/htdocs/secret/top_secret
%dir %attr (0755, root, bin) %{_libdir}/erlang/lib/inets-5.3/examples/server_root/htdocs/mnesia_secret/top_secret
%dir %attr (0755, root, bin) %{_libdir}/erlang/lib/inets-5.3/examples/server_root/logs
%dir %attr (0755, root, bin) %{_libdir}/erlang/lib/mnesia-4.4.13/include
%dir %attr (0755, root, bin) %{_libdir}/erlang/lib/ssl-3.10.8/examples/certs/etc/erlangCA/crl
%dir %attr (0755, root, bin) %{_libdir}/erlang/lib/ssl-3.10.8/examples/certs/etc/erlangCA/certs
%dir %attr (0755, root, bin) %{_libdir}/erlang/lib/ssl-3.10.8/examples/certs/etc/otpCA/crl
%dir %attr (0755, root, bin) %{_libdir}/erlang/lib/ssl-3.10.8/examples/certs/etc/otpCA/certs
%dir %attr (0755, root, bin) %{_libdir}/erlang/lib/common_test-1.4.7/priv/bin
%dir %attr (0755, root, bin) %{_libdir}/erlang/lib/percept-0.8.4/priv/logs
%dir %attr (0755, root, bin) %{_libdir}/erlang/lib/odbc-2.10.7/priv/obj

%changelog
* Sun Jun 6 2010 - markwright@internode.on.net
- Initial spec
