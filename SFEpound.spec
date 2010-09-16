##
# spec file for package: pound
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:           SFEpound
Summary:        The Pound program is a reverse proxy, load balancer and HTTPS front-end for Web server(s)
Version:        2.4.5
License:        GPLv3
URL:            http://www.apsis.ch/pound/
Source:         http://www.apsis.ch/pound/Pound-%{version}.tgz
Source1:	%{name}-manifest.xml
Source2:	%{name}.cfg
Patch1:		pound-01-Makefile.in.diff
Distribution:	OpenSolaris
Vendor:		OpenSolaris Community

# OpenSolaris IPS Manifest Fields
#Meta(info.upstream): Robert Segall <roseg@apsis.ch>
#Meta(info.maintainer): Robert Milkowski <milek@wp.pl>
#Meta(info.classification): org.opensolaris.category.2008:Applications/Internet


BuildRoot:      %{_tmppath}/%{name}-%{version}-build
SUNW_Basedir:   /
SUNW_Copyright: %{name}.copyright


#####################################
##  Package Requirements Section   ##
#####################################

%include default-depend.inc
BuildRequires: SUNWopenssl-include
BuildRequires: SUNWbtool
BuildRequires: SUNWggrp
Requires: SUNWopensslr
Requires: SUNWopenssl-libraries
Requires: SUNWlibms
Requires: SUNWpcre
Requires: SUNWzlib
Requires: SUNWbzip


%description
The Pound program is a reverse proxy, load balancer and
HTTPS front-end for Web server(s). Pound was developed
to enable distributing the load among several Web-servers
and to allow for a convenient SSL wrapper for those Web
servers that do not offer it natively.

%prep
%setup -q -n Pound-%{version}
%patch1 -p0


%build
export CC=cc
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib -lmtmalloc"
export CFLAGS="%{optflags} -I/usr/sfw/include"
./configure --prefix=%{_prefix} --sysconfdir=/etc || (cat config.log; false)

# regexec() in libpcreposix behaves differently than in libc
# libc version works properly with pound
perl -pi -e 's/-lpcreposix//g' Makefile

make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#Install example config file
mkdir "${RPM_BUILD_ROOT}/etc/"
cp "%{SOURCE2}" "${RPM_BUILD_ROOT}/etc/"

#Install manifest
%define svcdir /var/svc/manifest/application/proxy
mkdir -p "${RPM_BUILD_ROOT}/%{svcdir}"
cp "%{SOURCE1}" "${RPM_BUILD_ROOT}/%{svcdir}/%{name}.xml"



%clean
rm -rf %{buildroot}

%if %(test -f /usr/sadm/install/scripts/i.manifest && echo 0 || echo 1)
%iclass manifest -f i.manifest
%endif


%files
%defattr(-,root,sys)
%dir %attr (0755, root, bin) %{_sbindir}
%attr(0555, root, bin) %{_sbindir}/pound
%attr(0555, root, bin) %{_sbindir}/poundctl

%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man8
%attr(0444, root, bin) %{_mandir}/man8/pound.8
%attr(0444, root, bin) %{_mandir}/man8/poundctl.8

%dir %attr(755,root,sys) /etc
%config(noreplace) %attr(644,root,root) /etc/%{name}.cfg

%dir %attr (0755, root, sys) /var
%dir %attr (0755, root, sys) %{svcdir}
%class(manifest) %attr (0444, root, sys) %{svcdir}/*

%dir %attr(0755, root, sys) %{_datadir}


%changelog
* Thu Nov 26 2009 - Thomas Wagner
- ported to SFE
* Wed Aug 12 2009 - Robert Milkowski
- spec changes after jucr update
* Thu May 05 2009 - Robert Milkowski
- initial version
## Re-build 24/09/09
