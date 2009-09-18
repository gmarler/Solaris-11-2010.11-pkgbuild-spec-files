#
# spec file for package SFEsimutrans.spec
#
%include Solaris.inc

%define src_version 102-0

Name:           SFEsimutrans
Version:        102.0
Summary:        Transport system simulation game
Source:         http://downloads.sourceforge.net/simutrans/simutrans-src-%{src_version}.zip
#Source1:	http://sourceforge.net/projects/simutrans/files/pak64/pak64-%{src_version}.zip
Source1:	http://sourceforge.net/projects/simutrans/files/Simutrans%20complete/simulinux_0-%{src_version}.zip
Patch1:		simutrans-01-config.diff
Patch2:		simutrans-02-label_t.diff
Patch3:		simutrans-03-datapath.diff
URL:            http://www.simutrans.com/
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:  SUNWlibsdl-devel
Requires:  SUNWlibsdl
BuildRequires:  SFEsdl-mixer-devel
Requires:  SFEsdl-mixer
BuildRequires:  SUNWpng-devel
Requires:  SUNWpng
BuildRequires:  SUNWunzip
BuildRequires:  SUNWzlib
Requires:  SUNWzlib

%description
In Simutrans you can build the transport networks you always dreamed of, with platforms, quays, level crossings, signals and much more. Transport passengers between nearby cities with a commuter train or use a high speed train to earn big money by connecting cities further apart.

%package data
Summary:       %{summary} - pak64 files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name


%prep
rm -rf %name-%{version}-build
mkdir -p %name-%{version}-build
cd %name-%{version}-build
unzip %SOURCE
unzip -n %SOURCE1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd %name-%{version}-build
CXX=/usr/sfw/bin/c++ make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
cd %name-%{version}-build
cp sim $RPM_BUILD_ROOT/usr/bin/simutrans
mkdir -p $RPM_BUILD_ROOT/usr/share/simutrans
mv simutrans/pak $RPM_BUILD_ROOT/usr/share/simutrans
mv simutrans/config $RPM_BUILD_ROOT/usr/share/simutrans
mv simutrans/font $RPM_BUILD_ROOT/usr/share/simutrans
mv simutrans/music $RPM_BUILD_ROOT/usr/share/simutrans
mv simutrans/text $RPM_BUILD_ROOT/usr/share/simutrans

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%files data
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/simutrans
%{_datadir}/simutrans/*

%changelog
* Fri Sep 18 2009 - Milan Jurik
- Initial version
