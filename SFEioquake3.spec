#
# spec file for package SFEioquake3.spec
#
# includes module(s): ioquake3
#
%include Solaris.inc

%define cc_is_gcc       1

%define SFEopenal       %(/usr/bin/pkg info openal-soft >/dev/null 2>&1 && echo 0 || echo 1)
%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

%define src_name        ioquake3
%define src_url         http://www.ioquake3.org/files/

Name:                   SFEioquake3
Summary:                ioquake3 - icculus.org Quake3
Version:                1.36
URL:                    http://www.ioquake3.org/
Source:                 %{src_url}/%{version}/%{src_name}-%{version}.tar.bz2
Patch1:                 ioquake3-01-solaris.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%else
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%endif
%ifarch i386 amd64
BuildRequires: SUNWxorg-mesa
%endif
BuildRequires: SUNWogg-vorbis-devel
# SUNWspeex is missing speex_preprocess_*
#BuildRequires: SUNWspeex-devel
%if %SFEopenal
BuildRequires: SFEopenal-devel
%endif
Requires: SUNWogg-vorbis
# SUNWspeex is missing speex_preprocess_*
#Requires: SUNWspeex
Requires: SUNWcurl

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%define 
make BUILD_CLIENT_SMP=1 USE_CURL_DLOPEN=0 USE_OPENAL_DLOPEN=1 \
    USE_CODEC_VORBIS=1 USE_INTERNAL_SPEEX=1 USE_LOCAL_HEADERS=0

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ioquake3/baseq3
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ioquake3/missionpack
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ioquake3

Q3ARCH=$(uname -p)
cp build/release-sunos-$Q3ARCH/ioquake3.$Q3ARCH $RPM_BUILD_ROOT%{_libdir}/ioquake3/ioquake3.bin
cp build/release-sunos-$Q3ARCH/ioquake3-smp.$Q3ARCH $RPM_BUILD_ROOT%{_libdir}/ioquake3/ioquake3-smp.bin
cp build/release-sunos-$Q3ARCH/ioq3ded.$Q3ARCH $RPM_BUILD_ROOT%{_libdir}/ioquake3/ioquake3-server.bin
for prog in ioquake3 ioquake3-smp ioquake3-server; do
  cat > $RPM_BUILD_ROOT%{_bindir}/$prog <<EOF
#!/bin/sh
if [ ! -r %{_datadir}/ioquake3/baseq3/pak8.pk3 ]; then
  echo "MISSING GAME DATA: Required game data updates are not installed."
  echo ""
  echo "Download quake3-latest-pk3s.zip from http://ioquake3.org/patch-data/"
  echo "To install the updates, run:"
  echo "  unzip quake3-latest-pk3s.zip"
  echo "  cp -r quake3-latest-pk3s/* %{_datadir}/ioquake3"
  exit 1
fi
if [ ! -r %{_datadir}/ioquake3/baseq3/pak0.pk3 ]; then
  echo "MISSING GAME DATA: Original game data (pak0.pk3) is not installed."
  echo ""
  echo "To install pak0.pk3 from your Quake III: Arena CD-ROM, run:"
  echo "  cd /media/Quake3 (or the location of your CD-ROM)"
  echo "  cp Quake3/baseq3/pak0.pk3 %{_datadir}/ioquake3/baseq3/pak0.pak"
  echo "Alternatively, you can use pak0.pk3 from the Quake III: Arena Demo"
  exit 1
fi
EOF
  case prog in
    *-server)
    echo "exec %{_libdir}/ioquake3/${prog}.bin +set fs_basepath %{_datadir}/ioquake3 \"\$@\"" >> $RPM_BUILD_ROOT%{_bindir}/$prog
    ;;
    *)
    echo "exec %{_libdir}/ioquake3/${prog}.bin +set fs_basepath %{_datadir}/ioquake3 +set ttycon 0 \"\$@\"" >> $RPM_BUILD_ROOT%{_bindir}/$prog
    ;;
  esac
  chmod 0755 $RPM_BUILD_ROOT%{_bindir}/$prog
done

cp build/release-sunos-$Q3ARCH/baseq3/*.so $RPM_BUILD_ROOT%{_libdir}/ioquake3/baseq3
cp build/release-sunos-$Q3ARCH/missionpack/*.so $RPM_BUILD_ROOT%{_libdir}/ioquake3/missionpack

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/ioquake3
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/ioquake3

%changelog
* Mon May 03 2010 - Albert Lee <trisk@opensolaris.org>
- Bump to 1.36
- Try openal-soft and make OpenAL optional, use SUNWcurl
- Update wrapper script
- Delete %post
* Wed Sep 19 2007 - trisk@acm.jhu.edu
- Initial spec
