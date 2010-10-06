#
# spec file for package SFElibid3tag
#
# includes module(s): libid3tag
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libid3tag_64 = libid3tag.spec
%endif

%include base.inc
%use libid3tag = libid3tag.spec

Name:                    SFElibid3tag
Summary:                 %{libid3tag.summary}
Version:                 %{libid3tag.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:     library/zlib

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libid3tag_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libid3tag.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%libid3tag_64.build -d %name-%version/%_arch64
%endif

%libid3tag.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libid3tag_64.install -d %name-%version/%_arch64
%endif

%libid3tag.install -d %name-%version/%{base_arch}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/id3tag.pc
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/id3tag.pc
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sun Sep 26 2010 - Alex Viskovatoff
- multiarch support, based on SFElibmad.spec
* Wed Jul  5 2006 - laca@sun.com
- rename to SFElibid3tag
- delete unnecessary env variables and dependencies
* Thu Apr  6 2006 - damien.carbery@sun.com
- Move Build/Requires to be listed under base package to be useful.
* Thu Mar 16 2006 - damien.carbery@sun.com
- Correct URL and version.
* Thu Mar 09 2006 - brian.cameron@sun.com
- Created,  
