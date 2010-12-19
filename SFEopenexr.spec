#
# spec file for package SFEopenexr.spec
#
# includes module(s): openexr
#
%include Solaris.inc

%define src_name	openexr
%define src_url		http://download.savannah.nongnu.org/releases/openexr

Name:		SFEopenexr
Summary:	high dynamic-range (HDR) image file format
Version:	1.7.0
Group:		Development/Libraries
URL:		http://www.openexr.com/
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		openexr-01-templ.diff
Patch2:		openexr-02-cast.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEilmbase-devel
Requires: SFEilmbase

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lm"
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
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%dir %attr (0755,root,sys) %{_datadir}
%dir %attr (0755,root,other) %{_datadir}/doc
%dir %attr (0755,root,other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/doc/*

%changelog
* Sun Dec 19 2010 - Milan Jurik
- bump to 1.7.0, use Sun Studio
* Mon May  7 2007 - dougs@truemail.co.th
- Initial version
