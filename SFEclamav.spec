#
# spec file for package SFEclamav
#
# includes module(s): clamav
#
%include Solaris.inc

%define	src_name clamav

Name:                SFEclamav
Summary:             Unix Anti-virus scanner
Version:             0.96
Source:              %{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWncurses-devel
Requires:	SUNWncurses
BuildRequires:	SUNWsndmu
Requires:	SUNWsndmu

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}			\
            --sbindir=%{_sbindir}		\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --sysconfdir=%{_sysconfdir}		\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --with-libncurses-prefix=/usr/gnu	\
	    --disable-static			\
	    --enable-shared			\
	    --enable-milter			\
	    --disable-clamav			\
	    --with-dbdir=%{_localstatedir}/clamav

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/groupadd clamav';
  echo '/usr/sbin/useradd -d /var/clamav -s /bin/true -g clamav clamav';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%postun root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/userdel clamav';
  echo '/usr/sbin/groupdel clamav';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%actions
group groupname="clamav"
user ftpuser=false gcos-field="ClamAV Reserved UID" username="clamav" password=NP group="clamav"

%files
%defattr (-, root, bin)
%{_bindir}
%{_sbindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files root
%defattr (-, root, sys)
%{_sysconfdir}
%dir %attr (0775, clamav, clamav) %{_localstatedir}/clamav
%{_localstatedir}/clamav/*.cvd


%changelog
* Sun Apr 25 2010 - Milan Jurik
- added IPS support
* Thu Apr 01 2010 - Milan Jurik
- update to 0.96
* Sat Sep 19 2009 - Milan Jurik
- update to 0.95.2
* Fri Jul 27 2007 - dougs@truemail.co.th
- Initial spec
