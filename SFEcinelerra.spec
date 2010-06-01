#
# TODO:
# - build guicast as separate, shared library to use in xmovie,
#   mix2005 and cinelerra
# - get rid of bootstrap stuff:
#   https://init.linpro.no/pipermail/skolelinux.no/cinelerra/2004-April/001413.html
#
Summary:	Cinelerra - capturing, editing and production of audio/video material
#Summary(pl.UTF-8):	Cinelerra - nagrywanie, obróbka i produkcja materiału audio/video
Name:		cinelerra
Version:	4.1
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/heroines/%{name}-%{version}-src.tar.bz2
# Source0-md5:	e489693cf7ccc98c46cbcf8f751210c3
#Patch0:		%{name}-system-libs.patch
#Patch1:		%{name}-strip.patch
#Patch2:		%{name}-fontsdir.patch
#Patch3:		%{name}-locale_h.patch
#Patch4:		%{name}-guicast_bootstrap.patch
#Patch5:		%{name}-fix.patch
#Patch6:		%{name}-libpng.patch
URL:		http://www.heroinewarrior.com/cinelerra.php
#BuildRequires:	OpenEXR-devel >= 1.6.1
#BuildRequires:	OpenGL-GLU-devel
#BuildRequires:	OpenGL-devel >= 2.0
#BuildRequires:	alsa-lib-devel >= 1.0.8
#BuildRequires:	bzip2-devel
#BuildRequires:	esound-devel
#BuildRequires:	flac-devel >= 1.1.4
#BuildRequires:	freetype-devel >= 2.1.4
#BuildRequires:	lame-libs-devel >= 3.93.1
#BuildRequires:	libavc1394-devel >= 0.5.1
#BuildRequires:	libiec61883-devel >= 1.0.0
#BuildRequires:	libmpeg3-devel >= 1.8
#BuildRequires:	libraw1394-devel >= 1.2.0
#BuildRequires:	libsndfile-devel >= 1.0.11
#BuildRequires:	libstdc++-devel >= 5:3.2.2
#BuildRequires:	libtheora-devel >= 1.0-0.alpha4
#BuildRequires:	libtiff-devel >= 3.5.7
#BuildRequires:	libuuid-devel
#%ifarch %{ix86}
#BuildRequires:	nasm
#%endif
#BuildRequires:	quicktime4linux-devel >= 2.3
#BuildRequires:	xorg-lib-libX11-devel
#BuildRequires:	xorg-lib-libXext-devel
#BuildRequires:	xorg-lib-libXv-devel
#BuildRequires:	xorg-lib-libXxf86vm-devel
#Requires:	OpenEXR >= 1.6.1
#Requires:	alsa-lib >= 1.0.8
#Requires:	freetype >= 2.1.4
#Requires:	libavc1394 >= 0.5.1
#Requires:	libiec61883 >= 1.0.0
#Requires:	libmpeg3 >= 1.8
#Requires:	libraw1394 >= 1.2.0
#Requires:	libsndfile >= 1.0.11
#Requires:	libtheora >= 1.0-0.alpha4
#Requires:	quicktime4linux >= 2.3
#Obsoletes:	bcast
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

#%define		_noautostrip	.*/microtheme.plugin

%description
There are two types of moviegoers: producers who create new content,
going back over their content at future points for further refinement,
and consumers who want to acquire the content and watch it. Cinelerra
is not intended for consumers. Cinelerra has many features for
uncompressed content, high resolution processing, and compositing,
with very few shortcuts. Producers need these features because of the
need to retouch many generations of footage with alterations to the
format, which makes Cinelerra very complex.

Cinelerra was meant to be a Broadcast 2000 replacement.

