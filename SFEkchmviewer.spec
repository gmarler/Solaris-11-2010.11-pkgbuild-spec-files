#
# spec file for package SFEkchmviewer
#
# includes module: kchmviewer
#

%include Solaris.inc
%define srcname kchmviewer

Name:		SFEkchmviewer
Summary:	CHM help file viewer based on Qt
URL:		http://www.kchmviewer.net
Vendor:		George Yunaev
Version:	5.2
License:	GPL
Source:		http://downloads.sourceforge.net/%srcname/%srcname-%version.tar.gz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires: SUNWgmake
BuildRequires: SUNWgnu-coreutils
BuildRequires: SUNWgtar
BuildRequires: SFEqt47-devel
BuildRequires: SFEchmlib

Requires: SFEqt47
Requires: SFEchmlib
Requires: SUNWzlib


%prep
gtar -xzf %SOURCE0
rm -fr %srcname-%version
mv build-%version %srcname-%version

%build
cd %srcname-%version

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi
export PATH=$PATH:/usr/stdcxx/bin
export QMAKESPEC=solaris-cc-stdcxx
export QTDIR=/usr/stdcxx

qmake
gmake -j$CPUS PREFIX=%_basedir

%install
rm -rf $RPM_BUILD_ROOT

ginstall -d $RPM_BUILD_ROOT/%_bindir
ginstall -t $RPM_BUILD_ROOT/%_bindir %srcname-%version/bin/kchmviewer

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir/%srcname


%changelog
* Fri Jan 28 2011 - Alex Viskovatoff
- Accommodate to Qt being in /usr/stdcxx
* Mon Jan 24 2011 - Alex Viskovatoff
- Define QMAKESPEC
* Sat Dec 11 2010 - Alex Viskovatoff
- Initial spec
