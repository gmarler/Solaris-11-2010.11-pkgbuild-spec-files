#
# spec file for package SFEsarg
#

# asked for new ownership: tom68

##TODO## new version needs basic testing - give feedback!
##TODO## cleanup the names for all custom variables to look more similar with 
#        other spec files
##TODO## tell spec file to define for gcc *or* tell configure not to use gcc, 
#        use CC instead  (--without-gcc use CC to compile)
##TODO## add dependencies (run check-deps.pl)
#        SUNWopenldap(ur...)
##TODO## patch to have Solaris related defaults in sarg.conf
#access_log /usr/local/squid/var/logs/access.log
#access_log /var/squid/logs/access.log
# grep local *
#sarg.conf:#access_log /usr/local/squid/var/logs/access.log
#sarg.conf:#exclude_codes /usr/local/sarg/exclude_codes
#sarg.conf:#LDAPBindDN cn=proxy,dc=mydomain,dc=local
#sarg.conf:#LDAPBaseSearch ou=users,dc=mydomain,dc=local
#sarg.conf:#      squidguard_conf /usr/local/squidGuard/squidGuard.conf
#sarg.conf:#redirector_log /usr/local/squidGuard/var/logs/urls.log
#user_limit_block:conf="/usr/local/sarg/sarg.conf"
#user_limit_block:squid_password_file="/usr/local/squid/etc/passwd"


%include Solaris.inc
%define cc_is_gcc 1
%define _gpp g++
%include base.inc

%define src_name sarg
%define     targetdirname sarg
%define     apache2_majorversion 2
%define     apache2_version 2.2

#%define maindir /opt/sarg
#NOTE: sarg.conf is placed into the existing /etc/squid config directory
%define sarg_sys_conf_dir %{_sysconfdir}/squid
%define html_dir %{_localstatedir}/%{src_name}

Name:                    SFEsarg
Summary:                 Squid Analysis Report Generator
Version:                 2.3.1
Source:                  %{sf_download}/sarg/%{src_name}-%{version}.tar.gz
URL:                     http://sarg.sourceforge.net/sarg.php
Source1:                 %{src_name}.conf.example
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{src_name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

#copy example apache config
cp -p %{SOURCE1} .

perl -w -pi.bak -e "s,^#\!\s*/bin/sh,#\!/usr/bin/bash," configure

%build

export CC=gcc
export CXX=g++

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I/usr/sfw/include -I/usr/include/openldap"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib -lsocket -lnsl"

./configure --prefix=%{_prefix}                      \
            --sysconfdir=%{sarg_sys_conf_dir}	      \
            --enable-sargphp=%{html_dir}              \
            --enable-fontdir=%{html_dir}/fonts        \
            --enable-imagedir=%{html_dir}/images      \
%if %cc_is_gcc
#nothing
%else
            --without-gcc \
%endif


     #--enable-extraprotection - compile sarg with extra GCC options for increased security

gmake -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT

#want sarg.1 in man/man1/ subdir
[ -e %{buildroot}%{_mandir}/man1/sarg.1 ] || (mkdir -p %{buildroot}%{_mandir}/man1 ; mv %{buildroot}%{_mandir}/sarg.1 %{buildroot}%{_mandir}/man1/ )

install -Dp -m0644 css.tpl %{buildroot}%{html_dir}/sarg.css

#cp -av fonts/ images/ languages/ %{buildroot}%{sarg_sys_conf_dir}/
cp -av fonts/ images/ languages/ %{buildroot}%{html_dir}/

### Clean up buildroot
rm -rf %{buildroot}%{_sysconfdir}/sarg/languages/.new

mkdir -p $RPM_BUILD_ROOT/etc/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/
cp -p %{src_name}.conf.example $RPM_BUILD_ROOT/etc/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/%{src_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

#the script is found automaticly in ext-sources w/o a Source<n> keyword
%iclass renamenew -f i.renamenew

%files
%defattr (-, root, bin)
%doc README ChangeLog COPYING LICENSE CONTRIBUTORS DONATIONS
#we are a SUNW_BaseDir: / package
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%attr (-, root, other) %{_localedir}


%defattr (0640, webservd, bin)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}
%{_localstatedir}/%{src_name}/*

%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_sysconfdir}
%dir %attr(0755, root, bin) %{_sysconfdir}/squid
%class(renamenew) %{_sysconfdir}/squid/*
%class(renamenew) %{_sysconfdir}/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/%{src_name}.conf


%changelog
* Sun Jan 02 2011 - Thomas Wagner
- bump to 2.3.1
- adjust path layout to be closer to solaris's native paths
- add basic apache2 configuration template for virtual webdomain
* Sun Oct 21 2007 - Petr Sobotka sobotkap@centrum.cz
- Deleted dependency on SFEsquid as it's not require to have squid installed
-   all you need is to have logs from squid
* Sun Oct 21 2007 - Petr Sobotka sobotkap@centrum.cz
- Initial commit
