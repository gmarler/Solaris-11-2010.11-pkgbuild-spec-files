#
# Copyright (c) 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define src_name ogmtools

Name:                SFEogmtools
Summary:             ogmtools - Tools for manipulating Ogg media streams
Version:             1.5
License:             GPLv2+
Source:              http://www.bunkus.org/videotools/ogmtools/%{src_name}-%{version}.tar.bz2
Patch1:              ogmtools-01-nogcc.diff
Patch2:              ogmtools-02-inttypes.diff
URL:                 http://www.bunkus.org/videotools/ogmtools/

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWogg-vorbis
BuildRequires: SFElibdvdread-devel
Requires: SFElibdvdread

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

aclocal
automake -a -c -f
autoconf

export CXX="$CXX -norunpath"
export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags} -lCrun"

./configure --prefix=%{_prefix}	\
            --bindir=%{_bindir}	\
	    --mandir=%{_mandir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Mon Mar 15 2010 - Albert Lee <trisk@opensolaris.org>
- Initial spec
