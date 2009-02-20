#
# spec file for package jack
#
# includes module(s): jack
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use jack64 = jack.spec
%endif

%include base.inc
%use jack = jack.spec

%define SFEdoxygen      %(/usr/bin/pkginfo -q SFEdoxygen && echo 1 || echo 0)
%define SFElibsndfile   %(/usr/bin/pkginfo -q SFElibsndfile && echo 1 || echo 0)

Name:		SFEjack
Summary:	%{jack.summary}
Version:	%{jack.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %SFElibsndfile
BuildRequires:	SFElibsndfile-devel
Requires:	SFElibsndfile
%else
BuildRequires:	SUNWlibsndfile
Requires:	SUNWlibsndfile
%endif

Requires:	oss

%package devel
Summary:         %{summary} - development files
SUNW_BaseDir:    %{_basedir}
%include default-depend.inc
Requires: %name

%if %SFEdoxygen
%package doc
Summary:                 %{summary} - Documentation
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%jack64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%jack.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%jack64.build -d %name-%version/%_arch64
%endif

%jack.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%jack64.install -d %name-%version/%_arch64
%endif

%jack.install -d %name-%version/%{base_arch}

%if %SFEdoxygen
  mkdir -p $RPM_BUILD_ROOT%{_docdir}    
  mv $RPM_BUILD_ROOT%{_datadir}/jack-audio-connection-kit $RPM_BUILD_ROOT%{_docdir}
%else
  rm -rf $RPM_BUILD_ROOT%{_datadir}/jack-audio-connection-kit
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/jack*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/jack
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/jack*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/jack
%endif

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%if %SFEdoxygen
%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%endif

%changelog
* Tue Feb 17 2009 - Thomas Wagner
- make (Build-)Requires conditional SUNWlibsndfile|SFElibsndfile(-devel)
* Tue Aug 28 2007 - dougs@truemail.co.th
- Added doc package if doxygen is installed
* Mon Aug 13 2007 - dougs@truemail.co.th
- Added 64bit build
* Sun Aug 12 2007 - dougs@truemail.co.th
- Initial version
