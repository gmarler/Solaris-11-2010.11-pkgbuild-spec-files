#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use libsamplerate64 = libsamplerate.spec
%endif

%include base.inc
%use libsamplerate = libsamplerate.spec

%define SFElibsndfile   %(/usr/bin/pkginfo -q SFElibsndfile && echo 1 || echo 0)

Name:                SFElibsamplerate
Summary:             %{libsamplerate.summary}
Version:             %{libsamplerate.version}
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#if build, examples will require libsndfile
%if %SFElibsndfile
BuildRequires: SFElibsndfile-devel
Requires: SFElibsndfile
#BuildConflicts: SUNWlibsndfile
Conflicts: SUNWlibsndfile
%else
BuildRequires:	SUNWlibsndfile
Requires:	SUNWlibsndfile
%endif

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
%libsamplerate64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libsamplerate.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%libsamplerate64.build -d %name-%version/%_arch64
%endif

%libsamplerate.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libsamplerate64.install -d %name-%version/%_arch64
%endif

%libsamplerate.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/sndfile-resample
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/sndfile-resample
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Fri Feb 20 2009 - Thomas Wagner
- add Conflicts: SUNWlibsndfile if SFElibsndfile if present (usually on older system)
* Tue Feb 17 2009 - Thomas Wagner
- make (Build-)Requires conditional SUNWlibsndfile|SFElibsndfile(-devel)
* Thu Sep 06 2007 - Thomas Wagner
- (Build)Requires on SFElibsndfile(-devel)
* Sun Aug 12 2007 - dougs@truemail.co.th
- Changed to build 64bit
* 20070522 Thomas Wagner
- Initial spec
