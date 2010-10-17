#
# spec file for package SFEmt-daapd
#
# includes module(s): mt-daapd
#
# # Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%use mtdaapd = mt-daapd.spec

Name:                    SFEmt-daapd
Summary:                 mt-daapd - firefly media server
Version:                 %{mtdaapd.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
# SMF manifest by Peter Woodman
# http://shortbus.org/bloggin/2008/10/22/making-a-manifest-for-smf/
Source1:                 mt-daapd.xml
 
%include default-depend.inc
Requires: SUNWgnu-dbm
Requires: SFElibid3tag
Requires: SFElibmad
BuildRequires: SUNWgmake
Requires: SUNWsqlite3
BuildRequires: SUNWsqlite3
# mt-daapd ships with an mDNS responder but its reportedly flaky
# let's use howl :D
Requires: SFEhowl
BuildRequires: SFEhowl-devel

%package root
Summary:                 %{summary} - root files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name


%prep
rm -rf %name-%version
mkdir %name-%version
%mtdaapd.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export CC=gcc
export CXX=g++
export CXXFLAGS="%{gcc_cxx_optflags}"
export CFLAGS="%optflags -std=c99"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"
export PERL_PATH=/usr/perl5/bin/perl
%mtdaapd.build -d %name-%version


%install
rm -rf $RPM_BUILD_ROOT
%mtdaapd.install -d %name-%version

# move file in /sbin to /bin
mv $RPM_BUILD_ROOT/usr/sbin $RPM_BUILD_ROOT/%{_bindir} 

# grab mt-daapd.conf
mkdir -p $RPM_BUILD_ROOT/etc
cp %{_builddir}/%name-%version/mt-daapd-%version/contrib/mt-daapd.conf $RPM_BUILD_ROOT/etc

# smf files
install -d $RPM_BUILD_ROOT/var/svc/manifest/system
install --mode=0444 %SOURCE1 $RPM_BUILD_ROOT/var/svc/manifest/system


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/mt-daapd

%files root
%defattr (-, root, sys)
%{_sysconfdir}/mt-daapd.conf
#%class(manifest) %attr(0444, root, sys)/var/svc/manifest/site/mt-daapd.xml
%attr (0444, root, sys) /var/svc/manifest/system/mt-daapd.xml


%changelog
* Fri Oct 01 2010 - jchoi42@pha.jhu.edu
- initial spec
