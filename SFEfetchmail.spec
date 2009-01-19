#
# spec file for package SFEfetchmail
#
# includes module(s): fetchmail
#
%include Solaris.inc

Name:                    SFEfetchmail
Summary:                 Fetchmail
Group:                   utilities/email
Version:                 6.3.6
Source:                  http://download.berlios.de/fetchmail/fetchmail-%{version}.tar.bz2
Patch1:                  fetchmail-01-gettext.diff
URL:                     http://fetchmail.berlios.de/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n fetchmail-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal -I m4-local"
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib"
export MSGFMT="/usr/bin/msgfmt"

glib-gettextize -f 
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake --add-missing
autoconf

./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}		\
	    --enable-POP3 --enable-IMAP		\
	    --enable-NTLM              		\
            --with-ssl-dir=/usr/sfw             \
	    --disable-nls

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
echo deleting pyo files
find $RPM_BUILD_ROOT -name '*.pyo' -exec rm {} \;

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python?.?
%dir %attr (0755, root, bin) %{_libdir}/python?.?/site-packages
%{_libdir}/python?.?/site-packages/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Jan 19 2009 - Thomas Wagner
- --enable-NTLM (untested)
* Mon Dec 15 2008 - halton.huo@sun.com
- Remove attribute.diff since SS12 support __attribute__ (unused)
* Wed May  7 2008 - Thomas Wagner
- enable ssl
* Sat Apr 21 2007 - dougs@truemail.co.th
- Added automake to build
* Thu Jan 11 2007 - laca@sun.com
- bump to 6.3.6
* Mon Jun 12 2006 - laca@sun.com
- rename to SFEfetchmail
- add -l10n pkg
- remove unnecessary patch no-po-dir.diff
- add patch attribute.diff that removed an __attribute unused
- change to root:bin to follow other JDS pkgs.
* Wed May 10 2006 - damien.carbery@sun.com
- Bump to 6.3.4. Modify %build/%install/%files 
* Wed May 10 2006 - damien.carbery@sun.com
- Add patch, 02-no-po-dir, to skip 'po' dir and stop infinite loop.
* Thu Oct 13 2005 - glynn.foster@sun.com
- Initial spec
