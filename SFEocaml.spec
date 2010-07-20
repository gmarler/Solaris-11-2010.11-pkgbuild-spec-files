#
# spec file for package SFEocaml
#
# includes module(s): ocaml
#

%include Solaris.inc

# SFEocaml, SFEcamlp5, SFEhevea compiles with Sun Studio 12u1 cc,
# and I guess SFElablgtk and SFEunison do as well.
# However SFEcoq wants SFEocaml to be compiled with gcc, to enable
# the THREADED_CODE define in /usr/lib/ocaml/caml/config.h
%define cc_is_gcc 1
%include base.inc

%define with_emacs %(pkginfo -q SFEemacs && echo 1 || echo 0)

Name:         SFEocaml
Summary:      ocaml - Objective Caml Programming Language
Version:      3.11.2
License:      GPL
Group:        Development/Languages
Release:      1
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Source0:      http://caml.inria.fr/pub/distrib/ocaml-3.11/ocaml-%{version}.tar.bz2
Patch1:       ocaml-01-ldflags.diff
URL:          http://caml.inria.fr/
SUNW_BaseDir: %{_basedir}
%include default-depend.inc
Requires:     SUNWlibms
%if %option_with_fox
Requires: FSWxorg-clientlibs
Requires: FSWxwrtl
BuildRequires: FSWxorg-headers
%else
Requires:     SUNWxwrtl
Requires:     SUNWxwplt
%endif
Requires:     SUNWTcl
Requires:     SUNWTk
BuildRequires: SUNWsfwhea
%if %with_emacs
BuildRequires: SFEemacs
%endif

%description
Objective Caml (OCaml) is a general-purpose programming language descended
from the ML family.  OCaml is an open source project managed and principally
maintained by INRIA.

OCaml shares the functional and imperative programming features of ML, but
adds object-oriented constructs and has minor syntax differences.  Like all
descendants of ML, OCaml is compiled, statically typed, strictly evaluated,
and uses automatic memory management.

OCaml's toolset includes an interactive toplevel, a bytecode compiler, and
an optimizing native code compiler.  It has a large standard library that
makes it useful for many of the same applications as Python or Perl, as
well as robust modular and object-oriented programming constructs that
make it applicable for large-scale software engineering.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n ocaml-%version
%patch1 -p1 -b .ldflags

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
%if %option_with_fox
# for <X11/Xlib.h>
export CFLAGS="$CFLAGS -I/usr/X11/include"
%endif

%if %{cc_is_gcc}
export CC=gcc
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export LD_OPTIONS="-L/usr/gnu/lib -R/usr/gnu/lib"
%else
export LDFLAGS="%_ldflags"
%endif

./configure                     \
       -verbose                 \
       -prefix %{_prefix}       \
       -libdir %{_libdir}/ocaml \
       -mandir %{_mandir}       \
       -cc "$CC $CFLAGS"        \
       -libs "$LDFLAGS"         \
       -dllibs "$LDFLAGS -lsocket -lnsl" \
       -tkdefs "-I/usr/sfw/include" \
       -tklibs "-L/usr/sfw/lib -R/usr/sfw/lib -ltk8.3"

#FIXME: can not use make -j$CPUS world.opt LIBS="-lsocket -lnsl"
#make -j$CPUS world.opt LIBS="-lsocket -lnsl"
make world
make opt
make opt.opt

%install
rm -rf $RPM_BUILD_ROOT
umask 022
make install \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    LIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
    MANDIR=$RPM_BUILD_ROOT%{_mandir}

%if %with_emacs
cd emacs
make install EMACSDIR=$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/ocaml
%dir %attr (0755, root, sys) %{_datadir}
%if %with_emacs
%attr (0755, root, root) %{_datadir}/emacs
%endif
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man[13]
%{_mandir}/man[13]/*

%changelog
* Sun May 23 2010 - markwright@internode.on.net
- bump to 3.11.2
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Enable building with either SUNWlibsdl or SFEsdl.
* Thu Aug 24 2006 - halton.huo@sun.com
- use %if for emacs depend
* Thu Jul 27 2006 - halton.huo@sun.com
- Add check depend on emacs
- Correct make fail, may need find a better way later.
* Tue Jul 11 2006 - laca@sun.com
- Created.
