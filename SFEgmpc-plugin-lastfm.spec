%include Solaris.inc
%define pluginname lastfm
%define plugindownloadname last-fm
%include base.inc
%use gmpcplugin = gmpc-plugin.spec

Name:			SFEgmpc-plugin-%{pluginname}
Summary:                gmpc-%{pluginname} - fetch artist images from last.fm
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
%dir %attr (0755, root, sys) %{_prefix}
%{_libdir}/gmpc/plugins/*.so
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%attr (0755, root, other) %{_datadir}/locale/*


%changelog
* Wed Oct  6 2010 - Alex Viskovatoff
- Update to 0.20.0, fixing packaging and making it last-fm
* Sat Feb 21 2009 - Thomas Wagner
- add plugindownloadname to have base-specs/gmpc-plugin.spec download the correct files and leave out the "dot" in the package name
- add (Build-)Requires: SFEgmpc(-devel) (moved from base-specs/gmpc-plugin.spec)
- removed %doc from %files (usually no docs contained in plugins)
* Sun Jan 25 2009 - Thomas Wagner
- make it last.fm
* Sun Dec 02 2007 - Thomas Wagner
- rework into base-spec
- bump to 0.15.5.0
