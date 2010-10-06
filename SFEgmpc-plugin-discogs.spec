%include Solaris.inc
%define pluginname discogs
%include base.inc
%use gmpcplugin = gmpc-plugin.spec

Name:			SFEgmpc-plugin-%{pluginname}
Summary:                gmpc-%{pluginname} - searches www.discogs.com for images of artists and albums
# Version e.g. 0.20.0
Version:                %{gmpcplugin.version}
 
BuildRequires: SFEgmpc-devel
Requires: SFEgmpc

%prep
%gmpcplugin.prep
 
%build
%gmpcplugin.build
 
%install
%gmpcplugin.install

%clean
%gmpcplugin.clean

%files
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%{_libdir}/gmpc/plugins/*.so
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%attr (0755, root, other) %{_datadir}/locale/*


%changelog
* Wed Oct  6 2010 - Alex Viskovatoff
- *new* - based on SFEgmpc-plugin-albumview.spec
