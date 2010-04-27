# spec file for package abiword 
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:        abiword
Version:     2.8.4
Release:     1
Summary:     Lean and fast full-featured word processor
Copyright:   GPL
URL:         http://www.abisource.com/
Source:      http://www.abisource.com/downloads/%{name}/%{version}/source/%{name}-%{version}.tar.gz
Patch1:      %{name}-01-suncc-map.diff
Patch2:      %{name}-02-ut-xml-define.diff
Patch3:      %{name}-03-unistd.diff
Patch4:      %{name}-04-endian.diff
BuildRoot:   %{_tmppath}/%{name}-%{version}-root
BuildRequires:	GConf-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	freetype2-devel
BuildRequires:	gcc-c++
BuildRequires:	gnome-vfs-devel
BuildRequires:	gnome-print-devel
BuildRequires:	libMagick-devel
BuildRequires:	libbzip2-devel
BuildRequires:	libgal-devel
BuildRequires:	libglade-devel
BuildRequires:	libtool-devel
BuildRequires:	libpspell-devel
BuildRequires:	libwmf-devel >= 0.2.1
BuildRequires:	libxml2-devel
BuildRequires:	texinfo

%description
AbiWord is a cross-platform, Open Source Word Processor developed
by the people at AbiSource, Inc. and by developers from around the world.
(http://www.abisource.com)
It is a lean and fast full-featured word processor. It works on Microsoft
Windows and most Unix Systems. Features include:

   * Basic character formatting (bold, underline, italics, etc.)
   * Paragraph alignment
   * Spell-check
   * Import of Word97 and RTF documents
   * Export to RTF, Text, HTML, and LaTeX formats
   * Interactive rulers and tabs
   * Styles
   * Unlimited undo/redo
   * Multiple column control
   * Widow/orphan control
   * Find/Replace
   * Images 

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

./configure --prefix=%{_prefix}			\
			--libdir=%{_libdir}			\
			--bindir=%{_bindir}			\
			--includedir=%{_includedir}	\
			--sysconfdir=%{_sysconfdir}	\
			--datadir=%{_datadir}		\
			--mandir=%{_mandir}			\

make -j $CPUS

%install
rm -rf ${RPM_BUILD_ROOT}
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc abi/user/wp/readme.txt abi/BUILD abi/BUILD.TXT abi/BiDiReadme.txt abi/COPYING abi/COPYRIGHT.TXT abi/CREDITS.TXT abi/README.TXT abi/TODO.TXT abi/UnixFonts.txt abi/UnixLocales.txt abi/VERSION.TXT abi/abi2po.pl abi/po2abi.pl
%doc abi/docs/*.abw abi/docs/*.txt abi/docs/*.html abi/docs/status/*.xsl abi/docs/status/*.xml
%{_bindir}/*
%dir %{_datadir}/AbiSuite
%{_datadir}/AbiSuite/AbiWord
%{_datadir}/AbiSuite/README
%{_datadir}/AbiSuite/clipart
%dir %{_datadir}/AbiSuite/dictionary
%{_datadir}/AbiSuite/dictionary
%{_datadir}/AbiSuite/fonts
%{_datadir}/AbiSuite/icons
%{_datadir}/AbiSuite/templates
%defattr(-, root, root)
/usr/X11R6/bin/abiword

%changelog
* Tue Apr 27 2010 - brian.cameron@sun.com
- Bump to 2.8.4.
* Fri Mar 05 2010 - brian.cameron@sun.com
- Bump to 2.8.2.
* Wed Feb 03 2010 - brian.cameron@sun.com
- Bump to 2.8.1.  Remove upstream patches and patches that no longer apply.
* Sat Nov 17 2007 - daymobrew@users.sourceforge.net
- Remove obsolete patch, 08-package-str.
* Wed Sep 26 2007 - nonsea@users.sourceforge.net
- Initial spec
