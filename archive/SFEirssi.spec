#
# spec file for package SFEirssi
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEirssi
Summary:             irssi - a terminal based IRC client
Version:             0.8.12
Source:              http://www.irssi.org/files/irssi-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%define perl_archlib /usr/perl5/vendor_perl/5.8.4/i86pc-solaris-64int

Requires: SUNWperl584usr

%prep
%setup -q -n irssi-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}                 \
             --bindir=%{_bindir}                 \
             --sysconfdir=%{_sysconfdir}         \
             --includedir=%{_includedir}         \
             --mandir=%{_mandir}                 \
             --libdir=%{_libdir}                 \
             --with-perl=module                  \
             --with-perl-lib=/usr/perl5/vendor_perl/5.8.4/

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_libdir}/irssi/modules/*.la \
         ${RPM_BUILD_ROOT}%{perl_archlib}/auto/Irssi/.packlist \
         ${RPM_BUILD_ROOT}%{perl_archlib}/auto/Irssi/*/.packlist \
         ${RPM_BUILD_ROOT}%{perl_archlib}/perllocal.pod \
         ${RPM_BUILD_ROOT}/etc/irssi.conf
rm -rf ${RPM_BUILD_ROOT}%{_docdir} \
        ${RPM_BUILD_ROOT}%{_includedir}
rmdir $RPM_BUILD_ROOT/etc

%clean
rm -rf $RPM_BUILD_ROOT

# The following shorthand works fine...

%files
%defattr (-, root, bin)
%{_bindir}/*
%{_libdir}/irssi/
%{perl_archlib}
%{_mandir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/irssi/

# Here's the "longhand" version:
# %files
# %defattr (-, root, bin)
# %dir %attr (0755, root, bin) %{_bindir}
# %{_bindir}/*
# %dir %attr (0755, root, bin) %{_libdir}/irssi
# %dir %attr (0755, root, bin) %{_libdir}/irssi/modules
# %{_libdir}/irssi/modules/*
# %{perl_archlib}/Irssi.pm
# %dir %attr (0755, root, bin) %{perl_archlib}/Irssi
# %{perl_archlib}/Irssi/*
# %dir %attr (0755, root, bin) %{perl_archlib}/auto/Irssi
# %{perl_archlib}/auto/Irssi/Irssi.bs
# %{perl_archlib}/auto/Irssi/Irssi.so
# %dir %attr (0755, root, bin) %{perl_archlib}/auto/Irssi/Irc
# %{perl_archlib}/auto/Irssi/Irc/*
# %dir %attr (0755, root, bin) %{perl_archlib}/auto/Irssi/TextUI
# %{perl_archlib}/auto/Irssi/TextUI/*
# %dir %attr (0755, root, bin) %{perl_archlib}/auto/Irssi/UI
# %{perl_archlib}/auto/Irssi/UI/*
# %dir %attr (0755, root, other) %{_datadir}/irssi
# %dir %attr(0755, root, bin) %{_datadir}/irssi/*
# %{_datadir}/irssi/*/*
# %dir %attr(0755, root, bin) %{_mandir}
# %dir %attr(0755, root, bin) %{_mandir}/*
# %{_mandir}/*/*
# %{_sysconfdir}/irssi.conf
# In order to include /etc/irssi.conf, is a root
# package required (which in this case would contain one file)?

%changelog
* Fri Oct 09 2007 - Petr Sobotka sobotkap@centrum.cz
- bump to 0.8.12
* Sun Apr 08 2007 - Thomas Wagner
- bump to 0.8.11-rc1, removed tarball_version (re-add if ever needed)
* 
* Fri Sep 01 2006 - Eric Boutilier
- Initial spec
