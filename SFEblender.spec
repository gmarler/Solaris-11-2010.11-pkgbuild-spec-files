# Gilles Dauphin
#

%include Solaris.inc

Name:           SFEblender
Summary:        blender
Version:        2.49
Source:		http://download.blender.org/source/blender-%{version}.tar.gz
Source1:	blender-01.sh
Patch1:		blender-01-build.diff
Patch2:		blender-02-install.diff
Patch3:		blender-03-union.diff
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include	default-depend.inc
#Requires:	%name-root
Requires: 	SUNWlibsdl
Requires: 	SUNWopenexr
Requires: 	SUNWilmbase
Requires: 	SUNWxorg-mesa
Requires: 	SUNWfreetype2
Requires: 	SUNWpng
BuildRequires: 	SUNWTiff
BuildRequires: 	SUNWopensslr
BuildRequires: 	SUNWlibsdl-devel
BuildRequires: 	SUNWPython

%package root
Summary:         %summary - platform dependent files, / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:		 %summary - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:		 %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:        %{name}
%endif

%prep
%setup -q -c -n %{name}
cd blender-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

NAN_NO_KETSJI=true
export NAN_NO_KETSJI
NAN_OPENEXR=/usr 
export NAN_OPENEXR
NAN_PYTHON_VERSION=2.4
export NAN_PYTHON_VERSION
NAN_PYTHON=/usr
export NAN_PYTHON
NAN_SDL=/usr
export NAN_SDL
NAN_JPEG=/usr
export NAN_JPEG
NAN_PNG=/usr
export NAN_PNG
NAN_ZLIB=/usr
export NAN_ZLIB
NOPLUGINS=true
export NOPLUGINS


#PROTO_LIB=$RPM_BUILD_DIR/%{name}/usr/X11/lib
#PROTO_INC=$RPM_BUILD_DIR/%{name}/usr/X11/include
#PROTO_PKG=$RPM_BUILD_DIR/%{name}/usr/X11/lib/pkgconfig

export PKG_CONFIG_PATH="$PROTO_PKG"
#export CC=/usr/sfw/bin/gcc
#export LDFLAGS="-L$PROTO_LIB -L/usr/X11/lib -R/usr/X11/lib"

cd blender-%{version}

#export LDFLAGS="-L$PROTO_LIB -L/usr/X11/lib -L/usr/openwin/lib -R/usr/X11/lib -R/usr/openwin/lib -lX11 -lXext"

gmake

%install

NAN_NO_KETSJI=true
export NAN_NO_KETSJI
NAN_OPENEXR=/usr 
export NAN_OPENEXR
NAN_PYTHON_VERSION=2.4
export NAN_PYTHON_VERSION
NAN_PYTHON=/usr
export NAN_PYTHON
NAN_SDL=/usr
export NAN_SDL
NAN_JPEG=/usr
export NAN_JPEG
NAN_PNG=/usr
export NAN_PNG
NAN_ZLIB=/usr
export NAN_ZLIB
NOPLUGINS=true
export NOPLUGINS

rm -rf $RPM_BUILD_ROOT
#mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
cd blender-%{version}
gmake release
cd obj/blender-2.49.0-solaris-2.11-x86_64-py2.4
mkdir -p $RPM_BUILD_ROOT%{_datadir}/blender
#chown root:bin $RPM_BUILD_ROOT%{_datadir}/blender

for f in blender.html BlenderQuickStart.pdf copyright.txt GPL-license.txt Python-license.txt release_248.txt ; do
   install -m 0644 $f $RPM_BUILD_ROOT%{_datadir}/blender
done

install -d -m 0755 $RPM_BUILD_ROOT/%{_bindir}
install -m 0755 blender $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{_bindir}/blender $RPM_BUILD_ROOT%{_bindir}/blender.exe
cd .blender
tar cf - . | (cd $RPM_BUILD_ROOT%{_datadir}/blender ; tar xfp -)

cd ..
cp %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/blender
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/blender
#chown root:bin $RPM_BUILD_ROOT%{_bindir}/blender


#%if %build_l10n
#%else
#rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
#%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/blender.exe
%attr(0755, root, bin) %{_bindir}/blender
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/blender
%{_datadir}/blender/*
%{_datadir}/blender/.Blanguages
%{_datadir}/blender/.bfont.ttf


#%if %build_l10n
#%files l10n
#%defattr (-, root, bin)
#%dir %attr (0755, root, sys) %{_datadir}
#%attr (-, root, other) %{_datadir}/locale
#%endif

%changelog
* Jue  17 2009 - Simonjin
- Bump to 2.49, and update the patch blender-01-build.diff
* April 2009 - Gilles dauphin
- adjust version for IPS
* Sun 18 Jan 2009 - Henry Zhang
- Bump to 2.48a, and update the patch and blender-01.sh.
* Thu 27 Nov 2008 - Henry Zhang
- Add dependency SUNWilmbase
* Sun 09 Nov 2008 - Gilles Dauphin
- depend SUNWopenexr
* Sept 16 2008 - Gilles Dauphin ( Gilles DOT Dauphin AT enst DOT fr)
- Initial spec
