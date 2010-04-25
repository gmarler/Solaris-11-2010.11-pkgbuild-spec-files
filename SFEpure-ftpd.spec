
%include Solaris.inc

%define src_name pure-ftpd

Name:		SFEpure-ftpd
Version:	1.0.29
Summary:	Lightweight, fast and secure FTP server

Group:		System Environment/Daemons
License:	BSD
URL:		http://www.pureftpd.org
Source:		http://download.pureftpd.org/pub/%{src_name}/releases/%{src_name}-%{version}.tar.bz2
Source1:	pure-ftpd.xml
Patch1:		pure-ftpd-01-openldap.diff
Provides:	ftpserver
SUNW_BaseDir:	/
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

BuildRequires:	SUNWopenldapu
Requires:	SUNWopenldapu
BuildRequires:	SUNWopenssl-include
Requires:	SUNWopenssl-libraries
BuildRequires:	SUNWmysql51
Requires:	SUNWmysql51lib

%description
Pure-FTPd is a fast, production-quality, standard-comformant FTP server,
based upon Troll-FTPd. Unlike other popular FTP servers, it has no known
security flaw, it is really trivial to set up and it is especially designed
for modern Linux and FreeBSD kernels (setfsuid, sendfile, capabilities) .
Features include PAM support, IPv6, chroot()ed home directories, virtual
domains, built-in LS, anti-warez system, bandwidth throttling, FXP, bounded
ports for passive downloads, UL/DL ratios, native LDAP and SQL support,
Apache log files and more.

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
export CFLAGS="%optflags -I/usr/include/openldap -I/usr/mysql/5.1/include/mysql"
export LDFLAGS="%_ldflags -L/usr/mysql/5.1/lib/mysql -R /usr/mysql/5.1/lib/mysql"

./configure --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir}/%{src_name} \
            --with-sendfile \
            --with-paranoidmsg \
            --with-altlog \
            --with-puredb \
            --with-extauth \
            --with-pam \
            --with-cookie \
            --with-throttling \
            --with-ratios \
            --with-quotas \
            --with-ftpwho \
            --with-welcomemsg \
            --with-uploadscript \
            --with-virtualhosts \
            --with-virtualchroot \
            --with-diraliases \
            --with-peruserlimits \
            --with-privsep \
            --with-rfc2640 \
            --with-ldap \
            --with-mysql \
            --with-tls \
            --without-bonjour

make


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

install -d -m 755 %{buildroot}%{_mandir}/man8
install -d -m 755 %{buildroot}%{_sbindir}
install -d -m 755 %{buildroot}%{_sysconfdir}/%{src_name}
install -d -m 755 %{buildroot}%{_sysconfdir}/pki/%{src_name}}
install -d -m 755 %{buildroot}%{_localstatedir}/ftp

# Conf
install -p -m 755 configuration-file/pure-config.pl %{buildroot}%{_sbindir}
install -p -m 644 configuration-file/pure-ftpd.conf %{buildroot}%{_sysconfdir}/%{src_name}
install -p -m 755 configuration-file/pure-config.py %{buildroot}%{_sbindir}
install -p -m 644 pureftpd-ldap.conf %{buildroot}%{_sysconfdir}/%{src_name}
install -p -m 644 pureftpd-mysql.conf %{buildroot}%{_sysconfdir}/%{src_name}
install -p -m 644 pureftpd-pgsql.conf %{buildroot}%{_sysconfdir}/%{src_name}

# Manifest
install -d 0755 %{buildroot}%/var/svc/manifest/network
install -m 0644 %{SOURCE1} %{buildroot}%/var/svc/manifest/network

# Man
install -p -m 644 man/pure-ftpd.8 %{buildroot}%{_mandir}/man8
install -p -m 644 man/pure-ftpwho.8 %{buildroot}%{_mandir}/man8
install -p -m 644 man/pure-mrtginfo.8 %{buildroot}%{_mandir}/man8
install -p -m 644 man/pure-uploadscript.8 %{buildroot}%{_mandir}/man8
install -p -m 644 man/pure-pw.8 %{buildroot}%{_mandir}/man8
install -p -m 644 man/pure-pwconvert.8 %{buildroot}%{_mandir}/man8
install -p -m 644 man/pure-statsdecode.8 %{buildroot}%{_mandir}/man8
install -p -m 644 man/pure-quotacheck.8 %{buildroot}%{_mandir}/man8
install -p -m 644 man/pure-authd.8 %{buildroot}%{_mandir}/man8
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
rm -rf $RPM_BUILD_ROOT

%pre
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/groupadd pure-ftpd';
  echo '/usr/sbin/useradd -s /bin/true -g pure-ftpd pure-ftpd';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%postun
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/userdel pure-ftpd';
  echo '/usr/sbin/groupdel pure-ftpd';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%actions
group groupname="pure-ftpd"
user ftpuser=false gcos-field="pure-ftpd Reserved UID" username="pure-ftpd" password=NP group="pure-ftpd"

%files
%defattr(-, root, bin, -)
%doc FAQ THANKS AUTHORS CONTACT HISTORY NEWS
%doc README README.Authentication-Modules README.Configuration-File
%doc README.Contrib README.Donations README.LDAP README.MySQL
%doc README.PGSQL README.TLS README.Virtual-Users
%doc contrib/pure-vpopauth.pl pureftpd.schema contrib/pure-stat.pl
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc

