#
# spec file for package SFEfluidsynth
#
# includes module(s): fluidsynth
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use fluidsynth_64 = fluidsynth.spec
%endif

%include base.inc
%use fluidsynth = fluidsynth.spec

Name:		SFEfluidsynth
Summary:	%{fluidsynth.summary}
Version:	%{fluidsynth.version}
License:	%{fluidsynth.license}
URL:		%{fluidsynth.url}
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
FluidSynth is a real-time software synthesizer based on the SoundFont
2 specifications. FluidSynth can read MIDI events from MIDI input
devices and render them to audio devices using SoundFont files to
define the instrument sounds. It can also play MIDI files and supports
real time effect control via SoundFont modulators and MIDI
controls. FluidSynth can be interfaced to other programs in different
ways, including linking as a shared library.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%description devel
FluidSynth is a real-time software synthesizer based on the SoundFont
2 specifications. FluidSynth can read MIDI events from MIDI input
devices and render them to audio devices using SoundFont files to
define the instrument sounds. It can also play MIDI files and supports
real time effect control via SoundFont modulators and MIDI
controls. FluidSynth can be interfaced to other programs in different
ways, including linking as a shared library.

This package contains libraries and includes for building applications
with FluidSynth support.

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%fluidsynth_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%fluidsynth.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%fluidsynth_64.build -d %name-%version/%_arch64
%endif

%fluidsynth.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%fluidsynth_64.install -d %name-%version/%_arch64
%endif

%fluidsynth.install -d %name-%version/%{base_arch}

%clean
if [ -d $RPM_BUILD_ROOT ]; then rm -rf $RPM_BUILD_ROOT; fi

%files
%defattr (-, root, bin)
%{_bindir}/fluidsynth
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/man1

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


%changelog
* Wed May 05 2010 Milan Jurik
- Initial import to SFE
* Mon Aug 25 2003 Josh Green <jgreen@users.sourceforge.net>
- Created initial fluidsynth.spec.in
