#
# spec file for package SFEssmtp
#
%include Solaris.inc

Name:                SFEssmtp
Summary:             Extremely simple SMTP Send-Only MTA
URL:                 http://alioth.debian.org/projects/ssmtp/
Version:             2.64
License:             GPLv2+
Source:              http://ftp.debian.org/debian/pool/main/s/ssmtp/ssmtp_%{version}.orig.tar.bz2
Patch1:		     ssmtp-01-genconfig.diff
Patch2:		     ssmtp-02-libc.diff
SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/ssmtp-%{version}-build
%include default-depend.inc

%prep
%setup -q -n ssmtp-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --sbindir=%{_sbindir}	\
            --libdir=%{_libdir}		\
            --sysconfdir=%{_sysconfdir}	\
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --disable-static		\
	    --enable-shared		\
	    --enable-logfile		\
	    --enable-inet6		\

make -j$CPUS

%install
rm -rf %{buildroot}
install -p -D -m 755 ssmtp            %{buildroot}%{_sbindir}/ssmtp
install -p -D -m 644 generate_config  %{buildroot}%{_bindir}/generate_config
install -p -D -m 644 revaliases       %{buildroot}%{_sysconfdir}/ssmtp/revaliases
install -p    -m 644 ssmtp.conf       %{buildroot}%{_sysconfdir}/ssmtp/ssmtp.conf
install -p -D -m 644 ssmtp.conf.5     %{buildroot}%{_mandir}/man5/ssmtp.conf.5
install -p -D -m 644 ssmtp.8          %{buildroot}%{_mandir}/man8/ssmtp.8
cd %{buildroot}%{_sbindir}
ln -s ssmtp sendmail.ssmtp
ln -s ssmtp newaliases.ssmtp
ln -s ssmtp mailq.ssmtp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_prefix}/bin
%{_prefix}/bin/*

%dir %attr (0755, root, bin) %{_prefix}/sbin
%{_prefix}/sbin/*

%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/ssmtp
%config(noreplace) %{_sysconfdir}/ssmtp/revaliases
%config(noreplace) %{_sysconfdir}/ssmtp/ssmtp.conf

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%doc COPYING INSTALL README TLS CHANGELOG_OLD
%dir %attr (0755, root, other) %{_docdir}


%changelog
* Sat Aug 21 2010 - Milan Jurik
- fix of permissions, included in SFE repository
* Sun Apr 11 2010 - Miroslav Osladil <mira@osladil.cz>
- Added generate_config
- Symlimks for sendmail, newaliases, mailq
* Sat Apr 10 2010 - Miroslav Osladil <mira@osladil.cz>
- Initial spec
