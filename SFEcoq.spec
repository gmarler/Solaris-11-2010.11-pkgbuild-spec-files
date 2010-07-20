#
# spec file for package SFEcoq 
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

%define src_name         coq
%define src_ver          8.2pl2

Name:                    SFEcoq 
Summary:                 coq - Coq proof assistant
Version:                 %{src_ver}
Release:                 1
License:                 LGPL
Group:                   Development/Languages/Coq
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://coq.inria.fr
Source:                  http://coq.inria.fr/distrib/V8.2pl2/files/%{src_name}-%{src_ver}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{src_name}_%{src_ver}

%description
Coq is a formal proof management system. It provides a formal language
to write mathematical definitions, executable algorithms and theorems
together with an environment for semi-interactive development of
machine-checked proofs.

%include default-depend.inc

Requires: 	SFEocaml
Requires: 	SFEhevea
Requires: 	SFEcamlp5
Requires: 	SFEgcc
BuildRequires: 	SFEnetpbm

if [ ! `which latex` ]
then
BuildRequires: 	SFEtexlive
fi

%prep
%setup -q -n %{src_name}-%{version}

sed -i -e 's,#!/bin/sh,#!/bin/bash,' configure doc/tools/latex_filter doc/tools/show_latex_messages \
    dev/ocamldebug-coq.template dev/tools/univdot dev/v8-syntax/check-grammar \
    doc/stdlib/make-library-files doc/stdlib/make-library-index install.sh \
    test-suite/check tools/beautify-archive tools/check-translate
sed -i -e 's,#! /bin/sh,#! /bin/bash,' install.sh 

export CFLAGS="%optflags"
%if %{cc_is_gcc}
export CC=gcc
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export LD_OPTIONS="-L/usr/gnu/lib -R/usr/gnu/lib"
%else
export LDFLAGS="%_ldflags"
%endif
export SHELL="/bin/bash"
export MAKESHELL="/bin/bash"

bash ./configure             \
    -prefix %{_prefix}       \
    -libdir %{_libdir}/coq   \
    -docdir %{_docdir}/coq-%{src_ver} \
    -mandir %{_mandir}       \
    -camldir %{_bindir} \
    -camlp5dir %{_libdir}/ocaml/camlp5 \
    -emacs %{_datadir}/emacs/site-lisp \
    -with-cc "$CC"           \
    -with-doc yes \
    -fsets all \
    -reals all \
    -annotate \
    -opt

sed -i -e "1iexport SHELL:=/bin/bash" Makefile Makefile.stage1

%if %{cc_is_gcc}
sed -i -e 's,CFLAGS=-fno-defer-pop -Wall -Wno-unused,CFLAGS=-fno-defer-pop -Wall -Wno-unused %optflags,' config/Makefile
%else
sed -i -e 's,CFLAGS=-fno-defer-pop -Wall -Wno-unused,CFLAGS=%optflags,' config/Makefile
%endif

%build
export CFLAGS="%optflags"
%if %{cc_is_gcc}
export CC=gcc
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export LD_OPTIONS="-L/usr/gnu/lib -R/usr/gnu/lib"
%else
export LDFLAGS="%_ldflags"
%endif
export LD_LIBRARY_PATH="${PWD}/kernel/byterun"
export SHELL="/bin/bash"
export MAKESHELL="/bin/bash"
make world VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT

export CFLAGS="%optflags"
%if %{cc_is_gcc}
export CC=gcc
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export LD_OPTIONS="-L/usr/gnu/lib -R/usr/gnu/lib"
%else
export LDFLAGS="%_ldflags"
%endif
export SHELL="/bin/bash"
export MAKESHELL="/bin/bash"
make COQINSTALLPREFIX=$RPM_BUILD_ROOT install VERBOSE=1

# Prepare lists of files for packaging
touch SFEcoq-all.files

find $RPM_BUILD_ROOT%{_prefix} \( -type f -o -type l \) -name "*" > SFEcoq-all.files
sort SFEcoq-all.files > SFEcoq-all-sort.files
# Clean up syntax for %files section
sed -i -e 's:'"$RPM_BUILD_ROOT"'::' SFEcoq-all-sort.files

%clean
rm -rf $RPM_BUILD_ROOT

%files -f SFEcoq-all-sort.files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, bin) %{_libdir}

%dir %attr (0755, root, bin) %{_libdir}/coq
%dir %attr (0755, root, bin) %{_libdir}/coq/user-contrib
%dir %attr (0755, root, bin) %{_libdir}/coq/ide
%{_libdir}/coq/ide/.coqide-gtk2rc
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, root) %{_datadir}/emacs
%dir %attr (0755, root, root) %{_datadir}/emacs/site-lisp
%dir %attr (0755, root, other) %{_docdir}

%changelog
* Tue July 20 2010 - markwright@internode.on.net
- Initial spec
