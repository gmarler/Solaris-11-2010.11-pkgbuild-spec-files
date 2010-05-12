#
#
# spec file for package SFEtun
#
# includes module(s): tun
#
%include Solaris.inc
%define src_name tuntap
%define src_url http://www.whiteboard.ne.jp/~admin2/tuntap/source/%{src_name}

%define usr_kernel /usr/kernel
%define drv_base %{usr_kernel}/drv

Name:		SFEtun
Summary:	Virtual Point-to-Point network device
Version:	1.1
Source:		%{src_url}/%{src_name}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n %{src_name}

%build
autoconf -f
./configure
make
%ifarch sparcv9 amd64
mv tun tun64
mv tap tap64
make clean
./configure --disable-64bit
make
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -D if_tun.h $RPM_BUILD_ROOT%{_includedir}/net/if_tun.h
install -D tun $RPM_BUILD_ROOT%{drv_base}/tun
install -D tap $RPM_BUILD_ROOT%{drv_base}/tap
%ifarch sparcv9 amd64
install -D tun64 $RPM_BUILD_ROOT%{drv_base}/%{_arch64}/tun
install -D tap64 $RPM_BUILD_ROOT%{drv_base}/%{_arch64}/tap
%endif
install -D tun.conf $RPM_BUILD_ROOT%{drv_base}/tun.conf
install -D tap.conf $RPM_BUILD_ROOT%{drv_base}/tap.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
( PATH=/usr/bin:/usr/sfw/bin; export PATH ;
  retval=0;
  /usr/sbin/add_drv tun || retval=1;
  [ "$retval" = 0 ] && /usr/sbin/add_drv tap || retval=1;
  exit $retval ) 

%preun
( echo PATH=/usr/bin:/usr/sfw/bin; export PATH ;
  /usr/sbin/rem_drv tun || retval=1;
  /usr/sbin/rem_drv tap || retval=1;
  exit 0
)

%actions
driver name=tun
driver name=tap

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/net
%{_includedir}/net/if_tun.h
%dir %attr (0755, root, sys) %{usr_kernel}
%dir %attr (0755, root, sys) %{drv_base}
%{drv_base}/tun
%{drv_base}/tap
%{drv_base}/tun.conf
%{drv_base}/tap.conf
%ifarch amd64 sparcv9
%dir %attr (0755, root, sys) %{drv_base}/%{_arch64}
%{drv_base}/%{_arch64}/tun
%{drv_base}/%{_arch64}/tap
%endif

%changelog
* Wed May 12 2010 - Milan Jurik
- update according the latest upstream
- IPS support added
* Wed Oct  3 2007 - Doug Scott
- Added base spec
- Updated to build tap from latest source
* Wed Apr 07 2007 - Eric Boutilier
- Initial spec
