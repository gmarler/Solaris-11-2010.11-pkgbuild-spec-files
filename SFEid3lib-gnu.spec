#
# spec file for package SFEid3lib-gnu
#
# includes module(s): id3lib
#
#
%include Solaris.inc
%include usr-gnu.inc

Name:                    SFEid3lib-gnu
Summary:                 id3lib  - a software library for manipulating ID3v1/v1.1 and ID3v2 tags (g++)
Version:                 3.8.3
Source:                  %{sf_download}/id3lib/id3lib-%{version}.tar.gz
Patch1:                  id3lib-01-wall.diff
Patch2:                  id3lib-02-uchar.diff
Patch3:                  id3lib-03-gcc4.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWzlib
Requires: SUNWlibC
Requires: SUNWlibms

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n id3lib-%version
%patch1  -p1
%patch2  -p1
%patch3  -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CC=gcc
export CFLAGS="%{gcc_optflags}"
export CXX=g++
export CXXFLAGS="%{gcc_cxx_optflags}"
export LDFLAGS="%{_ldflags}"
export LD_OPTIONS="-i -L%{_libdir} -R%{_libdir}"

aclocal -I ./m4 $ACLOCAL_FLAGS
automake -a -c -f
autoconf
libtoolize --copy --force
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-fpm=%{fp_arch}          \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri Sep 25 2009 - trisk@opensolaris.org
- Add patch3
- Update build system
* Tue Jul 17 2007 - dougs@truemail.co.th
- Converted from SFEid3lib
