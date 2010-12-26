#
# spec file for package SFEgutenprint
#
# includes module(s): gutenprint
#
%include Solaris.inc

%define	src_ver 5.1.3
%define	src_name gutenprint
%define	src_url	http://nchc.dl.sourceforge.net/sourceforge/gimp-print

Name:		SFEgutenprint
Summary:	Collection of high-quality printer drivers
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:		gutenprint-01-cups-version.diff
Patch2:		gutenprint-02-isfinite.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Requires: SFEcups

%description
Gutenprint is a collection of very high quality printer drivers for
UNIX/Linux. The goal of this project is uncompromising print quality
and robustness. Included with this package is the Print plugin for the
GIMP (hence the name), a CUPS driver, and a driver for Ghostscript
that may be compiled into that package. This driver package is
Foomatic-compatible to enable plug and play with many print spoolers.
In addition, various printer maintenance utilities are included. Many
users report that the quality of Gutenprint on high end Epson Stylus
printers matches or exceeds the quality of the drivers supplied for
Windows and Macintosh.

This package was previously named gimp-print.

%package root   
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-I/usr/gnu/include -I/usr/sfw/include -I/usr/sfw/include/ijs"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export LD_OPTIONS="-L/usr/gnu/lib -L/usr/sfw/lib -R/usr/gnu/lib:/usr/sfw/lib"

bash autogen.sh --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --disable-static			\
	    --enable-shared			\
	    --disable-debug

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm -rf $RPM_BUILD_ROOT%{_libdir}/gimp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_sbindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/cups
%{_libdir}/gutenprint
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gutenprint
%{_datadir}/foomatic
%{_datadir}/cups
%{_mandir}

%files root
%defattr (-, root, sys)
%{_sysconfdir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*


%changelog
* Fri Aug  3 2007 - dougs@truemail.co.th
- Initial spec
