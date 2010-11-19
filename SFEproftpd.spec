#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

# Proftpd needs to install in a special place to avoid name collisions with
# ftpshut, ftpcount, and ftpwho. Putting it in /usr/gnu is an option; but
# because its a server app -- as with SUNWapchu (Apache) -- putting it under
# /usr/<appname> seems to make more sense. Therefore...

%define src_name proftpd
%define _bindir %{_prefix}/%{src_name}/bin
%define _libdir %{_prefix}/%{src_name}/lib
%define _sbindir %{_prefix}/%{src_name}/sbin
%define _datadir %{_prefix}/%{src_name}/share
%define _includedir %{_prefix}/%{src_name}/include

%define	src_version	1.3.3c
%define	gss_version	1.3.3

Name:		SFEproftpd
Summary:	Highly configurable FTP server
Version:	%{src_version}
IPS_component_version: 1.3.3.0.3
License:	GPL
Group:		Applications/Internet
URL:		http://www.proftpd.org/
Source:		ftp://ftp.proftpd.org/distrib/source/%{src_name}-%{src_version}.tar.gz
Source1:	proftpd.xml
Source2:	%{sf_download}/gssmod/mod_gss-%{gss_version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: %name-root
BuildRequires: SUNWhea
BuildRequires: SUNWopenssl-include
Requires: SUNWopenssl-libraries
BuildRequires: SUNWgss
Requires: SUNWgss

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n %{src_name}-%version
gzcat %{SOURCE2} | tar xf -

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

export install_user=$LOGNAME
export install_group=`groups | awk '{print $1}'`

pushd mod_gss-%{gss_version}
./configure
popd

cp mod_gss-%{gss_version}/mod_gss.h include
cp mod_gss-%{gss_version}/mod_gss.c contrib

./configure --prefix=%{_prefix}/%{src_name}  \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --mandir=%{_mandir} \
            --sbindir=%{_sbindir} \
            --sysconfdir=%{_sysconfdir} \
            --localstatedir=%{_localstatedir} \
            --enable-ipv6 \
            --enable-ctrls \
            --enable-facl \
            --enable-nls \
            --enable-dso \
            --enable-openssl \
            --with-shared=mod_shaper:mod_gss

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

cp -r doc ${RPM_BUILD_ROOT}%{_docdir}
cp mod_gss-%{gss_version}/README.mod_auth_gss ${RPM_BUILD_ROOT}%{_docdir}/contrib
cp mod_gss-%{gss_version}/README.mod_gss ${RPM_BUILD_ROOT}%{_docdir}/contrib
cp mod_gss-%{gss_version}/mod_gss.html ${RPM_BUILD_ROOT}%{_docdir}/contrib
cp mod_gss-%{gss_version}/rfc1509.txt ${RPM_BUILD_ROOT}%{_docdir}/rfc
cp mod_gss-%{gss_version}/rfc2228.txt ${RPM_BUILD_ROOT}%{_docdir}/rfc

install -d 0755 %{buildroot}%/var/svc/manifest/site
install -m 0644 %{SOURCE1} %{buildroot}%/var/svc/manifest/site

# section 8 is not valid for Solaris
install -d 0755 $RPM_BUILD_ROOT%{_datadir}/man/man1m
for i in $RPM_BUILD_ROOT%{_datadir}/man/man8/*.8
do
  base=`basename $i 8`
  name1m=${base}1m
  mv $i $RPM_BUILD_ROOT%{_datadir}/man/man1m/${name1m}
done
rmdir $RPM_BUILD_ROOT%{_datadir}/man/man8
for i in $RPM_BUILD_ROOT%{_datadir}/man/*/*
do
  sed 's/(8)/(1M)/g' $i | sed '/^\.TH/s/ \"8\" / \"1M\" /g' > $i.new
  mv $i.new $i
done

find $RPM_BUILD_ROOT%{_prefix}/%{src_name}/libexec -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_prefix}/%{src_name}/libexec -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man?
%{_mandir}/man?/*
%dir %attr (0755, root, bin) %{_mandir}/man1m
%{_mandir}/man1m/*
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%attr (-, root, other) %{_localedir}
%dir %attr (0755, root, bin) %{_prefix}/%{src_name}/libexec
%{_prefix}/%{src_name}/libexec/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/%{src_name}.conf
%dir %attr (0755, root, sys) %{_localstatedir}
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/%{src_name}.xml

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Fri Nov 19 2010 - Milan Jurik
- bump to 1.3.3c
* Mon Jul 19 2010 - Milan Jurik
- bump to 1.3.3a
* Sun May 23 2010 - Milan Jurik
- shaper module build
- Kerberos module added
* Tue May 19 2010 - Milan Jurik
- SMF service for standalone mode added
- new bundled modules included
* Mars 24 2010 - Gilles dauphin
- bump to 1.3.3
* Mon Feb 12 2007 - Damien Carbery <daymobrew@users.sourceforge.net>
- Remove patch, 01-no-chown, and use current user's name and group in call to
  configure.

* Fri Feb  9 2007 - Damien Carbery <daymobrew@users.sourceforge.net>
- Bump to 1.3.1rc2. Add devel package. Add patch to remove chown commands
  that break the build.

* Tue Nov 14 2006 - Eric Boutilier
- Initial spec
