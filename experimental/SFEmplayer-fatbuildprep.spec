#
# spec file for building a full features mplayer-snap from SVN
#

%include osdistro.inc


#NOTE auto-install of the OS provided packages on an IPS system does *not* work currently


#place packages to be build before mplayer-snap. mplayer-snap
#does find them and use them if they are present before, else skip.

%define requiresforfatbuild experimental/SFEmplayer-fatbuildprep.spec SUNWlibsndfile SFEfaad2 SFElibfribidi SFEladspa SFEopenal SFEliba52 SFElame SFEtwolame SFElibmad SFElibmpcdec SFExvid SFElibx264 SFEopenjpeg SFEgiflib SFEliveMedia SFElibcdio SFElibcdio-devel

#supplement (do not list those, who are already listed in SFEmplayer-snap iteself
%define requiresforfatbuildsupplement SUNWsmbau SUNWgnome-audio SUNWgscr

# place specs excluded from above *here* and do not delete them.
#
# example for paused: SFElibsndfile SFEfaad


#script resolveipspackages is part of "bootstrap-sfe-latest-os20nn" and "bootstrap-sfe-testing-os20nn"
#ealybird is a dummy. This step just installs packages from the present IPS repo on this system
%define earlybird $( /opt/jdsbld/bin/resolveipspackages %{requiresforfatbuild} %{requiresforfatbuildsupplement} experimental/SFEmplayer-snap )



#SFElame.spec
#SFEliba52.spec
#SFElibavc1394.spec
#SFElibdts.spec
#SFElibdv.spec
#SFElibdvbpsi.spec
#SFElibdvdcss.spec
#SFElibfame.spec
#SFElibgsm.spec
#SFElibiec61883.spec
#SFElibmad.spec
#SFElibmms.spec
#SFElibmpcdec.spec
#SFElibmpeg2.spec
#SFElibnjb.spec
#SFElibquicktime.spec
#SFElibraw1394.spec
#SFElibx264.spec
#SFEmjpegtools.spec
#SFEmpd.spec
#SFEmpg321.spec
#SFEmpgtx.spec
#SFEmplayer-codecs.spec
#SFEmplayer-snap.spec
#SFEmplayer.spec
#SFEmplayerplug-in.spec
#SFEnntpcached.spec
#SFEogle.spec
#SFEopencore-amr.spec
#SFEsmpeg.spec
#SFEsox.spec
#SFEswfdec.spec
#SFEtwolame.spec
#SFEvice.spec
#SFEvlc-b134.spec
#SFEvlc.spec
#SFEvnc2swf.spec
#SFExine-lib-b134.spec
#SFExine-lib.spec
#SFExine-ui.spec
#SFExmms1-oss4.spec
#SFExmms1-scrobbler.spec
#SFExmms1.spec
#SFExmms2.spec
#SFExvid-b134.spec
#SFExvid.spec
#SFEy4mscaler.spec


Name:                    SFEmplayer-fat
Summary:                 mplayer-fat - dummy spec file to BuildRequire tons of prerequisites and then also requires SFEmplayer-snap
Version:                 0.1


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

#you really *want* the compilers newer the 4.3.3, codecs might crash
#best to use most fresh compilers like that:
#pfexec uninstall gcc4
#pfexec uninstall SFEgcc
#
#first make fresh gcc compiler:
#pkgtool --download --autodeps build experimental/SFEgcc-4.5.1.spec  (or SFEgcc-4.4.5.spec)
#then make fatbuild...
#pkgtool --download --autodeps --interactive build experimental/SFEmplayer-fatbuildprep.spec
BuildRequires: SFEgcc
Requires:      SFEgccruntime

#:. s/ /\rBuildRequires: /g
#
BuildRequires: SFEfaad2
BuildRequires: SFElibfribidi
BuildRequires: SFEladspa
BuildRequires: SFEopenal
BuildRequires: SFEliba52
BuildRequires: SFElame
BuildRequires: SFEtwolame
BuildRequires: SFElibmad
BuildRequires: SFElibmpcdec
BuildRequires: SFExvid
BuildRequires: SFElibx264
BuildRequires: SFEopenjpeg
BuildRequires: SFEgiflib
BuildRequires: SFEliveMedia
BuildRequires: SFElibcdio
BuildRequires: SFElibcdio-devel
BuildRequires: SFEmplayer-snap

%prep

echo %earlybird > /tmp/%{name}-earlybird-$$.out

%build

%install

%clean
rm -rf $RPM_BUILD_ROOT

%files


%changelog
* Fri Nov 05 2010  - Thomas Wagner
- broken is autoinstall of OS provided required packages
- added SFEmplayer-snap itself to get it build
- SFEmplayer-fatbuild empty package might easily be removed afterwards, pfexec pkg uninstall SFEmplayer-fatbuildprep
- experimental dummy script to require other specfiles/pacakges and install
  OS packages needed
- NOTE: use most fresh gcc compiler to get best results
- usage: pkgtool --download --autodeps               build SFEmplayer-fatbuildprep.spec
or
- NOTE: use most fresh gcc compiler to get best results
- usage: pkgtool --download --autodeps --interactive build experimental/SFEmplayer-fatbuildprep.spec
