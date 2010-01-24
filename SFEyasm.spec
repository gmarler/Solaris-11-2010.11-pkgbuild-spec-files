#
# spec file for package SFEyasm.spec
#
# includes module(s): yasm
#
%include Solaris.inc

%define src_name	yasm
%define src_url		http://www.tortall.net/projects/yasm/releases

Name:                   SFEyasm
Summary:                Yet another assembler
Version:                0.8.0
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:                 yasm-01-bin_multi_test.sh.diff
Patch2:                 yasm-02-configure.diff
Patch3:                 yasm-03-out_test.sh.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1 -b .patch01
%patch2 -p1 -b .patch02
%patch3 -p1 -b .patch03


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%{_libdir}

%changelog
* Wed Jun 2 2008 - oboril.lukas@gmail.com
- bump to 0.7.1
- remove CFLAGS, LDFLAGS, use wihtout optim flags is
 the safest way to have correct yasm.
* Mon Apr 30 2007 - dougs@truemail.co.th
- Initial version
