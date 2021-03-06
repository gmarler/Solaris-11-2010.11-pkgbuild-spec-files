#
# spec file for package SFElibgsasl
#
# includes module(s): libgsasl
#
%include Solaris.inc

%define	src_name libgsasl
%define	src_url	ftp://alpha.gnu.org/pub/gnu/gsasl

Name:                SFElibgsasl
Summary:             Simple Authentication and Security Layer framework
Version:             0.2.18
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWlibgpg-error-devel
Requires: SUNWlibgpg-error
BuildRequires: SUNWlibgcrypt-devel
Requires: SUNWlibgcrypt
BuildRequires: SUNWgnutls-devel
Requires: SUNWgnutls
BuildRequires: SFElibntlm-devel
Requires: SFElibntlm
BuildRequires: SFElibidn-devel
Requires: SFElibidn
BuildRequires: SFEgsslib-devel
Requires: SFEgsslib
BuildRequires: SFEshishi-devel
Requires: SFEshishi
BuildRequires: SFElibtasn1-devel
Requires: SFElibtasn1

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version
rm m4/gettext.m4

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-I/usr/gnu/include"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export LD_OPTIONS="-L/usr/gnu/lib -R/usr/gnu/lib"

aclocal -I m4 -I gl/m4
libtoolize --copy --force 
automake -a -f
autoconf -f 
./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --sysconfdir=%{_sysconfdir}		\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --disable-rpath			\
	    --disable-static			\
	    --with-libgss-prefix=/usr/gnu	\
	    --enable-shared

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm -rf $RPM_BUILD_ROOT%{_datadir}/emacs
rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Fri Jul 27 2007 - dougs@truemail.co.th
- Initial spec
