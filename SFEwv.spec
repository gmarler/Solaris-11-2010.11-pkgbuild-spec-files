#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# owner: halton
# bugdb: bugzilla.abisource.com
#

%include Solaris.inc

Name:                SFEwv
License:             GPL
Summary:             A library that allows access to Microsoft Word files
Version:             1.2.4
URL:                 http://wvware.sourceforge.net/
Source:              %{sf_download}/wvware/wv-%{version}.tar.gz
# owner:halton date:2007-09-18 bugid:11195 type:bug
Patch1:              wv-01-solaris-iconv.diff
# owner:halton date:2007-09-18 bugid:11196 type:bug
Patch2:              wv-02-w3m-dump.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:            SUNWgnome-base-libs
Requires:            SUNWlxml
Requires:            SUNWzlib
Requires:            SUNWlibmsr
Requires:            SUNWbzip
Requires:            SUNWcslr
Requires:            SUNWlibgsf
BuildRequires:       SUNWgnome-base-libs-devel
BuildRequires:       SUNWgnome-common-devel
BuildRequires:       SUNWlxml-devel
BuildRequires:       SUNWlibgsf-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n wv-%version
%patch1 -p1
%patch2 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}	\
            --with-glib=glib2	\
            --enable-static=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/wv/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Tue May 04 2010 - Milan Jurik
- added missing build dependency
* Mon Apr 14 2008 - nonsea@users.sourceforge.net
- s/SUNWdesktop-search-libs/SUNWlibgsf cause the pkg name change.
* Tue Sep 18 2007 - nonsea@users.sourceforge.net
- Add patch w3m-dump to use w3m convert html to txt
- Remove Requires SFElinks
* Tue Sep 18 2007 - nonsea@users.sourceforge.net
- Add patch solaris-iconv to fix wvWare core dump
* Sun Jun 10 2007 - nonsea@users.sourceforge.net
- Add defattr root:bin to -devel package.
* Fri May 04 2007 - nonsea@users.sourceforge.net
- Initial spec
