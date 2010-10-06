#
# spec file for package libid3tag
#
# includes module(s): libid3tag
#

Name:                    libid3tag
Summary:                 ID3 tag reading library from the MAD project
Version:                 0.15.1.2
%define tarball_version  0.15.1b
Source:                  %{sf_download}/mad/libid3tag-%{tarball_version}.tar.gz
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n libid3tag-%tarball_version

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
%define fp_arch	default
%endif

%ifarch i386
%define fp_arch default
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

gmake

%install
gmake install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
# Generate pkgconfig id3tag.pc file
mkdir $RPM_BUILD_ROOT%{_libdir}/pkgconfig
cat > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/id3tag.pc << EOF
prefix=%{_prefix}
exec_prefix=\${prefix}
libdir=\${exec_prefix}/lib
includedir=\${prefix}/include/

Name: libid3tag
Description: ID3 tag reading library from the MAD project
Version: 0.15.1b
Libs: -L\${libdir} -lid3tag
Cflags: -I\${includedir}
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Sep 26 2010 - Alex Viskovatoff
- Initial base spec file, based on libmad.spec
