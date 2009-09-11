#
# spec file for package SFElibdvdread
#
# includes module(s): libdvdread
#
%include Solaris.inc
%define src_url  http://downloads.sourceforge.net/dvdbackup/dvdbackup-0.4.1/dvdbackup-0.4.1.tar.bz2
%define app_name dvdbackup

Name:                    SFEdvdbackup
Summary:                 dvdbackup will extract all (or optionally only selected) titles as found on the dvd. 
Version:                 0.4.1
Source:                  %{src_url}/%{app_name}-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
buildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFElibdvdcss
Requires: SFElibdvdread

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n %{app_name}-%{version}
perl -i.orig -lpe 's/^AC_FUNC_MALLOC//' configure.ac

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

libtoolize
aclocal -I m4
autoheader
automake -a -c
autoconf -f
./configure --prefix=%{_prefix} 	\
	    --mandir=%{_mandir}		\
            --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/%{app_name}

%if %build_l10n
%files l10n
%defattr (-, root, other)
%{_datadir}/locale
%endif

%changelog
* Fri Sep 11 2006 - drdoug007@gmail.com
- Initial version
