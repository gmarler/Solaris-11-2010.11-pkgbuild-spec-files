#
# spec file for package SFEazureus
#
# includes module(s): azureus
#
%include Solaris.inc
%define _desktopdir %{_datadir}/applications
%define _pixmapsdir %{_datadir}/pixmaps

%define src_name Vuze
%define src_ver 4.1.0.0
%define src_url http://%{sf_mirror}/azureus

Name:		SFEazureus
Summary:	Azureus - Java BitTorrent client
Version:	%{src_ver}
License:	GPL
Group:		X11/Applications/Networking
Source:		%{src_url}/%{src_name}_%{src_ver}_linux.tar.bz2
Source1:	azureus.png
Source2:	azureus.desktop
Source3:	azureus.sh
Patch1:		azureus-01-startscript.diff
URL:		http://azureus.sourceforge.net/
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
#Requires: SFEswt

%prep
%setup -q -c -n %{name}-%{version}
( cd vuze && 
%patch1 -p0
)
%build

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/Azureus
install -d $RPM_BUILD_ROOT%{_pixmapsdir}
install -d $RPM_BUILD_ROOT%{_desktopdir}
install -d $RPM_BUILD_ROOT%{_bindir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}

( cd vuze && cp -rp * $RPM_BUILD_ROOT%{_datadir}/Azureus/ )
ln -s ../share/Azureus/azureus $RPM_BUILD_ROOT%{_bindir}/azureus

rm -f $RPM_BUILD_ROOT%{_datadir}/Azureus/swt.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%attr(755,root,bin) %{_bindir}
%dir %attr(755,root,sys) %{_datadir}
#%dir %attr(755,root,sys) %{_datadir}/Azureus/plugins
#%dir %attr(755,root,sys) %{_datadir}/Azureus/plugins/azplugins
#%dir %attr(755,root,sys) %{_datadir}/Azureus/plugins/azrating
#%dir %attr(755,root,sys) %{_datadir}/Azureus/plugins/azupdater
#%dir %attr(755,root,sys) %{_datadir}/Azureus/plugins/azupnpav
%dir %attr(755,root,other) %{_desktopdir}
%{_desktopdir}/azureus.desktop
%dir %attr(755,root,other) %{_pixmapsdir}
%{_pixmapsdir}/azureus.png

%{_datadir}/Azureus/*
#%{_datadir}/Azureus/plugins/azplugins/*
#%{_datadir}/Azureus/plugins/azrating/*
#%{_datadir}/Azureus/plugins/azupdater/*
#%{_datadir}/Azureus/plugins/azupnpav/*

%changelog
* Apr 2010 - Gilles Dauphin
- swt is in B134
* Mon Feb 02 2008 - alfred.peng@sun.com
- Bump to version 4.1.0.0.
* Sun Oct 12 2008 - sobotkap@gmail.com
- Bump to version 3.1.1.0
* Fri Jun 20 2008 - river@wikimedia.org
- 3.1.0.0
- Use SFEswt instead of SFEeclipse
- Use binary instead of building from source
* Sat Dec 22 2007 - wickedwicky@users.sourceforge.net
- Add BuildRequires: SUNWgnome-common-devel
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Set CLASSPATH to try to get it to build.
* Sat Sep  8 2007 - dougs@truemail.co.th
- Initial version
