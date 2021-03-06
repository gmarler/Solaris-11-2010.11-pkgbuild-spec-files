#
# spec file for package SFEvala
#
# includes module(s): vala
#
%include Solaris.inc

%define	src_name vala
%define	src_url	http://download.gnome.org/sources/vala/0.10

Name:                SFEvala
Summary:             Vala programming language
Version:             0.10.3
Source:              %{src_url}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
#
# TODO: Does this depend on library/libgee too?
#
BuildRequires: library/desktop/libgee

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

aclocal
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
	    --disable-static			\
	    --enable-shared

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/devhelp
%{_datadir}/vala-0.10
%{_datadir}/aclocal
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sat Jan 29 2011 - gmarler@gmarler.com
- Bump to 0.10.3
- Change %{_datadir}/vala to .../vala-0.10
* Wed Mar 10 2010 - brian.cameron@sun.com
- Bump to 0.7.10.
* Tue Nov 24 2009 - brian.cameron@sun.com
- Bump to 0.7.8.
* Sun Oct 11 2009 - brian.cameron@sun.com
- Bump to 0.7.7.
* Fri Jul 27 2007 - dougs@truemail.co.th
- Initial spec
