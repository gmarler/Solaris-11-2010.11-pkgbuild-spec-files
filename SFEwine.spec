#
# spec file for package SFEwine.spec
#
# includes module(s): wine
#
# Owner: trisk
%include Solaris.inc

%define src_name	wine
%define src_url		%{sf_download}/%{src_name}

Name:                   SFEwine
Summary:                Windows compatibility
Version:                1.1.17
URL:                    http://www.winehq.org/
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2
Source101:		http://trisk.acm.jhu.edu/winetricks-20080627
Patch1:			wine-01-shell.diff
# http://bugs.winehq.org/show_bug.cgi?id=9787
Patch2:			wine-02-acceptex.diff
# Implement network statistics in iphlpapi via libkstat and STREAMS TPI
#Patch3:			wine-03-iphlpapi.diff
# Wine assumes libraries are mapped to contiguous memory regions.
# Use less restrictive alignment for data section to avoid "holes" between
# sections that the OS is allowed to use for an anonymous mmap:
# http://opensolaris.org/jive/message.jspa?messageID=229817#229799
#Patch7:			wine-07-sun-ld.diff
#Patch8:			wine-08-init-fini.diff
Patch101:		winetricks-01-sh.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SUNWgnome-camera-devel
Requires:	SUNWgnome-camera
BuildRequires:	SUNWhea
Requires:	SUNWhal
BuildRequires:	SUNWdbus-devel
Requires:	SUNWdbus
Requires:	SUNWxorg-clientlibs
BuildRequires:	SUNWxorg-headers
Requires:	SUNWxorg-mesa
Requires:	SUNWlcms
BuildRequires:	SUNWjpg-devel
Requires:	SUNWjpg
BuildRequires:	SUNWpng-devel
Requires:	SUNWpng
Requires:	SUNWlxml
Requires:	SUNWlxsl
Requires:	SUNWcupsu
Requires:	SUNWsane-backendu
BuildRequires:	SUNWopenssl-include
Requires:	SUNWopenssl-libraries
BuildRequires:	SFEfreetype-devel
Requires:	SFEfreetype
BuildRequires:	SFElibaudioio-devel
Requires:	SFElibaudioio

%package devel
Summary:                 wine - developer files, /usr
SUNW_BaseDir:            %{_basedir}
Requires: %name
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
cp %{SOURCE101} winetricks
%patch101 -p1

# patch5 changes the server request spec, so update related files
perl tools/make_requests

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CC=/usr/sfw/bin/gcc
export CPPFLAGS="-I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} -D__C99FEATURES__"
export CFLAGS="-O2 -march=i686 -Xlinker -i -fno-omit-frame-pointer" 
export LDFLAGS="%{xorg_lib_path} %{gnu_lib_path} %{sfw_lib_path}"
export LD=/usr/ccs/bin/ld

autoconf -f
autoheader
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static		\
	    --without-alsa		\
	    --without-capi		\
	    --without-nas		\
	    --without-jack

