#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFErecordmysolaris
Summary:             Recordmysolaris - Desktop recording tool
Version:             0.3
Source:              http://recordmysolaris.googlecode.com/files/recordmysolaris-%{version}.tar.gz
URL:                 http://code.google.com/p/recordmysolaris/
Patch1:              recordmysolaris-01-shm.diff
License:             GPLv2
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}_%{version}-build
BuildRequires:       SUNWogg-vorbis
BuildRequires:       SUNWlibtheora
BuildRequires:       SUNWaudh

Requires:            SUNWxwplt
Requires:            SUNWogg-vorbis
Requires:            SUNWlibtheora

%include default-depend.inc

%prep
%setup -q -n recordmysolaris-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

aclocal
autoheader
automake --copy --add-missing
autoconf

./configure --prefix=%{_prefix}                 \
            --libexecdir=%{_libexecdir}         \
            --mandir=%{_mandir}                 \
            --sysconfdir=%{_sysconfdir}         \
            --datadir=%{_datadir}               \
            --infodir=%{_infodir}		\
            --disable-jack


make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/recordmysolaris
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Tue Apr 27 2010 - Milan Jurik
- missing Boomer header files dependency
- disable JACK as not needed
- shm headers changed
* Sun Apr 05 2009 - (andras.barna@gmail.com)
- bump version
* Mon Mar 16 2009 - (andras.barna@gmail.com)
- fix Requires
* Sat Mar 07 2009 - (andras.barna@gmail.com)
- new version
* Mon Aug 25 2008 - (andras.barna@gmail.com)
- Initial spec
