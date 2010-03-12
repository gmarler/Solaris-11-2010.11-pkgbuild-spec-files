#
# spec file for package gpac
#
# includes module(s): gpac
#

%define	src_name gpac

Name:                SFEgpac
Summary:             Open Source multimedia framework
Version:             0.4.5
URL:                 http://gpac.sourceforge.net/
Source:              http://%{sf_mirror}/%{src_name}/%{src_name}-%{version}.tar.gz
Patch1:		     gpac-01-configure.diff
Patch2:              gpac-02-stringcat.diff 
Patch3:              gpac-03-ldflags.diff
Patch4:              gpac-04_wxT.diff
Patch5:              gpac-05-Playlist_wxT.diff
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%prep
unset P4PORT
%setup -q -n gpac
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I%{_includedir}"
export CXXFLAGS="%cxx_optflags -I%{_includedir}"
# search for freeglut in /usr/SFE
export LDFLAGS="%_ldflags $CFLAGS -L%{_libdir} -R%{_libdir}"

%if %with_jack
	JACK_OPTS="--enable-jack=yes"
%else
	JACK_OPTS="--disable-jack=yes"
%endif
%if %with_pulseaudio
	PULSEAUDIO_OPTS="--enable-pulseaudio=yes"
%else
	PULSEAUDIO_OPTS="--disable-pulseaudio=yes"
%endif
if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
	WXAPP="--disable-wx --use-theora=no"
else
	WXAPP="--enable-wx"
fi

chmod 755 ./configure
ksh93 ./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}         \
            --libdir=%{_libdir}		\
            --mandir=%{_mandir}		\
	    --cc=cc			\
	    --extra-libs="-lrt -lm"	\
	    --disable-opt		\
	    --mozdir=/usr/lib/firefox	\
	    --extra-cflags="$CFLAGS"	\
            --extra-ldflags="$LDFLAGS"  \
	    $JACK_OPTS			\
	    $PULSEAUDIO_OPTS		\
            $WXAPP

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
	mv config.mak config.orig && sed -e 's/OSS_LDFLAGS=/OSS_LDFLAGS=-m64/' -e 's/moddir=\/usr\/lib/moddir=\/usr\/lib\/%{_arch64}/' -e 's/moddir_path=\/usr\/lib/moddir_path=\/usr\/lib\/%{_arch64}/' -e 's/libdir=lib/libdir=lib\/%{_arch64}/' config.orig > config.mak
else
	mv config.mak config.orig && sed 's/WX_LFLAGS=/WX_LFLAGS=-lCrun -lgtk-x11-2.0 -lgdk-x11-2.0 -lX11 /' config.orig > config.mak
fi

# dn't build with paralell make. (need libgpac before MP4Box)
#make -j$CPUS
make 

%install
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/gpac
make install DESTDIR=$RPM_BUILD_ROOT
make install-lib DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mar 12 2010 - Gilles dauphin
- misssing lib/amd64
- minor patch for _T macro and new wxWidget
* Wed Sep 16 2009 - trisk@forkgnu.org
- Add patch3
- Support jack and pulseaudio
* Sun Aug 29 2009 - gilles Dauphin
- don't parallel make
* Sun Aug 24 2009 - Milan Jurik
- Initial base spec file
