#
# spec file for package SFEunbound
#
# includes module(s): unbound
#
%include Solaris.inc

Summary:	Validating, recursive, and caching DNS resolver
Name:		SFEunbound
Version:	1.3.1
License:	BSD
URL:		http://www.nlnetlabs.nl/unbound/
Source:		http://www.unbound.net/downloads/unbound-%{version}.tar.gz
Source1:	unbound.xml
Group: System Environment/Daemons
BuildRoot:	%{_tmppath}/unbound-%{version}-build
SUNW_BaseDir:	/
BuildRequires: SUNWflexlex
BuildRequires: SUNWopenssl-include
Requires: SUNWopenssl-libraries

%description
Unbound is a validating, recursive, and caching DNS resolver.

The C implementation of Unbound is developed and maintained by NLnet
Labs. It is based on ideas and algorithms taken from a java prototype
developed by Verisign labs, Nominet, Kirei and ep.net.

Unbound is designed as a set of modular components, so that also
DNSSEC (secure DNS) validation and stub-resolvers (that do not run
as a server, but are linked into an application) are easily possible.

The source code is under a BSD License.

%prep
%setup -q -n unbound-%{version}

CC=/opt/SUNWspro/bin/cc \
LDFLAGS="-lsocket -lnsl" \
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
	-libdir=%{_libdir} \
	--enable-static=no \
	--enable-sha2 \
	--with-conf-file=%{_sysconfdir}/unbound/unbound.conf \
	--with-pidfile=%{_localstatedir}/run/unbound.pid

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

make -j$CPU

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
install -d 0755 %{buildroot}%{_datadir}/doc/unbound
install -m 0644 doc/README %{buildroot}%{_datadir}/doc/unbound
install -m 0644 doc/CREDITS %{buildroot}%{_datadir}/doc/unbound
install -m 0644 doc/LICENSE %{buildroot}%{_datadir}/doc/unbound
install -m 0644 doc/FEATURES %{buildroot}%{_datadir}/doc/unbound
install -d 0700 %{buildroot}%{_sysconfdir}/unbound
install -d 0755 %{buildroot}%/var/svc/manifest/network/dns
install -m 0644 %{SOURCE1} %{buildroot}%/var/svc/manifest/network/dns

# no section 8
install -d 0755 %{buildroot}%{_datadir}/man/man1m
for i in %{buildroot}%{_datadir}/man/man8/*.8
do
  base=`basename $i 8`
  name1m=${base}1m
  mv $i %{buildroot}%{_datadir}/man/man1m/${name1m}
done
rmdir %{buildroot}%{_datadir}/man/man8
for i in %{buildroot}%{_datadir}/man/*/*
do
  sed 's/(8)/(1M)/g' $i | sed '/^\.TH/s/ \"8\" / \"1M\" /g' > $i.new
  mv $i.new $i
done

%clean
rm -rf ${RPM_BUILD_ROOT}

%pre
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/groupadd unbound';
  echo '/usr/sbin/useradd -d %{_sysconfdir}/unbound -s /bin/true -g unbound unbound';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%postun
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/userdel unbound';
  echo '/usr/sbin/groupdel unbound';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%files
%defattr(-,root,bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/doc/unbound
%attr(0644, root, other) %{_datadir}/doc/unbound/*
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr(0700, unbound, unbound) %{_sysconfdir}/unbound
%attr(0644, unbound, unbound) %config(noreplace) %{_sysconfdir}/unbound/unbound.conf
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/network
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/network/dns
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/network/dns/unbound.xml
%{_sbindir}/*
%{_mandir}/*/*
%{_includedir}/*
%{_libdir}/libunbound*

%changelog
* Sun Jul 12 2009 - Milan Jurik
- Added SMF manifest, removed init.d script
- Initial version.
