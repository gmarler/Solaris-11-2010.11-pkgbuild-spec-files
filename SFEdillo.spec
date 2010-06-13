#
# spec file for package SFEdillo.spec
#
# includes module(s): dillo
#
%include Solaris.inc

%define src_name	dillo
%define src_url		http://www.dillo.org/download

Name:		SFEdillo
Summary:	Lightweight browser
Version:	2.2
Patch1:		dillo-01-dynarray.diff
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
URL:		http://www.dillo.org/
License:	GPLv3
Group:		Applications/Internet
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SFEfltk2-devel
Requires:	SFEfltk2

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

libtoolize --force

export CFLAGS="%optflags -I/usr/sfw/include"
export LDFLAGS="%_ldflags -Lusr/sfw/lib -Rusr/sfw/lib"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-ssl		\
            --enable-ipv6

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/%{src_name}

%files root
%defattr (-, root, sys)
%{_sysconfdir}

%changelog
* Sun Jun 13 2010 - Milan Jurik
- bump to 2.2
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Remove SUNWGtku (gtk 1.x) dependency to get module to build.
* Mon Apr 30 2007 - dougs@truemail.co.th
- Initial version
