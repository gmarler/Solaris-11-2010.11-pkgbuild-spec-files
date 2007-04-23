#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

Name:                fftw
Summary:             Collection of fast C routines to compute DFTs
Version:             2.1.5
Source:              ftp://ftp.fftw.org/pub/%{name}/%{name}-%{version}.tar.gz
%include default-depend.inc

%prep
%setup -q -n %{name}-%{version}

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

# Can't figure out how to tell configure to install the provided
# html or ps docs... it installs the info files though. Punt.

./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --mandir=%{_mandir}		\
            --infodir=%{_infodir}	\
            --enable-shared=yes		\
            --enable-static=no

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/librfftw.la
rm ${RPM_BUILD_ROOT}%{_libdir}/libfftw.la

%changelog
* Mon Apr 23 2007 - Doug Scott
- Change to multi-isa build
* Wed Sep 27 2006 - Eric Boutilier
- Initial spec
