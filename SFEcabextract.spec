#
# spec file for package SFEcabextract.spec
#
# includes module(s): cabextract
#
%include Solaris.inc

%define src_name	cabextract
%define src_url		http://www.cabextract.org.uk

Name:                   SFEcabextract
Summary:                CAB file extractor
Version:                1.3
Group:			System/Utilities
URL:			http://www.cabextract.org.uk
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
License:		GPLv3
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"
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
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%changelog
* Sun Aug 08 2010 - Milan Jurik
- bump to 1.3 to fix CVE-2010-2801
* Tue Feb 11 2008 - pradhap (at) gmail.com
- Fixed links
* Tue Apr 24 2006 - dougs@truemail.co.th
- Initial version
