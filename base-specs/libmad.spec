#
# spec file for package libmad
#
# includes module(s): libmad
#

Name:                    libmad
Summary:                 A high-quality MPEG audio decoder
Version:                 0.15.1.2
%define tarball_version  0.15.1b
Source:                  %{sf_download}/mad/libmad-%{tarball_version}.tar.gz
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n libmad-%tarball_version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags" 
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

%define fp_arch	 default
%ifarch sparc
%define fp_arch	sparc
%endif

%ifarch i386
%define fp_arch intel
%endif

%ifarch amd64
%define fp_arch	64bit
%endif

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-fpm=%{fp_arch}          \
            --enable-shared		     \
            --enable-accuracy                \
	    --disable-static

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
# Generate pkgconfig mad.pc file
mkdir $RPM_BUILD_ROOT%{_libdir}/pkgconfig
cat > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/mad.pc << EOF
prefix=%{_prefix}
exec_prefix=\${prefix}
libdir=\${exec_prefix}/lib
includedir=\${prefix}/include/

Name: libMAD
Description: A high-quality MPEG audio decoder
Version: 0.15.2b
Libs: -L\${libdir} -lmad
Cflags: -I\${includedir}
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Aug 21 2009 - Milan Jurik
- Initial base spec file
