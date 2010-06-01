# From pdl-linux
# TODO:
# - external libraries packages (is there any sense in that?)
#

%define		snap	20100521
#%define		rel		7

Summary:	Cinelerra - capturing, editing and production of audio/video material
#Summary(pl.UTF-8):	Cinelerra - nagrywanie, obróbka i produkcja materiału audio/video
Name:		cinelerra-cv
Version:	2.1
Release:	0.%{snap}.%{rel}
License:	GPL
Group:		X11/Applications
# git clone git://git.cinelerra.org/j6t/cinelerra.git cinelerra-cv
Source0:	http://public.enst.fr/%{name}-snap%{snap}.tar.gz
# Source0-md5:	e130b134a9e691ae36d2bbb117fc530b
#Patch0:		%{name}-build.patch
#Patch1:		%{name}-libpng.patch
#Patch2:		%{name}-desktop.patch
URL:		http://cinelerra.org/
#BuildRequires:	OpenEXR-devel >= 1.2.1
#BuildRequires:	OpenGL-GLU-devel
#BuildRequires:	OpenGL-devel
#BuildRequires:	a52dec-libs-devel
#BuildRequires:	alsa-lib-devel >= 1.0.8
#BuildRequires:	autoconf
#BuildRequires:	automake
#BuildRequires:	esound-devel
#BuildRequires:	ffmpeg-devel
#BuildRequires:	fftw3-devel
#BuildRequires:	freetype-devel >= 2.1.4
#BuildRequires:	gettext-devel
#BuildRequires:	lame-libs-devel >= 3.93.1
#BuildRequires:	libavc1394-devel >= 0.5.1
#BuildRequires:	libdv-devel
#BuildRequires:	libiec61883-devel >= 1.0.0
##BuildRequires:	libmpeg3-devel >= 1.7
#BuildRequires:	libpng-devel >= 2:1.4.0
#BuildRequires:	libraw1394-devel >= 1.2.0
#BuildRequires:	libsndfile-devel >= 1.0.11
#BuildRequires:	libstdc++-devel >= 5:3.2.2
#BuildRequires:	libtheora-devel >= 1.0-0.alpha4
#BuildRequires:	libtiff-devel >= 3.5.7
#BuildRequires:	libtool
#BuildRequires:	libuuid-devel
#BuildRequires:	mjpegtools-devel
#BuildRequires:	pkgconfig
#%ifarch %{ix86} %{x8664}
#BuildRequires:	nasm
#%endif
##BuildRequires:	quicktime4linux-devel >= 2.2
#BuildRequires:	sed >= 4.0
#BuildRequires:	xorg-lib-libX11-devel
#BuildRequires:	xorg-lib-libXext-devel
#BuildRequires:	xorg-lib-libXv-devel
#BuildRequires:	xorg-lib-libXxf86vm-devel
#Requires:	OpenEXR >= 1.2.1
#Requires:	alsa-lib >= 1.0.8
#Requires:	freetype >= 2.1.4
#Requires:	libavc1394 >= 0.5.1
#Requires:	libiec61883 >= 1.0.0
##Requires:	libmpeg3 >= 1.7
#Requires:	libraw1394 >= 1.2.0
#Requires:	libsndfile >= 1.0.11
#Requires:	libtheora >= 1.0-0.alpha4
##Requires:	quicktime4linux >= 2.2
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

This is Community Version.

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
#
#Wersja społecznościowa.

%prep
%setup -q -n %{name}
#%patch0 -p1
#%patch1 -p1
#%patch2 -p1

find -name Makefile.am | xargs %{__sed} -i -e 's#^LIBTOOL =.*##g'
%{__sed} -i -e 's/png_check_sig((unsigned char\*)test, 8)/!png_sig_cmp((unsigned char\*)test, 0, 8)/g' cinelerra/filepng.C

%build
#rm -f m4/*.m4 *.m4
#touch config.rpath
#%{__gettextize}
#%{__libtoolize}
#%{__aclocal} -I m4
#%{__autoheader}
#%{__automake}
#%{__autoconf}

cd hvirtual

export CC=gcc
export CXX=g++
export CFLAGS="-I%{_includedir} -I%{_prefix}/X11/include"
export CXXFLAGS="-I%{_includedir} -I%{_prefix}/X11/include"
export LDFLAGS="-L%{_libdir} -L/usr/X11/lib -R%{_libdir} -R/usr/X11/lib"
export PKG_CONFIG_PATH="%{_libdir}/pkgconfig"
export OPENEXR_CFLAGS="-I/usr/include/OpenEXR"
export OPENEXR_LIBS="-lIlmImf -lImath -lIex -lHalf -lIlmThread -lz"


./autogen.sh
#glib-gettextize --copy --force
#libtoolize --copy --force
#intltoolize --copy --force --automake
#aclocal --force -I m4
#autoconf -f
#automake -a -c -f

./configure --prefix=%{_prefix} 	\
	--disable-alsa			\
	--enable-oss			\
	--enable-shared --disable-static	\
	--mandir=%{_mandir}             \
	--infodir=%{_infodir}           \
	--bindir=%{_bindir}             \
	--libdir=%{_libdir}             \
	--datadir=%{_datadir}           \
	--includedir=%{_includedir}     \
	--docdir=%{_docdir}             \
	--libexecdir=%{_libexecdir}

./configure \
	CPPFLAGS="%{rpmcppflags} -I/usr/include/freetype2" \
	--enable-freetype2 \
	--with-external-ffmpeg \
	--with-alsa-prefix=%{_prefix} \
	--with-fontsdir=%{_fontsdir} \
	--with-plugindir=%{_libdir}/cinelerra
#%ifarch ppc
#	--enable-altivec \
#%endif
#%ifarch %{ix86} %{x8664}
#	--enable-mmx \
#	--enable-3dnow \
#%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/cinelerra/fonts

%find_lang cinelerra

%clean
rm -rf $RPM_BUILD_ROOT

#%post -p /sbin/ldconfig
#%postun -p /sbin/ldconfig

%files -f cinelerra.lang
%defattr(644,root,root,755)
%doc doc/* README* TODO
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/cinelerra
%attr(755,root,root) %{_libdir}/cinelerra/*.so
%{_libdir}/cinelerra/*.la
%{_libdir}/cinelerra/shapewipe
%{_libdir}/cinelerra/fonts
%attr(755,root,root) %{_libdir}/lib*.so.*
#%{_desktopdir}/*.desktop
#%{_pixmapsdir}/*.*

%define date	%(echo `LC_ALL="C" date +"%a %b %d %Y"`)
%changelog
* May 21 2010 - Gilles dauphin
- import from pdl-linux
* PLD Team <feedback@pld-linux.org>
All persons listed below can be reached at <cvs_login>@pld-linux.org

