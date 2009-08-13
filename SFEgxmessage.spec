#
# spec file for package SFEgxmessage.spec
#
%include Solaris.inc

Name:         SFEgxmessage
Summary:      gxmessage - xmessage clone for GNOME
Version:      2.12.1
URL:          http://homepages.ihug.co.nz/~trmusson/programs.html#gxmessage
Source:       http://homepages.ihug.co.nz/~trmusson/stuff/gxmessage-%{version}.tar.gz
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgnome-libs
Requires: SUNWxwrtl
BuildRequires: SUNWxwinc

%prep
%setup -q -n gxmessage-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

pwd

./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --datadir=%{_datadir}       \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
ln -s gxmessage $RPM_BUILD_ROOT%{_bindir}/xmessage
rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%postun
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/*
%{_datadir}/info/gxmessage.info
%dir %attr(0755, root, bin) %{_datadir}/locale
%{_datadir}/locale/*
%{_datadir}/man/man1/gxmessage.1


%changelog
* Wed Aug 12 2009 - matt@greenviolet.net
- Cleaned up packaging
* Mon Aug 10 2009 - matt@greenviolet.net
- Fixed permissions for %{_prefix}/share and its children.
* Mon Jun 01 2009 - matt@greenviolet.net
- Initial version
