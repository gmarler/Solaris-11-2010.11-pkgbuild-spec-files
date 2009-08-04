#
# spec file for package SFExine-lib
#
# includes module(s): xine-lib
#

%include Solaris.inc

%define with_hal %(pkginfo -q SUNWhal && echo 1 || echo 0)
%define sunw_gnu_iconv %(pkginfo -q SUNWgnu-libiconv && echo 1 || echo 0)
%define use_gcc3 %([ -n "$_USE_GCC3_" ] && echo 1 || echo 0)
%define use_gcc3 1
%define plugin_version 1.25

Name:         SFExine-lib
License:      GPL
Group:        System/Libraries
#Version:      1.1.16.3
#Version:      1.1.16.2
Version:      1.1.16.1
#Version:      1.1.16
Summary:      xine-lib - the core engine of the xine video player
Source:       %{sf_download}/xine/xine-lib-%{version}.tar.bz2
#Patch1:       xine-lib-01-sysi86.diff
Patch2:       xine-lib-02-asm-pic.diff
Patch3:       xine-lib-03-gettext.diff
Patch4:       xine-lib-04-hal-support.diff
#Patch5:       xine-lib-05-buildfix.diff
#Patch6:       xine-lib-06-oss.diff
URL:          http://xinehq.de/index.php/home
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
SUNW_BaseDir: %{_basedir}
Autoreqprov:  on
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-audio-devel
Requires: SUNWgnome-audio
BuildRequires: SUNWgnome-vfs-devel
Requires: SUNWgnome-vfs
BuildRequires: SFEaalib-devel
Requires: SFEaalib
BuildRequires: SUNWxorg-headers
Requires: SUNWxorg-clientlibs
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWogg-vorbis
BuildRequires: SUNWlibtheora-devel
Requires: SUNWlibtheora
Requires: SUNWsmbau
BuildRequires: SFElibcdio-devel
Requires: SFElibcdio
Requires: SUNWlibmng
BuildRequires: SFElibdvdnav-devel
BuildRequires: SFElibmad-devel

%if %use_gcc3
BuildRequires: SUNWgcc
Requires: SUNWgccruntime
%else
BuildRequires: SFEgcc
Requires: SFEgccruntime
%endif

%if %with_hal
Requires: SUNWhal
%endif
%if %option_with_gnu_iconv
%if %sunw_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SFElibiconv
Requires: SFEgettext
%endif
%else
Requires: SUNWuiu8
%endif


%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%package encumbered
Summary:       %{summary} - encumbered codecs
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name
Requires: SFElibmad
Requires: SFElibdvdnav

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n xine-lib-%version
#%patch1 -p1
%patch2 -p1
%patch3 -p1
%if %with_hal
%patch4 -p1
%endif
#%patch5 -p1
#%patch6 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

glib-gettextize --force

%if %use_gcc3
	export CXX=/usr/sfw/bin/g++
	export CC=/usr/sfw/bin/gcc
	export LDFLAGS="%arch_ldadd %ldadd ${EXTRA_LDFLAGS} -L/usr/X11/lib -R/usr/X11/lib -L/usr/gnu/lib -R/usr/gnu/lib"
%else
	export CXX=/usr/gnu/bin/gcc
	export CC=/usr/gnu/bin/gcc
	export LD=/usr/gnu/bin/ld
	export LDFLAGS="%arch_ldadd %ldadd ${EXTRA_LDFLAGS} -Wl,-export-dynamic -L/usr/X11/lib -R/usr/X11/lib -L/usr/gnu/lib -R/usr/gnu/lib"
%endif

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS -I m4
autoheader
automake -a -c -f 
autoconf
export CFLAGS="-O4 -fPIC -DPIC -I/usr/X11/include -I/usr/openwin/include -D_LARGEFILE64_SOURCE -I/usr/gnu/include -I/usr/include/libmng -mcpu=pentiumpro -mtune=pentiumpro -msse2 -mfpmath=sse "
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl -liconv"
export CXXFLAGS="$CXXFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl -liconv"
%endif
./configure --prefix=%{_prefix} \
            --with-w32-path=%{_libdir}/mplayer/codecs \
            --with-external-libmad \
            --with-external-dvdnav \
            --disable-opengl
gmake -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
gmake DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

for doc in README.dvb README.dxr3 README.freebsd README.irix README.opengl \
            README.solaris README.syncfb README; do
  rm $RPM_BUILD_ROOT%{_datadir}/doc/xine-lib/$doc
done

