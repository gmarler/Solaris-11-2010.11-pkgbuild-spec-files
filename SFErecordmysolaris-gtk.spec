#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFErecordmysolaris-gtk
Summary:             Recordmysolaris-gtk - Desktop recording tool, gtk frontend
Version:             0.3.3
Source:              http://recordmysolaris.googlecode.com/files/recordmysolaris-gtk-%{version}.tar.gz
URL:                 http://code.google.com/p/recordmysolaris/

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}_%{version}-build
BuildRequires:       SUNWgnome-common-devel
BuildRequires:       SUNWgnome-python26-libs
Requires:            SFErecordmysolaris

%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif


%define pythonver 2.6

%prep
%setup -q -n recordmysolaris-gtk-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

aclocal -I m4/
automake --copy --add-missing
autoconf

./configure --prefix=%{_prefix}                 \
            --libexecdir=%{_libexecdir}         \
            --mandir=%{_mandir}                 \
            --sysconfdir=%{_sysconfdir}         \
            --datadir=%{_datadir}               \
            --infodir=%{_infodir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

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
%{_bindir}/recordmysolaris-gtk
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/site-packages/recordmysolaris
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/recordmysolaris-gtk.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Tue Apr 27 2010 - Milan Jurik
- python 2.6
* Sun Apr 05 2009 - (andras.barna@gmail.com)
- bump version
* Sat Mar 07 2009 - (andras.barna@gmail.com)
- new version
* Mon Aug 25 2008 - (andras.barna@gmail.com)
- Initial spec
