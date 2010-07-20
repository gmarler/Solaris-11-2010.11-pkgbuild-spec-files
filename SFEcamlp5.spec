#
# spec file for package SFEcamlp5 
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

%define src_name         camlp5
%define src_ver          5.14

Name:                    SFEcamlp5 
Summary:                 camlp5 - Camlp5 preprocessor
Version:                 %{src_ver}
Release:                 1
License:                 LGPL
Group:                   Development/Languages/Camlp5
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://cristal.inria.fr/~ddr/camlp5/
Source:                  http://cristal.inria.fr/~ddr/camlp5/distrib/src/%{src_name}-%{src_ver}.tgz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{src_name}_%{src_ver}

%description
Camlp5 is a preprocessor-pretty-printer of OCaml.
It is compatible with OCaml versions from 3.08.0 to 3.12.0 included.

%include default-depend.inc

Requires: 	SFEocaml
Requires: 	SFEgcc

%prep
%setup -q -n %{src_name}-%{version}
export CC=gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

bash ./configure             \
    -prefix %{_prefix}       \
    -bindir %{_bindir}       \
    -libdir %{_libdir}/ocaml \
    -mandir %{_mandir}       \
    -transitional

%build
export CC=gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
make world.opt

%install
export CC=gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
make install DESTDIR=$RPM_BUILD_ROOT

# Prepare lists of files for packaging
touch SFEcamlp5-all.files

find $RPM_BUILD_ROOT%{_prefix} \( -type f -o -type l \) -name "*" > SFEcamlp5-all.files
sort SFEcamlp5-all.files > SFEcamlp5-all-sort.files
# Clean up syntax for %files section
sed -i -e 's:'"$RPM_BUILD_ROOT"'::' SFEcamlp5-all-sort.files

%clean
rm -rf $RPM_BUILD_ROOT

%files -f SFEcamlp5-all-sort.files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, sys) %{_datadir}

%changelog
* Tue Jun 8 2010 - markwright@internode.on.net
- Initial spec
