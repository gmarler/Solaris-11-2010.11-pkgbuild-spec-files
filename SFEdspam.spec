#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEdspam
Summary:             Extremely scalable, statistical-hybrid anti-spam filter
Version:             3.9.0
Source:              %{sf_download}/dspam/dspam-%{version}.tar.gz
Source1:             dspam.xml

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name

%prep
%setup -q -n dspam-%version
cp -p %{SOURCE1} dspam.xml

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
            --sysconfdir=%{_sysconfdir} \
            --mandir=%{_mandir} \
            --enable-daemon \
            --with-dspam-home=%{_localstatedir}/dspam

# Notes: 
# I tried setting localstatedir instead of hard-coding
# /var/dspam (above), but it got ignored.
#
# If built with shared enabled and static disabled, the
# RPATH gets polluted with src/.libs. So for now I just
# went with the default: both enabled. Then I remove 
# libdspam.a (after install but before packaging, as usual).

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/libdspam.la
rm ${RPM_BUILD_ROOT}%{_libdir}/libdspam.a

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp dspam.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/dspam
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0770, root, sys) %{_localstatedir}/dspam
%{_localstatedir}/dspam/*

%dir %attr (0755, root, sys) %{_localstatedir}/svc
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/dspam.xml

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%dir %attr (0755, root, bin) %{_includedir}
%attr(755, root, bin) %{_includedir}/*

%changelog
* Sun Feb 14 2010 - Albert Lee <trisk@opensolaris.org>
- Bump to 3.9.0
- Add SMF manifest for daemon mode
- Add devel package
* Mon Sep  08 2008 - michal.bielickihalokwadrat.de
- bumped up version to 3.8.0
* Wed Oct 11 2006 - laca@sun.com
- fix pkgconfig dir permissions
* Wed Sep 27 2006 - Eric Boutilier
- Initial spec
