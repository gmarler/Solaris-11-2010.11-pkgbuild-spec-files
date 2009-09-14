#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# ### syslogd global replacement ###
# If you want to replace syslogd by syslog-ng do as follow:
# #>svcadm disable system-log 
# #>svccfg delete system-log
# #>svccfg import /var/svc/manifest/system/syslog-ng.xml
# #>svcadm enable syslog-ng
#
# Also you will need to fix logadm and all services that are dependent of system-log
# #>pfexec perl -pi.back -e 's#/var/run/syslog.pid#/var/run/syslog-ng.pid#g' /etc/logadm.conf
# #>for i in $(grep -Rl "svc:/system/system-log" /var/svc/manifest/); do pfexec perl -pi.back -e 's#svc:/system/system-log#svc:/system/syslog-ng#g' $i; done
# Done
#
#
%include Solaris.inc

Name:                SFEsyslog-ng
Summary:             Syslog-ng tries to fill the gaps original syslogd's were lacking
Version:             3.0.4
Source:              http://www.balabit.com/downloads/files/syslog-ng/open-source-edition/%{version}/source/syslog-ng_%{version}.tar.gz
Source2:             syslog-ng.xml
Source3:             syslog-ng.method
Source4:             syslog-ng.conf
#Patch1:              syslog-ng-01-loggen.diff

SUNW_BaseDir:        %{_basedir}
%include default-depend.inc
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

Requires:            SFEeventlog

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc


%prep
%setup -q -n syslog-ng-%version
# Fixing bad pcre.h include
perl -pi -e 's#<pcre.h>#<pcre/pcre.h>#' src/logmatcher.c
#%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# This source is gcc-centric, therefore...
export CC=gcc
# export CFLAGS="%optflags"
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"

export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --sysconfdir=%{_sysconfdir} \
            --localstatedir=%{_localstatedir}/run \
            --mandir=%{_mandir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# Remove %{_libexecdir} as it's empty
rm -rf $RPM_BUILD_ROOT%{_prefix}/libexec

# Add default conf
mkdir $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/syslog-ng.conf

# Add manifest and method
mkdir -p $RPM_BUILD_ROOT/lib/svc/method/
cp -p %{SOURCE3} $RPM_BUILD_ROOT/lib/svc/method/syslog-ng
mkdir -p $RPM_BUILD_ROOT/var/svc/manifest/system/
cp -p %{SOURCE2} $RPM_BUILD_ROOT/var/svc/manifest/system/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man5
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man5/syslog-ng.conf.5
%{_mandir}/man8/syslog-ng.8

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%attr(0644, root, sys) /etc/syslog-ng.conf
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/system/
%attr(0444, root, sys) %{_localstatedir}/svc/manifest/system/syslog-ng.xml
%defattr (-, root, bin)
%dir %attr (0755, root, bin) /lib/svc/method/
%attr(0755, root, bin) /lib/svc/method/syslog-ng


%changelog
* Sun Sep 13 2009 - oliver.mauras@gmail.com
- Version bump to 3.0.4
- Add SMF integration and default config
* Sun Feb 24 2008 - Moinak Ghosh
- Bump version to 2.0.8.
- Add dependency on required eventlog library.
- Add bindir to files to get additional programs.
- Add patch to work around broken configure when using --enable-dynamic-linking.
* Wed Oct 17 2007 - laca@sun.com
- bump to 2.0.5
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Sun Nov 05 2006 - Eric Boutilier
- Force gcc
* Wed Sep 27 2006 - Eric Boutilier
- Initial spec
