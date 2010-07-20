#
# spec file for package SFEhevea 
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

# SFEocaml, SFEcamlp5, SFEhevea compiles with Sun Studio 12u1 cc,
# and I guess SFElablgtk and SFEunison do as well.
# However SFEcoq wants SFEocaml to be compiled with gcc, to enable
# the THREADED_CODE define in /usr/lib/ocaml/caml/config.h
%define cc_is_gcc 1
%include base.inc

%define src_name         hevea
%define src_ver          1.10

Name:                    SFEhevea 
Summary:                 hevea - hevea is a quite complete and fast latex to html translator
Version:                 %{src_ver}
Release:                 1
License:                 Q PUBLIC LICENSE with special exception
Group:                   Development/Languages/Hevea
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://hevea.inria.fr/
Source:                  http://hevea.inria.fr/distri/%{src_name}-%{src_ver}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{src_name}_%{src_ver}

%description
hevea is a quite complete and fast latex to html translator

%include default-depend.inc

Requires: 	SFEocaml
Requires: 	SFEgcc

%prep
%setup -q -n %{src_name}-%{version}
sed -i -e "s,PREFIX=/usr/local,PREFIX=/usr," Makefile

%build
export CC=gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
make

%install
export CC=gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
sed -i -e "s,PREFIX=/usr,PREFIX=${RPM_BUILD_ROOT}/usr," Makefile
make install

# Prepare lists of files for packaging
touch SFEhevea-all.files

find ${RPM_BUILD_ROOT}%{_prefix} \( -type f -o -type l \) -name "*" > SFEhevea-all.files
sort SFEhevea-all.files > SFEhevea-all-sort.files
# Clean up syntax for %files section
sed -i -e 's:'"$RPM_BUILD_ROOT"'::' SFEhevea-all-sort.files

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f SFEhevea-all-sort.files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/hevea

%changelog
* Fri Jun 11 2010 - markwright@internode.on.net
- Initial spec
