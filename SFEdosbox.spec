#
# spec file for package SFEdosbox.spec
#
# includes module(s): dosbox
#
%include Solaris.inc

%define SFEsdl	%(/usr/bin/pkginfo -q SFEsdl && echo 1 || echo 0)

%define src_name	dosbox
Name:                   SFEdosbox
Summary:                DOS emulator
Version:                0.74
URL:			http://www.dosbox.com/
Group:			System/Emulators/Other
License:		GPLv2
Source:                 %{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
Patch1:			dosbox-01-solaris.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %SFEsdl
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%else
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%endif
BuildRequires: SFEsdl-net-devel
Requires: SFEsdl-net
BuildRequires: SFEsdl-sound-devel
Requires: SFEsdl-sound

%prep
%setup -q -c -n %name-%version
%patch1

%build
cd %{src_name}-%{version}
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags}"

libtoolize 
aclocal
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

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
cd %{src_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%changelog
* Fri Jun 25 2010 - Milan Jurik
- bump to 0.64, patch cleanup
* Wed Jul 22 2009 - matt@greenviolet.net
- Bump to 0.73, update patch1 to be cleaner, clean up spec file slightly
* Mon Feb 25 2008 - trisk@acm.jhu.edu
- Bump to 0.72, update dependencies, replace patch1
* Thu Apr 26 2006 - dougs@truemail.co.th
- Initial version
