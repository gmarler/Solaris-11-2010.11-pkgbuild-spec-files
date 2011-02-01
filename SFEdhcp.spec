#
# spec file for package dhcp
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

# Where dhcp configuration files are stored
%define dhcpconfdir %{_sysconfdir}/dhcp


%include Solaris.inc

Name:            dhcp
Summary:         Dynamic host configuration protocol software
Version:         4.2.0
License:         ISC DHCP license
URL:             http://www.isc.org/software/dhcp
Source:          ftp://ftp.isc.org/isc/%{name}/%{name}-%{version}a1.tar.gz
Source1:         %{name}-manifest.xml
SUNW_BaseDir:    /
BuildRoot:       %{_tmppath}/%{name}-%{version}-build
SUNW_Copyright:  %{name}.copyright

# OpenSolaris IPS Manifest Fields
Meta(info.upstream): dhcp-users@isc.org
Meta(info.maintainer): Robert Milkowski <milek@wp.pl>
Meta(info.classification): org.opensolaris.category.2008:System/Services
Meta(pkg.detailed_url): http://www.isc.org/software/dhcp

#####################################
##  Package Requirements Section   ##
#####################################

%include default-depend.inc
BuildRequires: SUNWgcc
BuildRequires: SUNWggrp
BuildRequires: SUNWgsed

%define sed /usr/bin/gsed

%description
DHCP (Dynamic Host Configuration Protocol) is a protocol which allows
individual devices on an IP network to get their own network
configuration information (IP address, subnetmask, broadcast address,
etc.) from a DHCP server. The overall purpose of DHCP is to make it
easier to administer a large network.  The dhcp package includes the
ISC DHCP service and relay agent.

To use DHCP on your network, install a DHCP service (or relay agent),
and on clients run a DHCP client daemon.  The dhcp package provides
the ISC DHCP service and relay agent.



%prep
%setup -q -n %name-%{version}a1

# Update paths in all man pages
for page in client/dhclient.conf.5 client/dhclient.leases.5 \
            client/dhclient-script.8 client/dhclient.8 ; do
    %{sed}   -i -e 's|CLIENTBINDIR|/sbin|g' \
                -e 's|RUNDIR|%{_localstatedir}/run|g' \
                -e 's|DBDIR|%{_localstatedir}/db/dhclient|g' \
                -e 's|ETCDIR|%{dhcpconfdir}|g' $page
done

for page in server/dhcpd.conf.5 server/dhcpd.leases.5 server/dhcpd.8 ; do
    %{sed}   -i -e 's|CLIENTBINDIR|/sbin|g' \
                -e 's|RUNDIR|%{_localstatedir}/run|g' \
                -e 's|DBDIR|%{_localstatedir}/db/dhcpd|g' \
                -e 's|ETCDIR|%{dhcpconfdir}|g' $page
done


%build
export CC=/usr/bin/gcc
export CXX=g++
export LDFLAGS="%_ldflags"
export CFLAGS="%{gcc_optflags}"
./configure --prefix=%{_prefix} --sysconfdir=%{dhcpconfdir} \
  || (cat config.log; false)

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove files we don't want
mkdir -p %{buildroot}/usr/share/doc/dhcp
mv %{buildroot}%{dhcpconfdir}/dhclient.conf %{buildroot}/usr/share/doc/dhcp/dhclient.conf.sample
mv %{buildroot}%{dhcpconfdir}/dhcpd.conf %{buildroot}/usr/share/doc/dhcp/dhcpd.conf.sample

cat << EOF > %{buildroot}%{dhcpconfdir}/dhcpd.conf
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp/dhcpd.conf.sample
#   see 'man -s 5 dhcpd.conf'
#
EOF

cat << EOF > %{buildroot}%{dhcpconfdir}/dhclient.conf
#
# DHCP Client Configuration file.
#   see /usr/share/doc/dhcp/dhclient.conf.sample
#   see 'man -s 5 dhclient.conf'
#
EOF

# create empty lease file
mkdir -p %{buildroot}/var/db
touch    %{buildroot}/var/db/dhcpd.leases

# install smf manifest
%define svcdir /var/svc/manifest/network
mkdir -p %{buildroot}/%{svcdir}
cp %{SOURCE1} %{buildroot}/%{svcdir}/%{name}.xml


%clean
rm -rf $RPM_BUILD_ROOT




%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_bindir}
%attr(0555, root, bin) %{_bindir}/*

%dir %attr (0755, root, bin) %{_sbindir}
%attr(0555, root, bin) %{_sbindir}/*

%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%dir %attr(0444, root, bin) %{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%dir %attr(0444, root, bin) %{_mandir}/man3/*
%dir %attr(0755, root, bin) %{_mandir}/man5
%dir %attr(0444, root, bin) %{_mandir}/man5/*
%dir %attr(0755, root, bin) %{_mandir}/man8
%dir %attr(0444, root, bin) %{_mandir}/man8/*


%dir %attr(0755, root, sys) /usr
%dir %attr(0755, root, bin) /usr/include
%dir %attr(0755, root, bin) /usr/include/dhcpctl
%dir %attr(0755, root, bin) /usr/include/isc-dhcp
%dir %attr(0755, root, bin) /usr/include/omapip
%dir %attr(0755, root, bin) /usr/lib
%dir %attr(0755, root, bin) /usr/share
%dir %attr(0755, root, bin) /usr/share/doc
%dir %attr(0755, root, bin) /usr/share/doc/dhcp

%config(noreplace) %attr(644,root,root) %{dhcpconfdir}/dhclient.conf
%config(noreplace) %attr(644,root,root) %{dhcpconfdir}/dhcpd.conf
%config(noreplace) %attr(644,root,root) /var/db/dhcpd.leases

%dir %attr (0755, root, sys) /var
%dir %attr (0755, root, sys) %{svcdir}
%class(manifest) %attr (0444, root, sys) %{svcdir}/*

/usr/include/dhcpctl/*
/usr/include/isc-dhcp/*
/usr/include/omapip/*
/usr/lib/*

/usr/share/doc/dhcp/dhclient.conf.sample
/usr/share/doc/dhcp/dhcpd.conf.sample


%changelog
* 2010-02-16 Robert Milkowski
- updated to 4.2.0a1
* 2009-08-30 Robert Milkowski
- initial spec
