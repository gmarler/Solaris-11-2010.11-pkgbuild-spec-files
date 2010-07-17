#
# spec file for package SFEgosm
#
# includes module(s): gosm
#
%include Solaris.inc

Name:           SFEgosm
Summary:        gosm let's you browse the free map-data from the Openstreetmap-project
Version:        0.0.9
Source:         %{sf_download}/gosm/0.09/gosm.%{version}.tar.gz
Patch1:		gosm-01-makefile.diff
Patch2:		gosm-02-init.diff
URL:            http://gosm.sourceforge.net/
License:	GPLv3
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWgnome-common-devel
Requires:	SFEwebkitgtk
BuildRequires:	SFEwebkitgtk-devel
Requires:	SUNWcurl
BuildRequires:	SUNWcurl

%prep
%setup -q -n gosm
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
cp gosm $RPM_BUILD_ROOT/%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/gosm

%changelog
* Sat Jul 17 2010 - Milan Jurik
- Initial spec file
