#
# spec file for package: nexuiz
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define datez 20091001

Name:		SFEnexuiz
Summary:      	Nexuiz - A fast-paced 3D first-person shooter
Version:       	252
License:	GPLv2
Url: 		http://alientrap.org/nexuiz
Source:	 	http://downloads.sourceforge.net/nexuiz/nexuiz-%{version}.zip
Source1:	nexuiz
Group:		Games
Distribution:   OpenSolaris
Vendor:		OpenSolaris Community

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
SUNW_Basedir:   %{_basedir}

%include default-depend.inc
BuildRequires:	SUNWaudh
BuildRequires:	SUNWunzip
BuildRequires:	SUNWgmake
BuildRequires:	SUNWgcc
BuildRequires:	SUNWimagick
BuildRequires:	SUNWxwinc
BuildRequires:	SUNWxorg-headers
BuildRequires:	NVDAgraphics
BuildRequires:	SUNWxorg-mesa
BuildRequires:	SUNWzip

# OpenSolaris IPS Manifest Fields
Meta(info.upstream):	 	Alientrap
Meta(info.maintainer):	 	Andras Barna
Meta(info.repository_url):	svn://svn.icculus.org/nexuiz/trunk
Meta(info.detailed_url):	http://www.alientrap.org/nexuiz

%description
Nexuiz is a fast paced 3d deathmatch game project created online 
by a team of developers called Alientrap.

%prep
rm -rf Nexuiz
%setup -q -n Nexuiz


%build
export CC=/usr/sfw/bin/gcc 
export CFLAGS="%gcc_optflags"
export LDFLAGS="%_ldflags"

cd sources
unzip -o enginesource%{datez}.zip
cd darkplaces
echo "SHELL=/bin/bash" > makefile.good
cat makefile >> makefile.good
gmake -f makefile.good cl-nexuiz
convert nexuiz.xpm nexuiz.png
#touch nexuiz.png

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/nexuiz/data
mkdir -p $RPM_BUILD_ROOT/usr/share/pixmaps

install --mode=755 %{SOURCE1} $RPM_BUILD_ROOT/usr/bin
install --mode=755 sources/darkplaces/nexuiz-glx $RPM_BUILD_ROOT/usr/share/nexuiz
cp sources/darkplaces/nexuiz.png $RPM_BUILD_ROOT/usr/share/pixmaps

cd data
zipsplit -n 104857600 data%{datez}.pk3 
mv data20_1.zip data%{datez}.1.pk3
mv data20_2.zip data%{datez}.2.pk3
mv data20_3.zip data%{datez}.3.pk3
mv data20_4.zip data%{datez}.4.pk3
mv data20_5.zip data%{datez}.5.pk3
mv data20_6.zip data%{datez}.6.pk3

cd ..

cp data/data%{datez}.1.pk3 $RPM_BUILD_ROOT/usr/share/nexuiz/data
cp data/data%{datez}.2.pk3 $RPM_BUILD_ROOT/usr/share/nexuiz/data
cp data/data%{datez}.3.pk3 $RPM_BUILD_ROOT/usr/share/nexuiz/data
cp data/data%{datez}.4.pk3 $RPM_BUILD_ROOT/usr/share/nexuiz/data
cp data/data%{datez}.5.pk3 $RPM_BUILD_ROOT/usr/share/nexuiz/data
cp data/data%{datez}.6.pk3 $RPM_BUILD_ROOT/usr/share/nexuiz/data

cp data/common-spog.pk3 $RPM_BUILD_ROOT/usr/share/nexuiz/data
cp havoc/data%{datez}havoc.pk3 $RPM_BUILD_ROOT/usr/share/nexuiz/data

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%postun
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/nexuiz
%dir %attr (-, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%changelog
* Sun May 16 2010 - Milan Jurik
- added to SFE and update to 2.52
* Wed Mar 25 2009 - andras.barna@gmail.com
- Initial spec
