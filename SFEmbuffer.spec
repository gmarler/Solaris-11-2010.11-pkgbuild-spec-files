#
# spec file for package SFEmbuffer
#

%include Solaris.inc
Name:                    SFEmbuffer
Summary:                 mbuffer - tool for extra buffering pipes
URL:                     http://www.maier-komor.de/software/mbuffer
Version:                 20101230
Source:                  http://www.maier-komor.de/software/mbuffer/mbuffer-%{version}.tgz


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires: SUNWopenssl-include
Requires: SUNWopenssl-libraries

%include default-depend.inc


%prep
%setup -q -n mbuffer-%version

%build

perl -w -pi.bak -e "s,^#\!\s*/bin/sh,#\!/usr/bin/bash," configure
./configure --prefix=%{_prefix}  


make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# for older pkgbuild/pkgtool
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README ChangeLog INSTALL NEWS AUTHORS LICENSE
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%changelog
* Sun Jan  1 2011  - Thomas Wagner
- bump to 20101230
- change shell in configure, remove obsolete configure switches
* Tue Jan 27 2009  - Thomas Wagner
- Initial spec
