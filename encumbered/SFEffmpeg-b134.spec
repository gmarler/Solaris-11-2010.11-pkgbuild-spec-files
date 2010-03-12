#
# spec file for package SFEffmpeg
#
# includes module(s): FFmpeg
#

%include Solaris.inc

%define SUNWlibsdl %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)
%define with_amrnb %(/usr/bin/pkginfo -q SFEamrnb && echo 1 || echo 0)
%define with_amrwb %(/usr/bin/pkginfo -q SFEamrwb && echo 1 || echo 0)

%define cc_is_gcc 1

#%if %arch_sse2
#%define arch_opt --cpu=i686 --enable-mmx --enable-mmx2
#%include x86_sse2.inc
#%use ffmpeg_sse2 = ffmpeg.spec
#%endif

%ifarch sparc
%define arch_opt --enable-mlib
%endif

#%ifarch i386
%ifarch i386 amd64
%define arch_opt --disable-mmx --disable-mmx2
%endif

%include base.inc
%use ffmpeg = ffmpeg.spec

Name:                    SFEffmpeg
Summary:                 %{ffmpeg.summary}
Version:                 %{ffmpeg.version}
URL:                     %{ffmpeg.url}

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Autoreqprov:             on

%include default-depend.inc
BuildRequires: SUNWtexi
%ifarch sparc
BuildRequires: SUNWmlibh
Requires: SUNWmlib
%endif
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
%if %with_amrnb
Requires: SFEamrnb
BuildRequires: SFEamrnb-devel
%endif
%if %with_amrwb
Requires: SFEamrwb
BuildRequires: SFEamrwb-devel
%endif
BuildRequires: SFElame-devel
Requires: SFElame
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWogg-vorbis
BuildRequires: SUNWlibtheora-devel
Requires: SUNWlibtheora
BuildRequires: SUNWspeex-devel
Requires: SUNWspeex

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version

#%if %arch_sse2
#mkdir %name-%version/%sse2_arch
#%ffmpeg_sse2.prep -d %name-%version/%sse2_arch
#%endif

mkdir %name-%version/%base_arch
%ffmpeg.prep -d %name-%version/%base_arch


%build
#%if %arch_sse2
#%ffmpeg_sse2.build -d %name-%version/%sse2_arch
#%endif

%ffmpeg.build -d %name-%version/%base_arch


%install
rm -rf $RPM_BUILD_ROOT

#%if %arch_sse2
#%ffmpeg_sse2.install -d %name-%version/%sse2_arch
#%endif

%ffmpeg.install -d %name-%version/%base_arch
mkdir $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
mv $RPM_BUILD_ROOT%{_bindir}/ffserver $RPM_BUILD_ROOT%{_bindir}/%{base_isa}/
#cd $RPM_BUILD_ROOT%{_bindir} && ln -s ../lib/isaexec ffserver
cd $RPM_BUILD_ROOT%{_bindir} && cp -p  /usr/lib/isaexec ffserver
mv $RPM_BUILD_ROOT%{_bindir}/ffplay $RPM_BUILD_ROOT%{_bindir}/%{base_isa}/
#cd $RPM_BUILD_ROOT%{_bindir} && ln -s ../lib/isaexec ffplay
cd $RPM_BUILD_ROOT%{_bindir} && cp -p /usr/lib/isaexec ffplay
mv $RPM_BUILD_ROOT%{_bindir}/ffmpeg $RPM_BUILD_ROOT%{_bindir}/%{base_isa}/
#cd $RPM_BUILD_ROOT%{_bindir} && ln -s ../lib/isaexec ffmpeg
cd $RPM_BUILD_ROOT%{_bindir} && cp -p /usr/lib/isaexec ffmpeg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%if %can_isaexec
%{_bindir}/%{base_isa}/*
#%if %arch_sse2
#%{_bindir}/%{sse2_arch}/*
#%endif
%hard %{_bindir}/ffserver
%hard %{_bindir}/ffplay
%hard %{_bindir}/ffmpeg
%else
%{_bindir}/*
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
#%if %arch_sse2
#%dir %attr (0755, root, bin) %{_libdir}/%{sse2_arch}
#%{_libdir}/%{sse2_arch}/lib*.so*
#%endif
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
#%if %arch_sse2
#%dir %attr (0755, root, other) %{_libdir}/%{sse2_arch}/pkgconfig
#%{_libdir}/%{sse2_arch}/pkgconfig/*.pc
#%endif
%{_libdir}/ffmpeg
#%if %arch_sse2
#%{_libdir}/%{sse2_arch}/ffmpeg
#%endif
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/libavutil
%{_includedir}/libavcodec
%{_includedir}/libavfilter
%{_includedir}/libavformat
%{_includedir}/libavdevice
%{_includedir}/libpostproc
%{_includedir}/libswscale

%changelog
* Mar 2010 - Gilles dauphin
- make it generic, --libdir=/usr/SFE/lib/pentium_pro+mmx is annoying
* Tue Sep 8 2009 - Milan Jurik
- amrXX optional
- improved multiarch support (64-bit not done because of missing SUNW libraries)
* Mon Mar 16 2009 - Milan Jurik
- version 0.5
* Fri Jun 13 2008 - trisk@acm.jhu.edu
- New spec for base-spec
