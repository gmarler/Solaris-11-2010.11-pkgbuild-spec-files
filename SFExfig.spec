#
# spec file for package: xfig
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): xfig
#

%include Solaris.inc

%define src_name xfig

Name:		SFExfig
Summary:      	Xfig is an interactive drawing tool for X
Version:       	3.2.5
Release:        b
License:	Xfig license
Url: 		http://xfig.org
Source:	 	http://downloads.sourceforge.net/mcj/xfig.%{version}%{release}.full.tar.gz
Distribution:   OpenSolaris
Vendor:		OpenSolaris Community
BuildRoot:      %{_tmppath}/%{name}-%{version}%{release}-build
SUNW_Basedir:   /
SUNW_Copyright: %{src_name}.copyright

%include default-depend.inc

BuildRequires:  SUNWxwopt
BuildRequires:  SUNWxwinc
BuildRequires:  SUNWbtool
BuildRequires:  SUNWgnu-coreutils
BuildRequires:  SUNWgmake

Requires:       SUNWpng
Requires:       SUNWzlib
Requires:       SUNWjpg
Requires:       SFEXaw3d
# wait for transfig and netpbm to be in /contrib
Requires:       SFEtransfig
Requires:       SFEnetpbm

Source1:        xfig.desktop
Source2:        xfig.png

Patch0:         xfig-01-3.2.5b-Imakefile.diff
Patch1:         xfig-02-3.2.5b-w_keyboard.c.diff
Patch2:         xfig-03-3.2.5b-Fig.ad.diff
Patch3:         xfig-04-3.2.5b-urwfonts.diff
Patch4:         xfig-05-3.2.5b-w_drawprim.c.diff

# OpenSolaris IPS Package Manifest Fields
Meta(info.upstream):	 	Brian V. Smith<bvsmith@lbl.gov>
Meta(info.maintainer):	 	Federico Beffa<beffa@ieee.org>
Meta(info.detailed_url):        http://xfig.org
Meta(info.repository_url):	http://downloads.sourceforge.net/mcj/xfig.3.2.5b.full.tar.gz
Meta(info.classification):      org.opensolaris.category.2008:Applications/Graphics and Imaging

%description 
XFig is a menu-driven tool that allows the user to draw
and manipulate objects interactively in an X window. The resulting
pictures can be saved, printed on postscript printers, or converted to
a variety of other formats (e.g. to allow inclusion in LaTeX documents
or web pages) using the transfig program.

%prep
rm -rf %{src_name}.%{version}%{release}
%setup -q -n %{src_name}.%{version}%{release}
%patch0 -p1 -b .imake
%patch1 -p1 -b .w_keyboard
%patch2 -p1 -b .Fig.ad
%patch3 -p1 -b .urw
%patch4 -p1 -b .w_drawprim

%build
#export CFLAGS="%optflags -I%{_basedir}/X11/include -DUSE_JPEG -DUSE_XPM -DUSE_XPM_ICON -DXAW3D -DXAW3D1_5E"
export CFLAGS="-g -I%{_basedir}/X11/include -DUSE_JPEG -DUSE_XPM -DUSE_XPM_ICON -DXAW3D -DXAW3D1_5E -DNEWARROWTYPES"
#export LDFLAGS="%{_ldflags} -R%{_basedir}/X11/lib -L%{_basedir}/X11/lib -lXaw3d"
export LDFLAGS=" -g -R%{_basedir}/X11/lib -L%{_basedir}/X11/lib -lXaw3d"
export PATH=${PATH}:/usr/X11/bin
xmkmf
make DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} XFIGLIBDIR=%{_datadir}/%{src_name} XFIGDOCDIR=%{_docdir}/%{src_name}-%{version}%{release} MANDIR=%{_mandir}/man1 INSTALL=/opt/dtbld/bin/install MAKE=/usr/gnu/bin/make XAWLIB="-R%{_basedir}/X11/lib -L%{_basedir}/X11/lib -lXaw3d" CFLAGS="$CFLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} XFIGLIBDIR=%{_datadir}/%{src_name} XFIGDOCDIR=%{_docdir}/%{src_name}-%{version}%{release} MANDIR=%{_mandir}/man1 INSTALL=/usr/bin/ginstall MAKE=/usr/gnu/bin/make install.all MKDIRHIER="mkdir -p" XAPPLOADDIR=/usr/X11/lib/X11/app-defaults

make DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} XFIGLIBDIR=%{_datadir}/%{src_name} XFIGDOCDIR=%{_docdir}/%{src_name}-%{version}%{release} MANDIR=%{_mandir}/man1 INSTALL=/usr/bin/ginstall MAKE=/usr/gnu/bin/make install.man MKDIRHIER="mkdir -p" XAPPLOADDIR=/usr/X11/lib/X11/app-defaults

rm -rf $RPM_BUILD_ROOT/usr/X11/man

# install icon
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps

# ... and desktop menu
desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE1}

# need to create link to ghostscript fonts
mkdir -p $RPM_BUILD_ROOT/etc/X11/fontpath.d
ln -s /usr/share/ghostscript/fonts/ $RPM_BUILD_ROOT/etc/X11/fontpath.d/ghostscript:pri=60

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root, bin)
%{_bindir}/*
%dir %attr (0755, root, bin) %{_docdir}
%doc /%{_docdir}/%{src_name}-%{version}%{release}/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/man*/*
%dir %attr (0755, root, bin) %{_datadir}/%{src_name}
%{_datadir}/%{src_name}/*
%dir %attr (0755, root, bin) /usr/X11/lib/X11/app-defaults/
/usr/X11/lib/X11/app-defaults/Fig
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%attr (-, root, root) /etc/X11/fontpath.d/ghostscript:pri=60

%changelog
* May 2010 - Gilles dauphin
- Name is SFE...
* April 2010 - Gilles dauphin
- use SFE
* Fri Jul 24 - beffa@ieee.org
- initial version
## Re-build 24/09/09
