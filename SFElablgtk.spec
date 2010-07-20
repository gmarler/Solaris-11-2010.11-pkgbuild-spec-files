#
# spec file for package SFElablgtk
#
# includes module(s): LablGTK
#

%include Solaris.inc

# SFEocaml, SFEcamlp5, SFEhevea compiles with Sun Studio 12u1 cc,
# and I guess SFElablgtk and SFEunison do as well.
# However SFEcoq wants SFEocaml to be compiled with gcc, to enable
# the THREADED_CODE define in /usr/lib/ocaml/caml/config.h
%define cc_is_gcc 1

Name:         SFElablgtk
Summary:      LablGTK - objective caml bindings for gtk+
Version:      2.6.0
License:      GPL
Group:        libraries/GNOME/bindings
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Source0:      http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/dist/lablgtk-%{version}.tar.gz
URL:          http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/lablgtk.html
SUNW_BaseDir: %{_basedir}
%include default-depend.inc
Requires:     SFEocaml
Requires:     SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires:     SUNWlibrsvg
BuildRequires: SUNWlibrsvg-devel
Requires:     SUNWgnome-panel
BuildRequires: SUNWgnome-panel-devel
Requires:     SFEgtkspell
BuildRequires: SFEgtkspell-devel

%description
LablGTK is is an Objective Caml interface to gtk+.

%prep
%setup -q -n lablgtk-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure                          \
    --prefix=%{_prefix}              \
    --with-libdir=%{_libdir}/ocaml   \
    --with-glade                     \
    --with-rsvg                      \
    --with-gnomecanvas

make -j$CPUS
cd src
make -j$CPUS \
    lablgtk.cmxa \
    gtkInit.cmx \
    lablglade.cmxa \
    lablrsvg.cmxa \
    lablgnomecanvas.cmxa \
    lablgnomeui.cmxa \
    lablpanel.cmxa \
    lablgtkspell.cmxa

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/ocaml/lablgtk2/win32.h

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/ocaml/lablgtk2
%{_libdir}/ocaml/stublibs/dlllablglade2.so
%{_libdir}/ocaml/stublibs/dlllablgnomecanvas.so
%{_libdir}/ocaml/stublibs/dlllablgnomeui.so
%{_libdir}/ocaml/stublibs/dlllablgtk2.so
%{_libdir}/ocaml/stublibs/dlllablgtkspell.so
%{_libdir}/ocaml/stublibs/dlllablpanel.so
%{_libdir}/ocaml/stublibs/dlllablrsvg.so

%changelog
* Fri Jan  5 2007 - laca@sun.com
- add SFEgtkspell dependency, add lablgtkspell.cmxa to build targets and
  update pkging
* Tue Jul 11 2006 - laca@sun.com
- Created.
