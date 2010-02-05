#
# spec file for package SFEdovecot
#
# works: snv105 / pkgbuild 1.3.91 / Sun Ceres C 5.10 SunOS_i386 2008/10/22


##TODO## check if adding pam settings is necessary (by one-time SMF service)
##TODO## add convenient helper for generating a default configuration file, by default with SSL enabled
##TODO## add convenient helper for generating SSL-certificates, make one-time SMF service calling that helper on request

%define src_name dovecot
# maybe set to nullstring outside release-candidates (example: 1.1/rc  or just 1.1)
#%define downloadversion	 1.1/rc
%define downloadversion	 1.2

%include Solaris.inc
Name:                    SFEdovecot
Summary:                 dovecot - A Maildir based pop3/imap email daemon
URL:                     http://www.dovecot.org
#note: see downloadversion above
Version:                 1.2.9
Source:                  http://dovecot.org/releases/%{downloadversion}/%{src_name}-%{version}.tar.gz
Source2:		dovecot.xml


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires: SUNWzlib
BuildRequires: SUNWopenssl-include
Requires: SUNWzlib
Requires: SUNWopenssl-libraries

%include default-depend.inc

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
Requires: %name


%prep
%setup -q -n %{src_name}-%version
cp -p %{SOURCE2} dovecot.xml


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir}         \
            --with-moduledir=%{_libexecdir}/%{src_name}/modules \
            --datadir=%{_datadir}	\
            --sysconfdir=%{_sysconfdir}/%{src_name} \
            --enable-shared		\
            --with-rundir=%{_localstatedir}/run/%{src_name} \
            --enable-header-install \
            --with-solr \
	    --disable-static		

            #--libexecdir=%{_libdir}/%{src_name} \

gmake -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#rm -rf $RPM_BUILD_ROOT/usr/include

mkdir -p ${RPM_BUILD_ROOT}/%{_localstatedir}/run/%{src_name}

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp dovecot.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README ChangeLog COPYING INSTALL NEWS AUTHORS TODO 
%dir %attr (0755,root,bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/%{src_name}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/%{src_name}/*



%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/%{src_name}
%{_sysconfdir}/%{src_name}/*
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/run
%dir %attr (0755, root, sys) %{_localstatedir}/run/%{src_name}
%class(manifest) %attr(0444, root, sys)/var/svc/manifest/site/dovecot.xml


%changelog
* Thu Feb 04 2010 - Albert Lee <trisk@opensolaris.org>
- Set CFLAGS
- Fix /var/run permissions
* Thu Jan 07 2010 - Thomas Wagner
- bump to 1.2.9
- adjust _libexexdir
* Fri Jan 01 2010 - Thomas Wagner
- bump to 1.1.20
- add --with-rundir=%{_localstatedir}/run/%{src_name}  since /usr/var/run/dovecot is wrong, add new location to %files
- add header files to the package by --enable-header-install, add to %files, don't rm header file location
- add full-text search --with-solr
* Sat Oct 03 2009  - Thomas Wagner
- bump to 1.1.19
* Sun Feb 07 2009  - Thomas Wagner
- bump to 1.1.11
* Wed Jan  7 2009 - Thomas Wagner
- remove %post, %preun, %postun
- adjust files in %doc, adjust wildcard for %{_docdir}/%{src_name}/*
- bump to 1.1.7
* Mon Oct 06 2008  - Thomas Wagner
- bump to 1.1.4
- add SMF FMRI / manifest for site/dovecot
* Thu May 22 2008  - Thomas Wagner
- Initial spec
