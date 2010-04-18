#
# spec file for package SFElibid3tag-gnu
#
# includes module(s): libid3tag
#

%include Solaris.inc
%include usr-gnu.inc

Name:         SFElibid3tag-gnu
Summary:      libid3tag
License:      GPL
Group:        System/GUI/GNOME
Version:      0.15.1.1
%define tarball_version 0.15.1b
Release:      1
Source:       %{sf_download}/mad/libid3tag-%{tarball_version}.tar.gz
URL:          http://www.underbit.com/products/mad/
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%name-%{version}-build
%include default-depend.inc
Requires:     SUNWzlib

%description
ID3 tag manipulation library a wide range of multimedia formats

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-libs

%prep
%setup -q -n libid3tag-%{tarball_version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export CXX=g++
export CXXFLAGS="-O3 -fno-omit-frame-pointer"
export LDFLAGS="%{_ldflags}"
export LD_OPTIONS="-i -L%{_libdir} -R%{_libdir}"

touch NEWS
touch AUTHORS
touch ChangeLog
libtoolize --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

./configure \
        --prefix=%{_prefix} \
        --sysconfdir=%{_sysconfdir} \
        --libdir=%{_libdir}         \
        --bindir=%{_bindir}         \
        --libexecdir=%{_libexecdir} \
        --mandir=%{_mandir}         \
        --localstatedir=/var/lib
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*a

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{tarball_version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sat Jul 14 2007 - dougs@truemail.co.th
- Converted from SFElibid3tag