%{_bindir}/pure-*
%{_sbindir}/pure-*
%{_sysconfdir}/%{src_name}
%{_sysconfdir}/pki/%{src_name}}
%{_mandir}/man1m/*
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/ftp
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/network
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/network/pure-ftpd.xml


%changelog
* Sun Apr 25 2010 - Milan Jurik
- added IPS support
- update to 1.0.29
- use Mysql 5.1 because 4.0 was removed
* Thu Jan 28 2010 Milan Jurik
- initial import to SFE

* Fri Dec 04 2009 Aurelien Bompard <abompard@fedoraproject.org> -  1.0.27-1
- version 1.0.27

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.22-4
- use password-auth common PAM configuration instead of system-auth

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.22-3
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 27 2009 Aurelien Bompard <abompard@fedoraproject.org> 1.0.22-1
- version 1.0.22

* Wed Mar 04 2009 Aurelien Bompard <abompard@fedoraproject.org> 1.0.21-20
- make pam and consolehelper's conf files noreplace

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.21-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 24 2009 Aurelien Bompard <abompard@fedoraproject.org> 1.0.21-18
- Rebuild for mysql

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.21-17
- Rebuild for Python 2.6

* Thu Jun 05 2008 Aurelien Bompard <abompard@fedoraproject.org> 1.0.21-16
- Rebuild for libcap.so.2 (bug 450086)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.21-15
- Autorebuild for GCC 4.3

* Thu Dec 06 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.0.21-14
- Rebuild for deps

* Sun Aug 26 2007 Aurelien Bompard <abompard@fedoraproject.org> 1.0.21-13
- rebuild for BuildID

* Sat Dec 09 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.0.21-12
- rebuild

* Sat Dec 09 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.0.21-11
- rebuild

* Wed Aug 30 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.0.21-9
- rebuild

* Fri Aug 04 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.0.21-8
- BuildRequire selinux-policy-devel for FC6 onwards

* Fri Aug 04 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.0.21-7
- install README.SELinux with perms 644 to avoid depending on the
  buildsys' umask (bug 200844)

* Fri Jun 16 2006 Aurelien Bompard <gauret[AT]free.fr> 1.0.21-6
- add missing m4 BuildRequires

* Sun May 14 2006 Aurelien Bompard <gauret[AT]free.fr> 1.0.21-5
- add missing BuildRequires

* Sun May 14 2006 Aurelien Bompard <gauret[AT]free.fr> 1.0.21-4
- add SELinux support
- prevent the init script from displaying the config on startup

* Sun Apr 09 2006 Aurelien Bompard <gauret[AT]free.fr> 1.0.21-3
- fix mysql socket location (bug 188426)

* Wed Feb 22 2006 Aurelien Bompard <gauret[AT]free.fr> 1.0.21-2
- build option rendezvous has been renamed to bonjour
- add --with-cork
- see bug 182314 for more info, thanks to Jose Pedro Oliveira

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 1.0.21-1
- version 1.0.21

* Sun Nov 13 2005 Aurelien Bompard <gauret[AT]free.fr> 1.0.20-4
- rebuild
- i18n in init script

* Mon Aug 01 2005 Aurelien Bompard <gauret[AT]free.fr> 1.0.20-3
- build feature-complete by default
- add TLS support
- see bug #162849

* Wed Mar 23 2005 Aurelien Bompard <gauret[AT]free.fr> 1.0.20-2.fc4
- implement Jose's RFE in bug 151337: pure-ftpwho can be run
  by a normal user.
- change release tag for FC4

* Sun Mar 13 2005 Aurelien Bompard <gauret[AT]free.fr> 1.0.20-1
- adapt to Fedora Extras (drop Epoch, change Release tag)

* Wed Feb 16 2005 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.20-0.fdr.9
- license is BSD, not GPL

* Mon Feb 14 2005 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.20-0.fdr.8
- various fixes. See bug 1573 (fedora.us) for more info.

* Fri Feb 11 2005 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.20-0.fdr.7
- fix init script
- require logrotate
- add rebuild switches to lower dependancies
- see bug 1573 (fedora.us) for more info.

* Fri Feb 04 2005 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.20-0.fdr.6
- Add the "UseFtpUsers no" directive in the config file since we don't
  use it anymore

* Wed Feb 02 2005 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.20-0.fdr.5
- various spec file improvements

* Mon Jan 31 2005 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.20-0.fdr.4
- add patch for x86_64 support
- implement wishes in bug 1573 from Jose Pedro Oliveira
- don't use the ftpusers file, and thus remove conflicts with other FTP servers
- rediff config patch

* Tue Nov 02 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.20-0.fdr.3
- add large file support

* Fri Sep 24 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.20-0.fdr.2
- redirect %%preun output to /dev/null
- add requirements to chkconfig for the scriptlets

* Sun Aug 01 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.20-0.fdr.1
- version 1.0.20 (bugfixes)

* Mon Jun 28 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.19-0.fdr.1
- version 1.0.19

* Tue May 04 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.18-0.fdr.1
- version 1.0.18
- spec file cleanups

* Sun Oct 19 2003 Aurelien Bompard <gauret[AT]free.fr> 1.0.16a-1
- Redhatize the Mandrake RPM
- version 1.0.16a
- improve ftpusers creation script

