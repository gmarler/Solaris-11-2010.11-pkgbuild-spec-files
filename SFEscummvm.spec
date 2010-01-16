#
# spec file for package SFEscummvm
#
# includes module(s): ScummVM
#
%include Solaris.inc

Name:                    SFEscummvm
Summary:                 ScummVM - emulator for classic graphical games
Version:                 1.0.0
Source:                  %{sf_download}/scummvm/scummvm-%{version}.tar.bz2
URL:                     http://www.scummvm.org/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n scummvm-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%gcc_optflags -I/usr/sfw/include -DANSICPP"
export RPM_OPT_FLAGS="$CFLAGS -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export PERL5LIB=%{_prefix}/perl5/site_perl/5.6.1/sun4-solaris-64int
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"
export MSGFMT="/usr/bin/msgfmt"
export CXX=/usr/sfw/bin/gcc
export CC=/usr/sfw/bin/gcc
export PATH=$PATH:/usr/ccs/bin

./configure --prefix=%{_prefix}                 \
            --mandir=%{_mandir}
make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/scummvm
%{_datadir}/scummvm/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man6
%{_mandir}/man6/*

%changelog
* Sat Jan 16 2009 - Milan Jurik
- update to 1.0.0
* Sat Nov 17 2007 - trisk@acm.jhu.edu
- Bump to 0.10.0
* Fri Jul  7 2006 - laca@sun.com
- rename to SFEscummvm
- bump to 0.9.0
- update file attributes
- delete patchb build-fix.diff, no longer needed
* Wed Nov 09 2005 - glynn.foster@sun.com
- Initial spec
