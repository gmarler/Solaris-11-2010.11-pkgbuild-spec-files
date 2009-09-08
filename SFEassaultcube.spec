#
# spec file for package SFEassaultcube.spec
#
# includes module(s): assaultcube
#
%include Solaris.inc

%define src_name	AssaultCube
%define src_url		http://switch.dl.sourceforge.net/sourceforge/actiongame
%define src_ver		1.0.2

Name:                   SFEassaultcube
Summary:                AssaultCube Game
Version:                1.0.4
Source:                 %{src_url}/%{src_name}_v%{src_ver}.tar.bz2
Source1:                %{src_url}/%{src_name}_v%{version}-Update.tar.bz2
Patch1:			assaultcube-01-solaris.diff
Patch2:			assaultcube-02-conflict.diff
Patch3:			assaultcube-03-cmds.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEsdl-mixer-devel
Requires: SFEsdl-mixer
BuildRequires: SFEsdl-image-devel
Requires: SFEsdl-image

%prep
%setup -q -n %{src_name}_v%{src_ver}
gtar fxvj %{SOURCE1}
%patch1 -p1
%patch2 -p1
%patch3 -p1
mv "docs/How to add to the reference.txt" docs/How_to_add_to_the_reference.txt
#remove files that we can't package
find . -name '\!*' -exec rm {} \; -print

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd source/src
export CXX=/usr/sfw/bin/g++
export CXXOPTFLAGS="-O3 -fno-omit-frame-pointer"
export LD_OPTIONS="-i %{xorg_lib_path} %{gnu_lib_path}"
make -j $CPU install

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/assaultcube
chmod 755 assaultcube.sh server.sh
cp -p assaultcube.sh $RPM_BUILD_ROOT%{_bindir}/assaultcube
/usr/bin/tar fcp - README.html bot bin_unix config demos docs mods icon.ico packages server.sh server_wizard.sh assaultcube.sh | ( cd  $RPM_BUILD_ROOT%{_datadir}/assaultcube && tar fxv - )

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/assaultcube

%changelog
* Sun Sep 06 2009 - drdoug007@gmail.com
- Bumped to 1.0.4

* Mon Jul 10 2007 - dougs@truemail.co.th
- Initial version