#%description -l pl.UTF-8
#Są dwa rodzaje użytkowników zajmujących się filmami: producenci
#tworzący nowe filmy, wracający do nich w przyszłości w celu dalszego
#wygładzenia, oraz konsumenci, którzy chcą tylko zdobyć film i go
#obejrzeć. Cinelerra nie jest dla konsumentów. Program ma wiele
#możliwości do edycji nieskompresowanej zawartości, obróbki w wysokiej
#rozdzielczości oraz montażu, z bardzo małą liczbą skrótów. Producenci
#potrzebują tych możliwości ze względu na konieczność retuszowania oraz
#modyfikacji formatu, co czyni program bardzo złożonym.
#
#Cinelerra była tworzona z myślą o zastąpieniu programu Broadcast 2000.

%prep
%setup -q
#%patch0 -p1
#%patch1 -p1
#%patch2 -p1
#%patch3 -p1
#%patch4 -p1
#%patch5 -p1
#%patch6 -p0

# assume we have <linux/videodev2.h> and <linux/dvb/*> (present in llh)
#cat > hvirtual_config.h <<EOF
##define HAVE_VIDEO4LINUX2
##define HAVE_DVB
##define HAVE_GL
##define PACKAGE_STRING "cinelerra"
#EOF

#%{__rm} -r libmpeg3 quicktime \
#	thirdparty/{audiofile,esound,fftw-*,flac-*,freetype-*,ilmbase-*,libavc1394-*,libiec61883-*,libraw1394-*,libsndfile-*,libtheora-*,mjpegtools-*,openexr-*,tiff-*,uuid}
#

%build
#export CFLAGS="%{rpmcflags}"