make -j$CPUS || make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -m 0755 winetricks $RPM_BUILD_ROOT%{_bindir}/winetricks

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%postun
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}
%{_mandir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/wine
%defattr (-, root, other)
%{_datadir}/applications

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Mon Mar 16 2009 - andras.barna@gmail.com
- Bump to 1.1.17, disable patch3
* Sun Jan 25 2009 - Thomas Wagner
- Bump to 1.1.13
- rework patch3 wine-03-iphlpapi.diff for 1.1.13 - could update bug http://bugs.winehq.org/show_bug.cgi?id=14185
* Mon Dec 15 2008 - halton.huo@sun.com
- Bump to 1.1.10
* Mon Nov 17 2008 - halton.huo@sun.com
- Bump to 1.1.8
- Remove upstreamed patch and reorder
* Thu Jul 31 2008 - trisk@acm.jhu.edu
- Bump to 1.1.2
- Pause patch7 (partially upstreamed), add patch8
* Wed Jul 16 2008 - trisk@acm.jhu.edu
- Bump to 1.1.1
* Wed Jul 09 2008 - trisk@acm.jhu.edu
- Bump to 1.1.0
- Drop patch1 (upstreamed), patch2 (unnecessary)
* Thu Jun 19 2008 - trisk@acm.jhu.edu
- Add patch7, remove mapfile hack
* Tue Jun 17 2008 - trisk@acm.jhu.edu
- Bump to 1.0
- Add patch1
- Add winetricks
* Mon Jun 09 2008 - trisk@acm.jhu.edu
- Replace SFEfreetype dependency
* Mon Jun 09 2008 - trisk@acm.jhu.edu
- Bump to 1.0-rc4
- Drop patch1
- Replace SFEcups with SUNWcupsu
- Add lots of missing dependencies
- Use curses instead of ncurses
* Wed Jun 04 2008 - trisk@acm.jhu.edu
- Drop SFEfontforge, SUNWlcms-devel dependencies
- Add patch5 for http://bugs.winehq.org/show_bug.cgi?id=9787
- List bug URLs
* Sat May 31 2008 - trisk@acm.jhu.edu
- Bump to 1.0-rc3
* Sat May 24 2008 - trisk@acm.jhu.edu
- Bump to 1.0-rc2
* Sun May 18 2008 - trisk@acm.jhu.edu.
- Add patch4
* Tue May 13 2008 - trisk@acm.jhu.edu
- Bump to 1.0-rc1
* Mon Apr 28 2008 - trisk@acm.jhu.edu
- Bump to 0.9.61, update patch1, patch2
* Mon Apr 28 2008 - trisk@acm.jhu.edu
- Drop patch4 and patch5
- Add fix for long-standing problem with non-contiguous library mappings
- Add new patch2 to work around pre-snv_85 XRegisterIMInstantiateCallback
* Mon Apr 21 2008 - trisk@acm.jhu.edu
- Bump to 0.9.60, drop patch7, patch2
* Wed Apr 09 2008 - trisk@acm.jhu.edu
- Bump to 0.9.59, add patch7, update patch6
- Update dependencies (SFEfontforge is only used for build)
* Sat Mar 22 2008 - trisk@acm.jhu.edu
- Bump to 0.9.58
- Update patch1
- Update source URL
* Tue Mar 18 2008 - trisk@acm.jhu.edu
- Add patch6 to implement network statistics in iphlpapi
- Use autoconf
- Pause patch2 - -shared works, and the configure.ac part is broken
* Mon Mar 10 2008 - trisk@acm.jhu.edu
- Add SFElibaudioio dependency for Sun audio
* Sun Mar 09 2008 - trisk@acm.jhu.edu
- Bump to 0.9.57
- Add -D__C99FEATURES__ for isinf (can we do -std=c99?)
- Update patch5 to not mangle gp_list_* functions
* Thu Feb 21 2008 - nonsea@users.sourceforge.net
- Bump to 0.9.55
- Remove upstreamed patch add-wine_list.h_includes.diff and reorder
- Use gcc /usr/sfw/bin (there is no gcc under /usr/gnu/bin)
* Mon Nov 30 2007 - trisk@acm.jhu.edu
- Bump to 0.9.50
* Mon Nov 26 2007 - Thomas Wagner
- pause patch4 (removal of prelink) - breaks wine atm
* Sun Nov 25 2007 - Thomas Wagner
- bump to 0.9.49
- never Nevada builds define /usr/include/sys/list.h -> "list"* starts clushing with include/wine/list.h.
  to cleanup addwd "change_functions_structs_named_list_asterisk.sh" as patch5 and patch6
  quick patch4 removes code to run preload for linux (load an specific addresses on Solaris upcoming)
* Fri Oct 19 2007 - Doug Scott <dougs@truemail.co.th>
- bump to 0.9.47
* Wed Oct  3 2007 - Doug Scott <dougs@truemail.co.th>
- bump to 0.9.46
* Tue Aug 28 2007 - dougs@truemail.co.th
- bump to 0.9.44
* Mon Aug 13 2007 - dougs@truemail.co.th
- bump to 0.9.43
- Added SFEcups SFElcms SFEncurses to Required
* Sat Jul 14 2007 - dougs@truemail.co.th
* Fri Aug 03 2007 - dougs@truemail.co.th
- bump to 0.9.42
* Sat Jul 14 2007 - dougs@truemail.co.th
- bump to 0.9.41
* Mon Jul 10 2007 - dougs@truemail.co.th
- bump to 0.9.40
* Mon Apr 30 2007 - dougs@truemail.co.th
- bump to 0.9.37
* Mon Apr 30 2007 - dougs@truemail.co.th
- Remove $RPM_BUILD_ROOT before install
* Mon Apr 30 2007 - dougs@truemail.co.th
- Changed some scripts to use bash
* Mon Apr 30 2007 - dougs@truemail.co.th
- Added Requires: SFEfreetype to fix bad fonts
- bump to 0.9.36
* Mon Apr 23 2007 - dougs@truemail.co.th
- Fixed Summary
* Sun Apr 22 2007 - dougs@truemail.co.th
- Initial version
