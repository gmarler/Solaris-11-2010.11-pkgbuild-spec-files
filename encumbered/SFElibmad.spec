#
# spec file for package SFElibmad
#
# includes module(s): libmad
#
%include Solaris.inc

Name:                    SFElibmad
Summary:                 libmad  - a high-quality MPEG audio decoder
Version:                 0.15.1.2
%define tarball_version  0.15.1b
Source:                  %{sf_download}/mad/libmad-%{tarball_version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libmad-%tarball_version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
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

%if %cc_is_gcc
%define fpm_option --enable-fpm
%else
# asm stuff breaks with sun studio :(
%define fpm_option --disable-fpm
%endif

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-fpm=%{fp_arch}          \
            --enable-shared		     \
            --enable-accuracy                \
            %fpm_option                      \
	    --disable-static

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
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
Version: 0.15.1b
Libs: -L\${libdir} -lmad
Cflags: -I\${includedir}
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Thu Jul 30 2009 - oliver.mauras@gmail.com
- Add mad.pc to have a better detection for apps that needs libMAD
* Thu Jul 27 2006 - halton.huo@sun.com
- Correct Source url s/kend/kent
* Mon Jun 12 2006 - laca@sun.com
- renamed to SFElibmad
- changed to root:bin to follow other JDS pkgs.
- disable fpm when using sun studio, as the inline assembly syntax is different
  and breaks the build
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
