#
# spec file for package SFExmlto
#
# includes module(s): xmlto
#
%include Solaris.inc

Name:                    SFExmlto
Summary:                 xmlto - converts an XML file into a specified format
Group:                   Utility
Version:                 0.0.23
URL:                     http://fedorahosted.org/xmlto/
Source:                  http://fedorahosted.org/releases/x/m/xmlto/xmlto-%{version}.tar.bz2
Patch1:                  xmlto-01-find.diff
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlxsl
Requires: SUNWlxml
Requires: SUNWgnome-xml-share
Requires: SUNWgnome-xml-root
Requires: SUNWw3m
Requires: SFEgnugetopt

%prep
rm -rf %name-%version
%setup -q -n xmlto-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export GETOPT="/usr/gnu/bin/getopt"
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_datadir}/xmlto/xsl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/xmlto
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Sun Sep 19 2010 - Milan Jurik
- bump to 0.0.23
* Sat Aug 16 2008 - nonsea@users.sourceforge.net
- Add Requires to SUNWgnome-xml-root and SUNWw3m
* Tue Jun 17 2008 - simon.zheng@sun.com
- Add patch 01-find.diff, remove depedency of
  GNU find utility.
* Sun Mar 02 2008 - simon.zheng@sun.com
- By default, Solaris has already installed package 
  SUNWgnugetopt. Let's depend on it instead of
  SFEgetopt.
* Thu Feb 21 2008 - nonsea@users.sourceforge.net
- Bump to 0.0.20
* Tue Feb 13 2007 - laca@sun.com
- create
