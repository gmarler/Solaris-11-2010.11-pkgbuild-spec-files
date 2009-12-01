#
# spec file for package SFElibx264
#
# includes module(s): libx264
#

%include Solaris.inc

%define cc_is_gcc 1 
%ifarch amd64 sparcv9
%include arch64.inc
%use libx264_64 = libx264.spec
%endif

%if %arch_sse2
%define arch_opt --cpu=i686 --enable-mmx --enable-mmx2
%include x86_sse2.inc
%define arch_ldadd
%use libx264_sse2 = libx264.spec
%endif

%include base.inc
%use libx264 = libx264.spec

Name:                    SFElibx264
Summary:                 %{libx264.summary}
Version:                 %{libx264.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEyasm

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
%libx264_64.prep -d %name-%version/%_arch64
%endif

%if %arch_sse2
mkdir %name-%version/%sse2_arch
%libx264_sse2.prep -d %name-%version/%sse2_arch
%endif

mkdir %name-%version/%{base_arch}
%libx264.prep -d %name-%version/%{base_arch}


%build
%ifarch amd64 sparcv9
%libx264_64.build -d %name-%version/%_arch64
%endif

%if %arch_sse2
%libx264_sse2.build -d %name-%version/%sse2_arch
%endif

%libx264.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libx264_64.install -d %name-%version/%_arch64
%endif

%if %arch_sse2
%libx264_sse2.install -d %name-%version/%sse2_arch
%endif

%libx264.install -d %name-%version/%{base_arch}
find $RPM_BUILD_ROOT%{_libdir} -name \*.la -exec rm {} \;
mkdir $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
mv $RPM_BUILD_ROOT%{_bindir}/x264  $RPM_BUILD_ROOT%{_bindir}/%{base_isa}/
cd $RPM_BUILD_ROOT%{_bindir} && ln -s ../lib/isaexec x264


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%if %can_isaexec
%ifarch amd64 sparcv9
%{_bindir}/%{_arch64}/*
%endif
%{_bindir}/%{base_isa}/*
%if %arch_sse2
%{_bindir}/%{sse2_arch}/*
%endif
%hard %{_bindir}/x264
%else
%{_bindir}/*
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
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
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%if %arch_sse2
%dir %attr (0755, root, other) %{_libdir}/%{sse2_arch}/pkgconfig
%{_libdir}/%{sse2_arch}/pkgconfig/*
%endif


%changelog
* Sat Nov 28 2009 - Albert Lee <trisk@opensolaris.org>
- Remove GPAC dependency
* Tue Sep 8 2009 - Milan Jurik
- multiarch support
* Mon Mar 16 2009 - andras.barna@gmail.com
- Add patch7
* Sun Mar 15 2009 - Milan Jurik
- the latest snapshot
* Mon Jun 30 2008 - andras.barna@gmail.com
- Force SFWgcc
* Fri May 23 2008 - michal.bielicki <at> voiceworks.pl
- h26x chokes on optflags, fix by Giles Dauphin
* tue Jan 08 2008 - moinak.ghosh@sun.com
- Build with gcc and enable C99FEATURES.
* Tue Nov 20 2007 - daymobrew@users.sourceforge.net
- Bump to 20071119 and add Url.
* Sun Aug 12 2007 - dougs@truemail.co.th
- Added SFEgpac as Required
* Fri Aug  3 2007 - dougs@truemail.co.th
- initial version
