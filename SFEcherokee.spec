#
# spec file for package SFEcherokee
#
# includes module(s): cherokee
#
# http://code.google.com/p/cherokee/issues/detail?id=$bugid
#

%include Solaris.inc

Name:                    SFEcherokee
Summary:                 cherokee - Fast, flexible, lightweight web server
Version:                 0.99.4
Source:                  http://www.cherokee-project.com/download/0.99/%{version}/cherokee-%{version}.tar.gz
URL:                     http://www.cherokee-project.com/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

# date:2009-03-17 owner:alfred type:bug bugid:402
Patch1:                  cherokee-01-print-error.diff

%include default-depend.inc

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel          
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n cherokee-%version
%patch1 -p1

%build
export CFLAGS="%optflags -I%{_includedir}"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}                 \
            --bindir=%{_bindir}			\
            --sbindir=%{_sbindir}		\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}         \
            --datadir=%{_datadir}               \
            --mandir=%{_mandir}                 \
            --infodir=%{_infodir}               \
            --sysconfdir=%{_sysconfdir}         \
            --localstatedir=%{_localstatedir}   \
            --enable-os-string="OpenSolaris"    \
            --enable-pthreads                   \
            --with-wwwroot=%{_localstatedir}/cherokee
make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/cherokee/lib*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/cherokee/lib*.la
rm -rf $RPM_BUILD_ROOT/var/log
rm -rf $RPM_BUILD_ROOT/var/run

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/network/
cp http-cherokee.xml ${RPM_BUILD_ROOT}/var/svc/manifest/network/http-cherokee.xml

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}


%post -n SFEcherokee-root

if [ -f /lib/svc/share/smf_include.sh ] ; then
    . /lib/svc/share/smf_include.sh
    smf_present
    if [ $? -eq 0 ]; then
       /usr/sbin/svccfg import /var/svc/manifest/network/http-cherokee.xml
    fi
fi

exit 0

%preun -n SFEcherokee-root
if [  -f /lib/svc/share/smf_include.sh ] ; then
    . /lib/svc/share/smf_include.sh
    smf_present
    if [ $? -eq 0 ]; then
       if [ `svcs  -H -o STATE svc:/network/http:cherokee` != "disabled" ]; then
           svcadm disable svc:/network/http:cherokee
       fi
    fi
fi


%postun -n SFEcherokee-root

if [ -f /lib/svc/share/smf_include.sh ] ; then
    . /lib/svc/share/smf_include.sh
    smf_present
    if [ $? -eq 0 ] ; then
       /usr/sbin/svccfg export svc:/network/http > /dev/null 2>&1
       if [ $? -eq 0 ] ; then
           /usr/sbin/svccfg delete -f svc:/network/http:cherokee
       fi
    fi
fi

exit 0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/cherokee
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/cherokee
#%dir %attr (0755, root, other) %{_datadir}/doc
#%{_datadir}/doc/*


%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/*
%dir %attr (0755, root, sys) %{_localstatedir}
%{_localstatedir}/cherokee/*
%defattr (0755, root, sys)
%class(manifest) %attr(0444, root, sys)/var/svc/manifest/network/http-cherokee.xml

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*


%changelog
* Tue Mar 17 2009 - alfred.peng@sun.com
- Bump to 0.99.4.
* Sat Apr 21 2007 - dougs@truemail.co.th
- Fixed sbin to find cherokee-admin
* Sat Apr 07 2007 - alvaro@sun.com
- Bumped to 0.6.0 Beta1: 0.6.0b700
- Added SMF support
* Wed Jan 24 2007 - daymobrew@users.sourceforge.net
- s/SFEpcre/SUNWpcre/ because SUNWpcre is in Vermillion Devel.
* Wed Jan  3 2007 - laca@sun.com
- bump to 0.5.5 (note: 0.5.6 doesn't compile on Solaris)
- update download urls
* Fri Jun 23 2006 - laca@sun.com
- renamed to SFEcherokee
- updated file attributes
- removed the procedural scripts and added the manifest file to the manifest
  class
* Fri May 05 2006 - damien.carbery@sun.com
- Bump to 0.5.3.
* Thu Mar 30 2006 - damien.carbery@sun.com
- Add site URL and bump to 0.5.0.
* Wed Jan 25 2006 - rodrigo.fernandez-vizarra@sun.com
- Added SMF definition file install/removal
* Tue Jan 17 2006 - damien.carbery@sun.com
- Created.
