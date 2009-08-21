#
# spec file for package SFElibmad
#
# includes module(s): libmad
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libmad_64 = libmad.spec
%endif

%include base.inc
%use libmad = libmad.spec

Name:                    SFElibmad
Summary:                 %{libmad.summary}
Version:                 %{libmad.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

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
%libmad_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libmad.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%libmad_64.build -d %name-%version/%_arch64
%endif

%libmad.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libmad_64.install -d %name-%version/%_arch64
%endif

%libmad.install -d %name-%version/%{base_arch}


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
%{_libdir}/pkgconfig/mad.pc
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/mad.pc
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri Aug 21 2009 - Milan Jurik
- multiarch support
* Thu Jul 30 2009 - oliver.mauras@gmail.com
- Add mad.pc to have a better detection for apps that needs libMAD
* Thu Jul 27 2006 - halton.huo@sun.com
- Correct Source url s/kend/kent
* Mon Jun 12 2006 - laca@sun.com
- renamed to SFElibmad
- changed to root:bin to follow other JDS pkgs.
- disable fpm when using sun studio, as the inline assembly syntax is different
  and breaks the build
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