# the xv video driver causes a deadlock in 1.1.3
# still works in 1.1.2, but the problem doesn't seem to be in the xv
# driver itself; still investigating
#
# More info from Bernd Markgraf: the deadlock only happens starting from
# snv_51.
#
# Even more info from Alan Coopersmith: this is caused by libXv.so.1
# build issues in snv_51 to snv_44 (bugster 6494070)
snv_build=`uname -v`
case "$snv_build" in
    snv_5[1-6])
    echo "Deleting the XV video out plugin because it causes a deadlock in"
    echo "snv_51 to snv_55.  Please upgrade to snv_56 or later"
    rm $RPM_BUILD_ROOT%{_libdir}/xine/plugins/*/xineplug_vo_out_xv.so
    ;;
esac

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.so*
%{_libdir}/xine/plugins/%{plugin_version}/mime.types
%{_libdir}/xine/plugins/%{plugin_version}/post/xineplug_post_audio_filters.so
%{_libdir}/xine/plugins/%{plugin_version}/post/xineplug_post_goom.so
%{_libdir}/xine/plugins/%{plugin_version}/post/xineplug_post_mosaico.so
%{_libdir}/xine/plugins/%{plugin_version}/post/xineplug_post_planar.so
%{_libdir}/xine/plugins/%{plugin_version}/post/xineplug_post_switch.so
%{_libdir}/xine/plugins/%{plugin_version}/post/xineplug_post_tvtime.so
%{_libdir}/xine/plugins/%{plugin_version}/post/xineplug_post_visualizations.so
%{_libdir}/xine/plugins/%{plugin_version}/vidix
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_ao_out_esd.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_ao_out_file.so
#%{_libdir}/xine/plugins/%{plugin_version}/xineplug_ao_out_jack.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_ao_out_none.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_ao_out_oss.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_ao_out_sun.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_bitplane.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_gdk_pixbuf.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_image.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_lpcm.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_nsf.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_speex.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_spucmml.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_sputext.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_theora.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_vorbis.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_yuv.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_audio.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_avi.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_fli.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_flv.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_games.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_iff.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_image.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_matroska.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_mng.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_nsv.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_rawdv.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_ogg.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_pva.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_slave.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_sputext.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_yuv_frames.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_inp_cdda.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_inp_dvb.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_inp_dvd.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_inp_file.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_inp_gnome_vfs.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_inp_http.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_inp_net.so
%if %use_gcc3
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_inp_smb.so
%endif
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_inp_pnm.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_inp_rtp.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_inp_rtsp.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_inp_stdin_fifo.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_vo_out_aa.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_vo_out_none.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_vo_out_pgx32.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_vo_out_pgx64.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_vo_out_raw.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_vo_out_sdl.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_vo_out_xshm.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_vo_out_xv.so
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/xine

%files encumbered
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_a52.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_dts.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_dvaudio.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_faad.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_ff.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_gsm610.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_mad.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_mpc.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_mpeg2.so
#%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_qt.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_real.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_rgb.so
#%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_speex.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_spu.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_spucc.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_spudvb.so
#%{_libdir}/xine/plugins/%{plugin_version}/xineplug_decode_w32dll.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_asf.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_mpeg.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_mpeg_block.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_mpeg_elem.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_mpeg_pes.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_mpeg_ts.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_qt.so
#%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_rawdv.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_real.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_dmx_yuv4mpeg2.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_inp_mms.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_inp_vcd.so
%{_libdir}/xine/plugins/%{plugin_version}/xineplug_inp_vcdo.so

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/xine-config
%{_bindir}/xine-list-1.1
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Aug 01 2009 - Gilles Dauphin
- SUNWlibmng is in B117
- bump to 1.1.16.1
- read FLV now.
- TODO: sound of Flash video is not good.
* Tue Sep 02 2008 - nonsea@users.sourceforge.net
- No use undefined %{mplayer.codecdir}
* Sat Jan 26 2008 - moinak.ghosh@sun.com
- Change SFEgcc deps, follows from SFEgcc refactoring.
* Sat Jan 26 2008 - moinak.ghosh@sun.com
- Refactor package into encumbered and non-encumbered parts.
- Use gmake instead of Solaris make.
- Allow optional build using Gcc3.
- Rework patch xine-lib-04-hal-support.diff as it was failing to apply.
* Sun Nov 4 2007 - markwright@internode.on.net
- Bump to 1.1.8.  SUNWhal conditional dependency for Solaris 10.
- Comment patch1, patch5 and patch6 (already applied). Requires SFEgcc 4.2.2
- http://sourceforge.net/tracker/index.php?func=detail&aid=1812753&group_id=9655&atid=109655
* Mon Feb 26 2007 - markgraf@med.ovgu.de
- fix xine-lib-04-hal-support
  xineplug_inp_dvd.so needs to link LIBHAL_LIBS
* Fri Feb 23 2007 - markgraf@med.ovgu.de
- add patch to fix two hiccups with OSS 4.0x 
  (SOUND_PCM_SETFMT/SNDCTL_DSP_SETFMT and 
   SOUND_PCM_WRITE_RATE/SNDCTL_DSP_SPEED)
* Wed Feb 21 2007 - laca@sun.com
- re-enable the Xv video out plugin on snv_56 and later as libXv.so was fixed.
- bump to 1.1.4
- merge patches
- add patch buildfix.diff that adds a missing -I to a makefile
- disable the opengl plugin because it breaks the build -- need to investigate
  more
* Tue Jan 23 2007 - laca@sun.com
- move skins and plugins to base pkg from devel
* Sun Jan 21 2007 - laca@sun.com
- add missing defattr tag to %files
* Sun Jan  7 2007 - laca@sun.com
- create
