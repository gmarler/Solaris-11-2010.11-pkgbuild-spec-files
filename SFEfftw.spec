#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use fftw3_64 = fftw3.spec
%use fftw2_64 = fftw2.spec
%endif

%if %arch_sse2
%include x86_sse2.inc
%use fftw3_sse2 = fftw3.spec
%use fftw2_sse2 = fftw2.spec
%endif

%include base.inc

%use fftw3 = fftw3.spec
%use fftw2 = fftw2.spec

Name:                SFEfftw
Summary:             %{fftw3.summary}
Version:             %{fftw3.version}
URL:                 http://www.fftw.org/
License:             GPLv2
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:       SUNWtexi

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%fftw3_64.prep -d %name-%version/%_arch64
%fftw2_64.prep -d %name-%version/%_arch64
%endif

%if %arch_sse2
mkdir %name-%version/%sse2_arch
%fftw3_sse2.prep -d %name-%version/%{sse2_arch}
%fftw2_sse2.prep -d %name-%version/%{sse2_arch}
%endif

mkdir %name-%version/%{base_arch}
%fftw3.prep -d %name-%version/%{base_arch}
%fftw2.prep -d %name-%version/%{base_arch}

%build
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
export LD_OPTIONS="-64"
%fftw3_64.build -d %name-%version/%_arch64
%fftw2_64.build -d %name-%version/%_arch64
unset LD_OPTIONS
%endif

%if %arch_sse2
%fftw3_sse2.build -d %name-%version/%{sse2_arch}
%fftw2_sse2.build -d %name-%version/%{sse2_arch}
%endif

export options="--enable-float"
%fftw3.build -d %name-%version/%{base_arch}
%fftw3.install -d %name-%version/%{base_arch}
unset options
%fftw3.build -d %name-%version/%{base_arch}
%fftw2.build -d %name-%version/%{base_arch}

%install

%ifarch amd64 sparcv9
%fftw3_64.install -d %name-%version/%_arch64
%fftw2_64.install -d %name-%version/%_arch64
%endif

%if %arch_sse2
%fftw3_sse2.install -d %name-%version/%{sse2_arch}
%fftw2_sse2.install -d %name-%version/%{sse2_arch}
%endif

%fftw3.install -d %name-%version/%{base_arch}
%fftw2.install -d %name-%version/%{base_arch}

rm ${RPM_BUILD_ROOT}%{_datadir}/info/dir

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%if %arch_sse2
%dir %attr (0755, root, bin) %{_libdir}/%{sse2_arch}
%{_libdir}/%{sse2_arch}/lib*.so*
%endif


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif
%if %arch_sse2
%dir %attr (0755, root, other) %{_libdir}/%{sse2_arch}/pkgconfig
%{_libdir}/%{sse2_arch}/pkgconfig/*.pc
%endif

%changelog
* Wed May 05 2010 - Milan Jurik
- added missing build dependency
* Mon Jul 30 2007 - Doug Scott
- Added build of libfftw3f
* Mon Apr 23 2007 - Doug Scott
- Change to build version 2 and 3. Multi-isa build 
* Wed Sep 27 2006 - Eric Boutilier
- Initial spec
