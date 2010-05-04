#
# spec file for package SFEtremulous.spec
#
# includes module(s): tremulous
#
%include Solaris.inc

%define cc_is_gcc       1

%define SFEopenal       %(/usr/bin/pkg info openal-soft >/dev/null 2>&1 && echo 0 || echo 1)
%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

%define src_name        tremulous
%define src_url         http://%{sf_mirror}/sourceforge/tremulous
%define patch_url       http://gentoo.osuosl.org/distfiles
%define src_version     1.1.0

Name:                   SFEtremulous
Summary:                Tremulous - Team-based first-person shooter game with RTS elements
#Version:                1.1.0-r971
Version:                1.1.0.971
URL:                    http://tremulous.net/
Source:                 %{src_url}/%{src_name}-%{src_version}.zip
Source1:                %{patch_url}/tremulous-gentoopatches-1.1.0-r5.zip
#Source1:                http://dl.trem-servers.com/tremulous-gentoopatches-1.1.0-r5.zip
#Source2:                http://dl.trem-servers.com/vms-1.1.t971.pk3
# TO FIND : an official site for this file
Source2:                %{patch_url}/vms-1.1.t971.pk3
Patch1:                 tremulous-01-solaris.diff
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
#BuildRequires: SUNWcurl-devel
%if %SFEopenal
BuildRequires: SFEopenal-devel
%endif
Requires: SUNWogg-vorbis
Requires: SUNWcurl
%if %SFEopenal
Requires: SFEopenal
%endif

%prep
%setup -q -n %{src_name}
gzcat %{src_name}-%{src_version}-src.tar.gz | tar xf -
unzip -d %{src_name}-%{src_version}-src %{SOURCE1}
cd %{src_name}-%{src_version}-src
gpatch -p0 -f < tremulous-svn755-upto-971.patch
gpatch -p0 -f < tremulous-t971-client.patch
%patch1 -p1
cd ..
cp %{SOURCE2} base

%build
cd %{src_name}-%{src_version}-src

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="-I%{_includedir}"
export LDFLAGS="-L%{_libdir} -R%{_libdir}"
make BUILD_CLIENT_SMP=1 USE_CURL_DLOPEN=0 USE_OPENAL_DLOPEN=1 \
    USE_LOCAL_HEADERS=0 LDFLAGS="-L%{_libdir} -R%{_libdir} -lm -lnsl -lsocket"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/tremulous/base
mkdir -p $RPM_BUILD_ROOT%{_datadir}/tremulous

cd %{src_name}-%{src_version}-src

Q3ARCH=$(uname -p | sed -e s/i.86/x86/)
cp build/release-sunos-$Q3ARCH/tremulous.$Q3ARCH $RPM_BUILD_ROOT%{_libdir}/tremulous/tremulous.bin
cp build/release-sunos-$Q3ARCH/tremulous-smp.$Q3ARCH $RPM_BUILD_ROOT%{_libdir}/tremulous/tremulous-smp.bin
cp build/release-sunos-$Q3ARCH/tremded.$Q3ARCH $RPM_BUILD_ROOT%{_libdir}/tremulous/tremulous-server.bin
for prog in tremulous tremulous-smp tremulous-server; do
  echo "#!/bin/sh" > $RPM_BUILD_ROOT%{_bindir}/$prog
  case prog in
    *-server)
    echo "exec %{_libdir}/tremulous/${prog}.bin +set fs_basepath %{_datadir}/tremulous \"\$@\"" >> $RPM_BUILD_ROOT%{_bindir}/$prog
    ;;
    *)
    echo "exec %{_libdir}/tremulous/${prog}.bin +set fs_basepath %{_datadir}/tremulous +set ttycon 0 \"\$@\"" >> $RPM_BUILD_ROOT%{_bindir}/$prog
    ;;
  esac
  chmod 0755 $RPM_BUILD_ROOT%{_bindir}/$prog
done

cp build/release-sunos-$Q3ARCH/base/*.so $RPM_BUILD_ROOT%{_libdir}/tremulous/base

cd ..

mkdir -p $RPM_BUILD_ROOT%{_datadir}/tremulous/base
cp base/* $RPM_BUILD_ROOT%{_datadir}/tremulous/base
chmod 0644 $RPM_BUILD_ROOT%{_datadir}/tremulous/base/*

#mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
#cp tremuluous.xpm $RPM_BUILD_ROOT%{_datadir}/pixmaps
#chmod 0644 $RPM_BUILD_ROOT%{_datadir}/pixmaps/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/tremulous
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/tremulous
#%dir %attr (0755, root, other) %{_datadir}/pixmaps
#%{_datadir}/pixmaps/*

%changelog
* Mon May 03 2010 - Albert Lee <trisk@opensolaris.org>
- Try openal-soft and make OpenAL optional
- Update URLs
* APR 02 2010 - Gilles Dauphin
- update dowload site
* Mars 24 2010 - Gilles Dauphin
- adjust FLAGS for includedir
- compatible IPS version
* Sun Dec 07 2008 - dauphin@enst.fr
- SUNWcurl is in B101
* Thu Sep 20 2007 - trisk@acm.jhu.edu
- Fix version numbering
* Thu Sep 20 2007 - trisk@acm.jhu.edu
- Initial spec
