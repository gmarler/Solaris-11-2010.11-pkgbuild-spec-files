#
# spec file for package SFEctags
#
# includes module(s): ctags
#
%include Solaris.inc

Name:                SFEctags
Summary:             Exuberant ctags
Version:             5.8
License:             GPLv2
URL:                 http://ctags.sourceforge.net/
Source:              %{sf_download}/ctags/ctags-%{version}.tar.gz
Patch1:		     ctags-01-destdir.diff
Patch2:              ctags-02-exctags.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n ctags-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -D_LARGEFILE64_SOURCE"
export LDFLAGS="%_ldflags"

libtoolize --copy --force
aclocal 
autoheader
autoconf -f
./configure --prefix=%{_prefix}  \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --includedir=%{_includedir} \
            --mandir=%{_mandir} \
	    --infodir=%{_infodir} \
	    --enable-etags \
	    --with-posix-regex

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

#mv $RPM_BUILD_ROOT%{_prefix}/man $RPM_BUILD_ROOT%{_mandir}
# No deliverables clash
mv $RPM_BUILD_ROOT%{_bindir}/ctags $RPM_BUILD_ROOT%{_bindir}/exctags
mv $RPM_BUILD_ROOT%{_mandir}/man1/ctags.1 $RPM_BUILD_ROOT%{_mandir}/man1/exctags.1
cd $RPM_BUILD_ROOT%{_mandir}/man1/ && ln -s exctags.1 etags.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%changelog
* Fri Nov 12 2010 - Milan Jurik
- use exctags as name, to be compatible with OpenSolaris distro and avoid clash
* Fri Nov 13 2009 - halton.huo@sun.com
- Bump to 5.8
* Thu Oct 30 2008 - jedy.wang@sun.com
- Bump to 5.7
* Fri Jul 13 2007 - dougs@truemail.co.th
- Initial spec
