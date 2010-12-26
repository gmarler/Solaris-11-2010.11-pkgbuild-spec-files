#
# spec file for package: timidity++
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define src_name TiMidity++

Name:		SFEtimidity
Summary:	Software sound renderer (MIDI sequencer, MOD player)
Group:		Audio
Version:	2.13.2
License:	GPLv2
Source:		%{sf_download}/timidity/%{src_name}/%{src_name}-2.13.2/%{src_name}-%{version}.tar.gz
Patch1:		timidity-01-sunstudio.diff
Patch2:		timidity-02-inttypes.diff
Patch3:		timidity-10-freeinst.diff
URL:		http://timidity.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
SUNW_Basedir:	%{_prefix}

%include default-depend.inc
BuildRequires: SUNWaudh
BuildRequires: SUNWogg-vorbis
BuildRequires: SUNWxwinc
BuildRequires: SUNWxwplt
BuildRequires: SUNWxwrtl
BuildRequires: SUNWlibms
BuildRequires: SUNWmlib
BuildRequires: SUNWxorg-headers
BuildRequires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWgnome-audio-devel
BuildRequires: SUNWbtool
BuildRequires: SUNWgnu-coreutils
BuildRequires: SUNWfontconfig
BuildRequires: SUNWfreetype2
Requires: SUNWcslr
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWgnome-audio
Requires: SUNWgnome-base-libs
Requires: SUNWlexpt
Requires: SUNWlibmsr
Requires: SUNWmlib
Requires: SUNWogg-vorbis
Requires: SUNWpng
Requires: SUNWxorg-clientlibs
Requires: SUNWxwplt
Requires: SUNWxwrtl
Requires: SUNWzlibr
Requires: %{name}-root

%description
TiMidity++ is a very high quality software-only MIDI sequencer and MOD player. It uses sound fonts (GUS-compatible or SF2-compatible) to render MIDI files, which are not included in this package.

  * Plays MIDI files without any external MIDI instruments at all
  * Understands SMF, RCP/R36/G18/G36, MFI, RMI (MIDI)
  * Autodetects and supports GM/GS/XG MIDI
  * Understands MOD, XM, S3M, IT, 699, AMF, DSM, FAR, GDM,
    IMF, MED, MTM, STM, STX, ULT, UNI (MOD)
  * Does MOD to MIDI conversion (including playback)
  * Outputs audio into various audio file formats: WAV, au, AIFF,
    Ogg (Vorbis, FLAC, Speex)
  * Supports NAS, eSound, ARtS, JACK, ALSA and OSS drivers
  * Uses Gravis Ultrasound compatible patch files and SoundFont2 patch
    files as the voice data for MIDI instruments
  * Supports playing from archives (zip, lzh, tar...) and playing remote
    data from the network

%package root
SUNW_Basedir:	/
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir} \
	--with-default-path=%{_sysconfdir}/timidity \
	--mandir=%{_mandir} \
	--enable-audio=oss,sun,vorbis --enable-network \
	--enable-gtk --enable-spectrogram --with-x
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# Add documentation
mkdir -p %{buildroot}/%{_docdir}
install -m 0644 doc/C/FAQ %{buildroot}/%{_docdir}
install -m 0644 doc/C/README* %{buildroot}/%{_docdir}
install -m 0644 INSTALL %{buildroot}/%{_docdir}
install -m 0644 README %{buildroot}/%{_docdir}
install -m 0644 NEWS %{buildroot}/%{_docdir}

mkdir -p %{buildroot}/%{_datadir}/pixmaps
install -m 0644 interface/pixmaps/timidity.xpm \
    %{buildroot}/%{_datadir}/pixmaps

mkdir -p %{buildroot}/%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{src_name}.desktop << EOF
Version=1.0
Encoding=UTF-8
Name=TiMidity++
Comment=Software sound renderer (MIDI sequencer, MOD player)
Exec=/usr/bin/timidity -ig %U
Terminal=false
Type=Application
Icon=timidity
Categories=Application;AudioVideo;Audio;Player
StartupNotify=false
GenericName=
EOF

mkdir -p %{buildroot}/%{_sysconfdir}/timidity
touch %{buildroot}/%{_sysconfdir}/timidity/timidity.cfg

%clean
rm -rf %{buildroot}


%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%{_mandir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%files root
%defattr (-, root, sys)
%dir %{_sysconfdir}/timidity
%config %{_sysconfdir}/timidity/timidity.cfg

%changelog
* Sun Dec 26 2010 - Milan Jurik
- from jucr to SFE
* Fri Jul 31 2009 - milan.cermak@sun.com
- initial version
