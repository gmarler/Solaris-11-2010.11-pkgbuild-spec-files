# Gilles Dauphin
#

%include Solaris.inc

%define python_version 2.6
%define src_version 2.49b
%define src_url http://download.blender.org/source

Name:           SFEblender
Summary:        Blender - Open source 3D creation tools
Version:        2.49.2
Source:		%{src_url}/blender-%{src_version}.tar.gz
Patch1:		blender-01-build.diff
Patch2:		blender-02-install.diff
Patch3:		blender-03-union.diff
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include	default-depend.inc
Requires: 	SUNWlibsdl
Requires: 	SUNWopenexr
Requires: 	SUNWilmbase
%ifarch i386 amd64
Requires: 	SUNWxorg-mesa
%endif
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
cd blender-%{src_version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

NAN_NO_KETSJI=true
export NAN_NO_KETSJI
NAN_OPENEXR=/usr 
export NAN_OPENEXR
NAN_PYTHON_VERSION=%{python_version}
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

export PKG_CONFIG_PATH="$PROTO_PKG"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"

cd blender-%{src_version}

gmake REL_CFLAGS="$CFLAGS -DNDEBUG" REL_CCFLAGS="$CXXFLAGS -DNDEBUG"

%install

NAN_NO_KETSJI=true
export NAN_NO_KETSJI
NAN_OPENEXR=/usr 
export NAN_OPENEXR
NAN_PYTHON_VERSION=%{python_version}
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
cd blender-%{src_version}
gmake release
# x86_64, i386, etc.
cd obj/blender-%{version}-solaris-2.11-*-py%{python_version}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/blender

for f in blender.html BlenderQuickStart.pdf copyright.txt GPL-license.txt Python-license.txt release_`echo '%{src_version}' | tr -d '[a-z.]'`.txt ; do
   install -m 0644 $f $RPM_BUILD_ROOT%{_datadir}/blender
done

cd .blender
tar cf - . | (cd $RPM_BUILD_ROOT%{_datadir}/blender ; tar xfp -)
cd ..

install -d -m 0755 $RPM_BUILD_ROOT/%{_bindir}
install -m 0755 blender $RPM_BUILD_ROOT%{_bindir}/blender-bin
cat > blender.sh <<EOF
#!/bin/sh
# Idea from pkgsrc GD 20080916

BLENDER_DATA="%{_datadir}/blender"
BLENDER_HOME="\${HOME}/.blender"

if  [ ! -d "\${BLENDER_HOME}" ]; then
	echo "Softlinking \$BLENDER_HOME to point to global \$BLENDER_DATA settings."
	mkdir -p "\${BLENDER_HOME}"
	mkdir -p "\${BLENDER_HOME}/scripts"
	ln -s "\${BLENDER_DATA}/.Blanguages" "\${BLENDER_HOME}/.Blanguages"
	ln -s "\${BLENDER_DATA}/.bfont.ttf" "\${BLENDER_HOME}/.bfont.ttf"
fi

# Check for new scripts
(cd "\${BLENDER_DATA}" && for file in *; do
	[ -r "\${BLENDER_HOME}/\${file}" ] || \
		ln -s "\${BLENDER_DATA}/\${file}" "\${BLENDER_HOME}/\${file}"
done)

exec %{_bindir}/blender-bin "\$@"
EOF

install -m 0755 blender.sh $RPM_BUILD_ROOT%{_bindir}/blender

#%if %build_l10n
#%else
#rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
#%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/blender-bin
%{_bindir}/blender
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
* May 18 2010 - G.D.
- exec in bindir
* Wed May 12 2010 - Albert Lee <trisk@opensolaris.org>
- Bump to 2.49b
- Update Python version to 2.6
- Fix install on non-amd64
- Create wrapper at build time
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
