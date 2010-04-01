#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define src_version 2.08.01

Name:                SFEnasm
Summary:             Portable, modular 80x86 assembler
Version:             2.8.1
Source:              http://www.nasm.us/pub/nasm/releasebuilds/%{src_version}/nasm-%{src_version}.tar.bz2
License:             2-BSD
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:       SUNWtexi
BuildRequires:       SUNWghostscript

%prep
%setup -q -n nasm-%src_version

%build

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --infodir=%{_datadir}/info

make everything

%install
rm -rf "$RPM_BUILD_ROOT"

mkdir -p "$RPM_BUILD_ROOT"
mkdir -p "$RPM_BUILD_ROOT"%{_bindir}
mkdir -p "$RPM_BUILD_ROOT"%{_mandir}/man1
mkdir -p "$RPM_BUILD_ROOT"/%{_infodir}
DOC="$RPM_BUILD_ROOT"%{_docdir}/nasm
mkdir -p "$DOC"
mkdir -p "$DOC"/rdoff
make INSTALLROOT="$RPM_BUILD_ROOT" \
        docdir=%{docdir}/nasm \
        install_everything
cp AUTHORS CHANGES LICENSE README TODO doc/*.doc "$DOC"
cp rdoff/README "$DOC"/rdoff
cp rdoff/doc/* "$DOC"/rdoff

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_datadir}/info
%{_datadir}/info/*
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/doc/nasm
%{_datadir}/doc/nasm/*

%changelog
* Apr 01 2010 - Milan Jurik
- update to 2.08.01
- build dependency fix
* Mar 22 2010 - Gilles Dauphin
- _bindir instead of /usr/bin
* Sat Aug 22 2009 - Milan Jurik
- update to 2.07
* Sat Jun 13 2009 - Milan Jurik
- upgrade to 2.06rc12
* Sat Mar 14 2009 - Milan Jurik
- upgrade to 2.06rc1
* Thu Dec 14 2006 - Eric Boutilier
- Initial spec