make -f build/Makefile.toolame  GCC=gcc
make -C mpeg2enc CC=gcc
make -C mplexlo CC=gcc
make -C guicast GCC=gcc CC=g++
# cinelerra, defaulttheme and microtheme are stripped before running "bootstrap"
make -C cinelerra GCC=gcc  CC="g++" LINKER='g++ -o $(OUTPUT)'
make -C plugins CC="g++" 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/cinelerra}
cp -a bin/* $RPM_BUILD_ROOT%{_libdir}/cinelerra
mv $RPM_BUILD_ROOT{%{_libdir}/cinelerra,%{_bindir}}/cinelerra
rm -rf $RPM_BUILD_ROOT%{_libdir}/cinelerra/c_flags

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/{*.png,*.html,press} cinelerra/{CHANGELOG*,TODO}
%attr(755,root,root) %{_bindir}/cinelerra
%dir %{_libdir}/cinelerra
%attr(755,root,root) %{_libdir}/cinelerra/*.plugin

%define date	%(echo `LC_ALL="C" date +"%a %b %d %Y"`)
%changelog
* May 21 2010 Gilles dauphin
- import in SFE
*  PLD Team <feedback@pld-linux.org>
All persons listed below can be reached at <cvs_login>@pld-linux.org

$Log: cinelerra.spec,v $
Revision 1.39  2010/04/06 21:10:48  sparky
- BR: OpenGL-GLU-devel, bzip2-devel

Revision 1.38  2010/03/05 12:46:51  hawk
- updated to 4.1, added libpng 1.4 fix

Revision 1.37  2010/01/15 23:42:25  hawk
- release 4

Revision 1.36  2009/07/07 10:51:15  glen
- install and package files, leave stripping for rpmbuild scripts

Revision 1.35  2009/07/07 08:46:20  glen
- fix url and md4

Revision 1.34  2008/10/11 18:17:29  duddits
- rel. 3
- patch for ffmpeg >= 080930 added
- patch for 'fade error' added

Revision 1.33  2008/10/06 06:31:39  hawk
- release 2

Revision 1.32  2008/08/29 14:35:48  qboosh
- updated to 4
- updated system-libs,strip,fontsdir,fix patches
- added plugindir patch

Revision 1.31  2008/02/19 23:39:18  glen
- revert wordwrap by bad adapter

Revision 1.30  2008-01-13 12:18:45  qboosh
- R: OpenEXR, not -devel

Revision 1.29  2007-02-12 21:23:50  glen
- tabs in preamble

Revision 1.28  2007/02/12 00:48:42  baggins
- converted to UTF-8

Revision 1.27  2006/07/06 18:43:24  qboosh
- added fixes for make 3.81 to fix patch
- enabled DVB support
- switched to modular xorg

Revision 1.26  2006/07/05 10:19:25  qboosh
- updated to 2.1, updated system-libs,guicast_bootstrap patches, added fix patch

Revision 1.25  2006/06/13 19:25:11  hawk
- release 2
- updated TODO

Revision 1.24  2005/11/02 21:07:17  qboosh
- updated system-libs,guicast_bootstrap patches (!x86 fixes)
- removed EA - at least builds and starts on alpha (although very slowly...)
  needs checking on big-endians

Revision 1.23  2005/11/01 17:19:32  qboosh
- updated to 2.0
- updated system-libs,fontsdir patches, removed alpha,libsndfile1 patches

Revision 1.22  2005/10/30 12:19:30  arekm
- rel 4

Revision 1.21  2005/05/11 17:05:48  qboosh
- use x8664 macro

Revision 1.20  2005/03/29 07:20:23  ankry
- EA, rel. 3

Revision 1.19  2005/03/29 02:01:43  ankry
- rel. 2 to rebuild with ffmpeg-0.4.9-0.pre1.1

Revision 1.18  2004/09/13 09:16:21  jajcus
- trying to fix alpha/ppc/sparc build failure

Revision 1.17  2004/09/13 07:57:39  jajcus
- locale_h patch added, fixes AMD64 build

Revision 1.16  2004/08/22 20:42:16  qboosh
- updated to 1.2.1, updated system-libs,strip patches

Revision 1.15  2004/06/05 10:34:51  qboosh
- updated to 1.2.0, updated alpha,strip,system-libs patches

Revision 1.14  2004/04/11 01:27:27  qboosh
- Obsoletes: bcast

Revision 1.13  2004/03/08 21:13:52  qboosh
- updated to 1.1.9, updated fontsdir,libsndfile1 patches
- removed obsolete freetype patch

Revision 1.12  2003/11/12 23:16:11  qboosh
- 1.1.8, updated system-libs,libsndfile1,strip patches

Revision 1.11  2003/11/10 12:45:55  qboosh
- added alpha patch - now builds on alpha using gcc

Revision 1.10  2003/10/14 22:52:11  qboosh
- s/e2fsprogs-devel/libuuid-devel/
- BR: quicktime4linux-devel updated to >= 2.0.0
- added freetype patch to fix build titler plugin with ft 2.1.5
- release 2

Revision 1.9  2003/08/18 08:07:57  gotar
- mass commit: cosmetics (removed trailing white spaces)

Revision 1.8  2003/08/17 12:46:49  qboosh
- 1.1.7
- updated system-libs,libsndfile1,fontsdir patches
- removed obsolete lame patch

Revision 1.6  2003/07/18 23:30:28  qboosh
- up to 1.1.6
- updated libsndfile1 patch, removed both obsolete c++ patches

Revision 1.5  2003/05/26 16:24:47  malekith
- massive attack: adding Source-md5

Revision 1.4  2003/05/25 05:46:16  misi3k
- massive attack s/pld.org.pl/pld-linux.org/

Revision 1.3  2003/03/24 17:30:25  qboosh
- removed mpeg2 patch (not needed with libmpeg3 >= 1.5.0-2)
- changed system-libs patch to use only system quicktime headers (BR: 1.6.1-2)
- added lame patch to use system libmp3lame (contains lame frontend update)
- strip theme plugins before "bootstrap" (strip patch), the rest in install
- changed font search path to /usr/share/fonts (fontsdir patch)

Revision 1.2  2003/03/21 19:16:48  qboosh
- fixed some plugins (still NF)

Revision 1.1  2003/03/21 00:38:55  qboosh
- NFY - saving work
