#
# spec file for package SFEsourcenav
#
# includes module(s): sourcenav
#
%include Solaris.inc

Name:                    SFEsourcenav
Summary:                 sourcenav - source code analysis tool
Version:                 5.2
%define tarball_version  5.2b2
Source:                  http://kent.dl.sourceforge.net/sourceforge/sourcenav/sourcenav-%{tarball_version}.tar.gz
URL:                     http://sourcenav.sourceforge.net/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n sourcenav-%{tarball_version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -DANSICPP"
export LDFLAGS="%{_ldflags}"
./configure --prefix=%{_prefix}/sourcenav	\
	    --mandir=%{_mandir}			\
	    --sysconfdir=%{_sysconfdir}
	    
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT%{_prefix}/sourcenav
mv man/mann/* $RPM_BUILD_ROOT/%{_mandir}/mann/
rm -rf man
rm -rf COPYING INSTALL.TXT NEWS README.TXT html

mkdir -p $RPM_BUILD_ROOT/%{_bindir}
cd $RPM_BUILD_ROOT/%{_bindir}
echo 'mydir=`dirname $0`' > snavigator
echo 'exec ${mydir}/../sourcenav/bin/snavigator "${@}"' >> snavigator
chmod 755 snavigator

rm $RPM_BUILD_ROOT %{_mandir}/man1/tclsh.1
rm $RPM_BUILD_ROOT %{_mandir}/man1/wish.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%{_prefix}/sourcenav
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Sat Oct 14 2006 - laca@sun.com
- move to /usr/sourcenav -- moving just datadir doesn't work unfortunately
- get rid of devel subpkg
* Sun Jul 23 2006 - laca@sun.com
- rename to SFEsourcenav
- mv datadir stuff into datadir/sourcenav subdir
- define tarball_version because Version should not include letters
- define -devel subpkg
* Mon Jul 17 2006 - Halton Huo <halton.huo@sun.com>
- Initial spec.
