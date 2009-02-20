#
# package are under the same license as the package itself.
#
# bugdb: www.pulseaudio.org/report/
#

%include Solaris.inc

%define src_name pulseaudio
%define src_url http://0pointer.de/lennart/projects/%{src_name}

%define SFElibsndfile   %(/usr/bin/pkginfo -q SFElibsndfile && echo 1 || echo 0)

Name:		SFEpulseaudio
Summary:	pulseaudio - stream audio to clients
Version:	0.9.5
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
# bug 253
Patch1:		pulseaudio-01-ioctl.diff
Patch2:		pulseaudio-02-default.pa.diff
# bug 254
Patch3:		pulseaudio-03-esdcompat.diff
# bug 255
Patch4:		pulseaudio-04-devname.diff
Patch5:		pulseaudio-05-dirty_hack_IP_MULTICAST_LOOP-module-rtp-send.c
# bug 256
Patch6:         pulseaudio-06-null-argument.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#TODO are dependencies complete? 
%if %SFElibsndfile
BuildRequires: SFElibsndfile-devel
Requires: SFElibsndfile
%else
BuildRequires:	SUNWlibsndfile
Requires:	SUNWlibsndfile
%endif

BuildRequires: SUNWliboil-devel
BuildRequires: SFElibsamplerate-devel
Requires: SUNWliboil
Requires: SFElibsamplerate

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
perl -pi -e 's,/bin/sh,/bin/ksh,' src/daemon/esdcompat.in

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#_XGP4_2 and __EXTENSIONS__ for rtp.c to find all typedefs
export CPPFLAGS="-D_XPG4_2 -D__EXTENSIONS__"

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags} -lxnet -lsocket -lgobject-2.0"

./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

#rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a
#rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
#rm -f $RPM_BUILD_ROOT%{_libdir}/pulse-*/modules/lib*.a
#rm -f $RPM_BUILD_ROOT%{_libdir}/pulse-*/modules/lib*.la
find $RPM_BUILD_ROOT%{_libdir}/ -name "*.a" -exec rm {} \; -print -o -name  "*.la" -exec rm {} \; -print

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libexecdir}/pulse*
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files root
%defattr (-, root, bin)
%attr (0755, root, sys) %dir %{_sysconfdir}
%attr (0755, root, sys) %dir %{_sysconfdir}/pulse
%{_sysconfdir}/pulse/*

%changelog
* Tue Feb 17 2009 - Thomas Wagner
- make (Build-)Requires conditional SUNWlibsndfile|SFElibsndfile(-devel)
* Tue Mar 04 2008 - trisk@acm.jhu.edu
- Add patch6 to fix pactl crash
* Sat Sep 22 2007 - Thomas Wagner
- add patch5 dirty_hack_IP_MULTICAST_LOOP-module-rtp-send.c
  TODO: find correct way to setup IP_MULTICAST_LOOP or isn't it necessary
* Tue Sep 18 2007 - trisk@acm.jhu.edu
- Add patch4
* Sat Sep 15 2007 - trisk@acm.jhu.edu
- Fix rules, add patch3
* Thu Sep 13 2007 - Thomas Wagner
- corrected rm lib*.a and lib*.la
- activated patch2 (default.pa)
* Tue Sep 04 2007 - Thomas Wagner
- Added LDFLAG -lsocket to solve ipv6 socket error when setting IP-ACLs
- remove left over files from lib/pulse-*/lib*\.a and \.la
- configuration-file default.pa: connection from mpd via 
  pulse-output now works. Listens to localhost, see examples
  for local LAN syntax
* Sun Aug 12 2007 - dougs@truemail.co.th
- Added ioctl patch and root package
* Tue May 22 2007 - Thomas Wagner
- Initial spec
