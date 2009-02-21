%include Solaris.inc
%define pluginname lastfm
%define plugindownloadname last.fm
%include base.inc
%use gmpcplugin = gmpc-plugin.spec

Name:			SFEgmpc-plugin-%{pluginname}
Summary:                gmpc-%{pluginname} - fetch artist images from last.fm  - plugin for gmpc
# Version e.g. 0.15.5.0, note: gmpcplugin.gmpcmainversion is 0.15.5
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
#%doc README ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gmpc
%dir %attr (0755, root, other) %{_datadir}/gmpc/plugins
%{_datadir}/gmpc/plugins/*


%changelog
* Sat Feb 21 2009 - Thomas Wagner
- add plugindownloadname to have base-specs/gmpc-plugin.spec download the correct files and leave out the "dot" in the package name
- add (Build-)Requires: SFEgmpc(-devel) (moved from base-specs/gmpc-plugin.spec)
- removed %doc from %files (usually no docs contained in plugins)
* Sun Jan 25 2009 - Thomas Wagner
- make it last.fm
* Sun Dec 02 2007 - Thomas Wagner
- rework into base-spec
- bump to 0.15.5.0
