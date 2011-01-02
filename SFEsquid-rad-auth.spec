#

##TODO## add example configuration hints
##TODO## add testing instructions: /usr/squid/libexec/squid_radius_auth -h localhost -w testing123
#        John%20Doe hello
#replys with Ok
#error would be Err
#note: escape blank chars with "%20"
#note: uncomment example with "John Doe" in SFEfreeradius -> /etc/raddb/radius.conf
#      and svcadm restart freeradius to load the updated users file

%include Solaris.inc

%define parentname squid

Name:                SFEsquid-rad-auth
Summary:             proxy caching server for web clients - Radius authentication helper
Version:             1.10
Source:              http://www.squid-cache.org/contrib/squid_radius_auth/squid_radius_auth-%{version}.tar.gz

SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n squid_radius_auth-%version

cp Makefile.solaris Makefile

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

gmake -j$CPUS CONFDIR=%{_sysconfdir}/%{parentname} PREFIX=%{_prefix} \
              MANDIR=%{_mandir}/man8 BINDIR='%{_prefix}/%{parentname}/libexec'

%install
rm -rf $RPM_BUILD_ROOT

gmake -j$CPUS CONFDIR=%{_sysconfdir}/%{parentname} PREFIX=%{_prefix} \
              MANDIR=%{_mandir}/man8 BINDIR='%{_prefix}/%{parentname}/libexec'              \
              DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

#the script is found automaticly in ext-sources w/o a Source<n> keyword
%iclass renamenew -f i.renamenew

%files
%defattr (-, root, bin)
%doc README COPYRIGHT Changelog
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_prefix}/%{parentname}
%{_prefix}/%{parentname}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%attr (0755, root, sys) %dir %{_sysconfdir}
#probably not necessary (renamenew)
%class(renamenew) %attr (0700, webservd, webservd) %{_sysconfdir}/%{parentname}/squid_radius_auth.conf.default

%changelog
* Sun Jan  2 2010 - Thomas Wagner
- Initial spec
