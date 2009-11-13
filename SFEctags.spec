#
# spec file for package SFEctags
#
# includes module(s): ctags
#
%include Solaris.inc
%include usr-gnu.inc

Name:                SFEctags
Summary:             Exuberant ctags
Version:             5.8
Source:              %{sf_download}/ctags/ctags-%{version}.tar.gz
Patch1:		     ctags-01-destdir.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWpostrun

%prep
%setup -q -n ctags-%version
%patch1 -p1

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
	    --infodir=%{_infodir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT%{_prefix}
ln -s share/man man

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%{_prefix}/man
%{_bindir}
%{_mandir}

%changelog
* Fri Nov 13 2009 - halton.huo@sun.com
- Bump to 5.8
* Thu Oct 30 2008 - jedy.wang@sun.com
- Bump to 5.7
* Fri Jul 13 2007 - dougs@truemail.co.th
- Initial spec
