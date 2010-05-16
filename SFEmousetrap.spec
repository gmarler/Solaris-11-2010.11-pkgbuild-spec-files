#
# Copyright (c) 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: trisk
#
%include Solaris.inc

%define python_version 2.6
%if %{?_without_debian:0}%{?!_without_debian:1}
%define src_name gnome-mousetrap
%define src_version 0.3+zgit2872572a
%define src_url http://ftp.us.debian.org/debian/pool/main/g/gnome-mousetrap
%else
%define src_name mousetrap
%define src_version 0.4
%define src_url http://trisk.acm.jhu.edu/src
%endif

Name:                    SFEmousetrap
Summary:                 MouseTrap - Webcam-based input system for GNOME
%if %{?_without_debian:0}%{?!_without_debian:1}
Version:                 0.3.1
%else
Version:                 0.4
%endif
License:                 GPLv2
%if %{?_without_debian:0}%{?!_without_debian:1}
Source:                  %{src_url}/%{src_name}_%{src_version}.orig.tar.gz
Patch1:                  gnome-mousetrap-01-debian.diff
Patch2:                  gnome-mousetrap-02-opencv2.diff
Patch3:                  gnome-mousetrap-03-area.diff
%else
Source:                  %{src_url}/%{src_name}-%{version}.tar.bz2
%endif
URL:                     http://live.gnome.org/MouseTrap

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWPython26
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-python26-libs
Requires: SUNWgnome-a11y-libs
Requires: SFEopencv
Requires: SFEpython26-xlib
BuildRequires: SUNWPython26-devel
BuildRequires: SUNWgnome-base-libs-devel

%if %build_l10n
%package l10n
Summary:                 %summary - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n %{src_name}-%{src_version}
%if %{?_without_debian:0}%{?!_without_debian:1}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%endif
for file in "src/mouseTrap/mousetrap.in" "src/mousetrap/app/mousetrap.in"; do
    if [ -f "$file" ]; then
        perl -pi -e 's,/bin/bash,/bin/sh,g; s,python2\.5,python,g' "$file"
    fi
done

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export MSGFMT="/usr/bin/msgfmt"

intltoolize
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

# Delete optimized py code
find $RPM_BUILD_ROOT%{_prefix} -type f -name "*.pyo" -exec rm -f {} ';'

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

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
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/mouseTrap
%{_datadir}/mouseTrap/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*/apps
%{_datadir}/icons/hicolor/*/apps/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/locale
%endif

%changelog
* Thu May 13 2010 - Albert Lee <trisk@opensolaris.org>
- Use Debian a11y fork of 0.3 by default, --without-debian to disable
- Add patch1, patch2, patch3
* Sun May 09 2010 - Albert Lee <trisk@opensolaris.org>
- Initial spec
