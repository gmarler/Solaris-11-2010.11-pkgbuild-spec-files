#
# spec file for package SFEfreealut.spec
#
# includes module(s): freealut
#
%include Solaris.inc

%define src_name	freealut
%define src_url		http://connect.creativelabs.com/openal/Downloads/ALUT

Name:                   SFEfreealut
Summary:                free implementation of OpenAL's ALUT standard
Version:                1.1.0
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:		SFEopenal-devel
Requires:		SFEopenal

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


export PATH=%{_bindir}:$PATH
export CFLAGS="%optflags -I%_includedir"
export LDFLAGS="%_ldflags"
export LD_OPTIONS="-i -L%{_libdir} -R\$ORIGIN:\$ORIGIN/../lib"
./autogen.sh
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static
make clean
make # -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr(0755,root,bin) %{_libdir}
%dir %attr(0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Mar 2010 - Gilles Dauphin
- look in right basedir i.e. includedir event if it is in /usr/SFE by exemple.
* Wed Aug 15 2007 - dougs@truemail.co.th
- Moved to SFE
* Mon May 14 2007 - dougs@truemail.co.th
- Initial version
