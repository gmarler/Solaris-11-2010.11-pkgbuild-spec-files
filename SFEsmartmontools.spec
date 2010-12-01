#
# spec file for package SFEsmartmontools.spec
#
%include Solaris.inc

%define src_name	smartmontools
%define src_url		%{sf_download}/%{src_name}

Name:                   SFEsmartmontools
Summary:                S.M.A.R.T. monitoring tools
Version:                5.40
Group:                  Utility
License:                GPLv2
URL:                    http://smartmontools.sourceforge.net/
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_prefix}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SUNWhea
Requires: %name-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_basedir}			\
	    --sysconfdir=%{_sysconfdir}			\
	    --sbindir=%{_sbindir}			\
	    --datadir=%{_datadir}			\
	    --docdir=%{_docdir}				\
	    --mandir=%{_mandir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d $RPM_BUILD_ROOT%{_sysconfdir}/init.d
rmdir $RPM_BUILD_ROOT%{_sysconfdir}/rc.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1m
%{_mandir}/man1m/*
%dir %attr(0755, root, bin) %{_mandir}/man4
%{_mandir}/man4/*
%{_datadir}/%{src_name}

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/init.d
%{_sysconfdir}/smartd.conf

%changelog
* Wed Dec 01 2010 - Milan Jurik
- bump to 5.40
* Tue Jun 15 2010 - Milan Jurik
- bump to 5.39.1
* Thu May 29 2008 - Albert Lee <trisk@acm.jhu.edu>
- Initial spec
