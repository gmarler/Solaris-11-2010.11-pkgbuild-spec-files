#
# spec file for package: transfig
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): transfig
#

%include Solaris.inc

%define src_name transfig

Name:		SFEtransfig
Summary:      	Tool to convert fig drawings (xfig) to other formats.
Version:       	3.2.5
Release:        a
License:	Xfig license
Url: 		http://xfig.org
Source:	 	http://downloads.sourceforge.net/mcj/%{src_name}.%{version}%{release}.tar.gz
Distribution:   OpenSolaris
Vendor:		OpenSolaris Community
BuildRoot:      %{_tmppath}/%{src_name}-%{version}%{release}-build
SUNW_Basedir:   %{_basedir}
SUNW_Copyright: %{src_name}.copyright

%include default-depend.inc

BuildRequires:  SUNWxwopt
BuildRequires:  SUNWxwinc
BuildRequires:  SUNWbtool
BuildRequires:  SUNWgnu-coreutils
BuildRequires:  SUNWgmake

Requires:       SUNWpng
Requires:       SUNWjpg
Requires:       SUNWzlib
Requires:       print/filter/ghostscript
Requires:       SFEnetpbm

Patch0:         transfig-0-3.2.5a-fig2dev-Imakefile.diff
Patch1:         transfig-1-3.2.5a-transfig-Imakefile.diff

# OpenSolaris IPS Package Manifest Fields
Meta(info.upstream):	 	Brian V. Smith<bvsmith@lbl.gov>
Meta(info.maintainer):	 	Federico Beffa<beffa@ieee.org>
Meta(info.detailed_url):        http://xfig.org
Meta(info.repository_url):	http://downloads.sourceforge.net/mcj/transfig.3.2.5a.tar.gz
Meta(info.classification):      org.opensolaris.category.2008:Applications/Graphics and Imaging

%description 
A tool to convert pictures generated with xfig to many other formats 
including vector formats such as EPS, PS, PDF and bitmap formats as
e.g. PNG. One strength of the program is the ability to create highly 
portable PIC figures to be used with LaTeX.

%prep
rm -rf %{src_name}.%{version}%{release}
%setup -q -n %{src_name}.%{version}%{release}
%patch0 -p1 -b .dif2dev-Imakefile
%patch1 -p1 -b .transfig-Imakefile

%build
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
export PATH=${PATH}:/usr/X11/bin
xmkmf
make DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} XFIGLIBDIR=%{_datadir}/xfig MANDIR=%{_mandir}/man1 FIG2DEV_LIBDIR=%{_datadir}/%{src_name} INSTALL=/usr/bin/ginstall MKDIRHIER="mkdir -p" MAKE=/usr/gnu/bin/make Makefiles

make DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} XFIGLIBDIR=%{_datadir}/xfig MANDIR=%{_mandir}/man1 FIG2DEV_LIBDIR=%{_datadir}/%{src_name} INSTALL=/usr/bin/ginstall MKDIRHIER="mkdir -p" MAKE=/usr/gnu/bin/make

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} XFIGLIBDIR=%{_datadir}/xfig MANDIR=%{_mandir}/man1 FIG2DEV_LIBDIR=%{_datadir}/%{src_name} INSTALL=/usr/bin/ginstall MKDIRHIER="mkdir -p" MAKE=/usr/gnu/bin/make install

make DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} XFIGLIBDIR=%{_datadir}/xfig MANDIR=%{_mandir}/man1 FIG2DEV_LIBDIR=%{_datadir}/%{src_name} INSTALL=/usr/bin/ginstall MKDIRHIER="mkdir -p" MAKE=/usr/gnu/bin/make install.man

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root, bin)
%doc CHANGES NOTES README LATEX.AND.XFIG
%{_bindir}/*
%dir %attr (0755, root, bin) %{_mandir}
%attr (0444, root, bin) %{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_datadir}
%{_datadir}/transfig/*
%{_datadir}/xfig/*

%changelog
* may 2010 - Gilles Dauphiun
- import in SFE, name is SFE...
* Fri Jul 24 - beffa@ieee.org
- initial version
## Re-build 24/09/09
