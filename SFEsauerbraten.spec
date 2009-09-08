#
# spec file for package SFEsauerbraten.spec
#
# includes module(s): sauerbraten
#
%include Solaris.inc

%define src_name	sauerbraten
%define src_url		http://nchc.dl.sourceforge.net/sourceforge/sauerbraten
%define src_edition	trooper_edition_linux

Name:                   SFEsauerbraten
Summary:                Sauerbraten game engine
Version:                2009_05_04
IPS_component_version:	20090504
Source:                 %{src_url}/%{src_name}_%{version}_%{src_edition}.tar.bz2
Patch1:			sauerbraten-01-solaris.diff
Patch2:			sauerbraten-02-startup.diff
Copyright:		sauerbraten.copyright
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEsdl-mixer-devel
Requires: SFEsdl-mixer
BuildRequires: SFEsdl-image-devel
Requires: SFEsdl-image

%prep
%setup -q -n %{src_name}
%patch1 -p1
%patch2 -p1
#remove files that we can't package
find . -name '\!*' -exec rm {} \; -print
# fix filenames 
perl -pi -e 's/\&/_and_/' packages/dg/package.cfg
mv packages/dg/floor_grass3\&soil.jpg packages/dg/floor_grass3_and_soil.jpg
mv packages/dg/floor_soil\&grave3.jpg packages/dg/floor_soil_and_grave3.jpg

mv packages/models/psionic/Psionic\ permission.txt packages/models/psionic/Psionic_permission.txt
mv packages/models/aftas/aftasardem\ licence.txt packages/models/aftas/aftasardem_licence.txt
mv packages/models/xeno/Xeno\ permission.txt packages/models/xeno/Xeno_permission.txt
mv packages/fanatic/Track\ Names.txt packages/fanatic/Track_Names.txt
mv packages/mitaman/mitaman\ texture\ readme.txt packages/mitaman/mitaman_texture_readme.txt
mv packages/mitaman/mm-texture\ readme.txt packages/mitaman/mm-texture_readme.txt
mv packages/dash/Dash\ Readme.txt packages/dash/Dash_Readme.txt
mv packages/loopix/loopix\ readme.txt packages/loopix/loopix_readme.txt
mv packages/aftas/aftasardem\ licence.txt packages/aftas/aftasardem_licence.txt
mv packages/ratboy/skyboxes/Coward\ Cove.txt packages/ratboy/skyboxes/Coward_Cove.txt
mv packages/noctua/noctua\ readme.txt packages/noctua/noctua_readme.txt
mv packages/golgotha/golgotha\ readme.txt packages/golgotha/golgotha_readme.txt
mv packages/blikjebier/snow/snow_path_2_end\ 2.jpg packages/blikjebier/snow/snow_path_2_end_2.jpg

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd src
export CXX=/usr/gnu/bin/g++
export CXXOPTFLAGS="-O3 -fno-omit-frame-pointer"
export LD_OPTIONS="-i %{xorg_lib_path} %{gnu_lib_path}"
make -j $CPUS install

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/sauerbraten
chmod 755 sauerbraten_unix
cp -p sauerbraten_unix $RPM_BUILD_ROOT%{_bindir}/sauerbraten
/usr/bin/tar fcp - README.html bin_unix data packages | ( cd $RPM_BUILD_ROOT%{_datadir}/sauerbraten && tar fxp - )

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/sauerbraten

%changelog
* Tue Sep  8 2009 - drdoug007@gmail.com
- Bumped to Trooper Edition (2009_05_04)
* Tue Jun  5 2007 - dougs@truemail.co.th
- Initial version
