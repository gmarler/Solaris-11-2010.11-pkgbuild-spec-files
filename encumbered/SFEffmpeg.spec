#
# spec file for package SFEffmpeg
#
# includes module(s): FFmpeg
#

%include Solaris.inc

%define SUNWlibsdl %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

%define cc_is_gcc 1

%if %arch_sse2
%define arch_opt --cpu=i686 --enable-mmx --enable-mmx2
%include x86_sse2.inc
%use ffmpeg_sse2 = ffmpeg.spec
%endif

%ifarch sparc
%define arch_opt --disable-optimizations
%endif

%ifarch i386
%define arch_opt
%endif

%include base.inc
%use ffmpeg = ffmpeg.spec

Name:                    SFEffmpeg
Summary:                 %{ffmpeg.summary}
Version:                 %{ffmpeg.version}
URL:                     %{ffmpeg.url}
Group:		Libraries/Multimedia

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Autoreqprov:             on

%include default-depend.inc
BuildRequires: SUNWtexi
BuildRequires: SUNWperl584usr
BuildRequires: SUNWxwinc
Requires: SUNWxwrtl
Requires: SUNWzlib
%if %SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%else
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%endif
BuildRequires: SFElibgsm-devel
Requires: SFElibgsm
BuildRequires: SFExvid-devel
Requires: SFExvid
BuildRequires: SFElibx264-devel
Requires: SFElibx264
BuildRequires: SFEfaad2-devel
Requires: SFEfaad2
BuildRequires: SFEfaac-devel
Requires: SFEfaac
BuildRequires: SFElame-devel
Requires: SFElame
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWogg-vorbis
BuildRequires: SUNWlibtheora-devel
Requires: SUNWlibtheora
BuildRequires: SUNWspeex-devel
Requires: SUNWspeex
BuildRequires: SFEopencore-amr-devel
Requires: SFEopencore-amr
BuildRequires: SUNWgsed
BuildRequires: SFEopenjpeg-devel
Requires: SFEopenjpeg
BuildRequires: SFElibschroedinger-devel
Requires: SFElibschroedinger

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version

%if %arch_sse2
mkdir %name-%version/%sse2_arch
%ffmpeg_sse2.prep -d %name-%version/%sse2_arch
%endif

mkdir %name-%version/%base_arch
%ffmpeg.prep -d %name-%version/%base_arch


%build
%if %arch_sse2
%ffmpeg_sse2.build -d %name-%version/%sse2_arch
%endif

%ffmpeg.build -d %name-%version/%base_arch


%install
rm -rf $RPM_BUILD_ROOT

%if %arch_sse2
%ffmpeg_sse2.install -d %name-%version/%sse2_arch
%endif

%ffmpeg.install -d %name-%version/%base_arch
mkdir $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
mv $RPM_BUILD_ROOT%{_bindir}/ffserver $RPM_BUILD_ROOT%{_bindir}/%{base_isa}/
cd $RPM_BUILD_ROOT%{_bindir} && ln -s ../lib/isaexec ffserver
mv $RPM_BUILD_ROOT%{_bindir}/ffplay $RPM_BUILD_ROOT%{_bindir}/%{base_isa}/
cd $RPM_BUILD_ROOT%{_bindir} && ln -s ../lib/isaexec ffplay
mv $RPM_BUILD_ROOT%{_bindir}/ffmpeg $RPM_BUILD_ROOT%{_bindir}/%{base_isa}/
cd $RPM_BUILD_ROOT%{_bindir} && ln -s ../lib/isaexec ffmpeg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%if %can_isaexec
%{_bindir}/%{base_isa}/*
%if %arch_sse2
%{_bindir}/%{sse2_arch}/*
%endif
%hard %{_bindir}/ffserver
%hard %{_bindir}/ffplay
%hard %{_bindir}/ffmpeg
%hard %{_bindir}/ffprobe
%else
%{_bindir}/*
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%if %arch_sse2
%dir %attr (0755, root, bin) %{_libdir}/%{sse2_arch}
%{_libdir}/%{sse2_arch}/lib*.so*
%endif
%dir %attr (0755, root, sys) %dir %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/ffmpeg
%{_datadir}/ffmpeg/*.ffpreset
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%if %arch_sse2
%dir %attr (0755, root, other) %{_libdir}/%{sse2_arch}/pkgconfig
%{_libdir}/%{sse2_arch}/pkgconfig/*.pc
%endif
%{_libdir}/ffmpeg
%if %arch_sse2
%{_libdir}/%{sse2_arch}/ffmpeg
%endif
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/libavutil
%{_includedir}/libavcodec
%{_includedir}/libavfilter
%{_includedir}/libavformat
%{_includedir}/libavdevice
%{_includedir}/libpostproc
%{_includedir}/libswscale

%changelog
* Mon Jan 24 2011 - Alex Viskovatoff
- Add missing build dependency
* Wed Jun 16 2010 - Milan Jurik
- update to 0.6
- remove older amr codecs, add libschroedinger and openjpeg
- remove mlib because it is broken now
- remove Solaris V4L2 support, more work needed
* Tue Apr 06 2010 - Milan Jurik
- missing perl build dependency (pod2man)
* Sun Mar 07 2010 - Milan Jurik
- replace amrXX for opencore implementation
* Tue Sep 08 2009 - Milan Jurik
- amrXX optional
- improved multiarch support (64-bit not done because of missing SUNW libraries)
* Mon Mar 16 2009 - Milan Jurik
- version 0.5
* Fri Jun 13 2008 - trisk@acm.jhu.edu
- New spec for base-spec
