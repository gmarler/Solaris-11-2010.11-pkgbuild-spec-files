#
# spec file for package SFEmbuffer
#

%include Solaris.inc
Name:                    SFEmbuffer
Summary:                 mbuffer - tool for extra buffering pipes
URL:                     http://www.maier-komor.de/software/mbuffer
Version:                 20081113
Source:                  http://www.maier-komor.de/software/mbuffer/mbuffer-%{version}.tgz


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires: SUNWopenssl-include
Requires: SUNWopenssl-libraries

%include default-depend.inc


%prep
%setup -q -n mbuffer-%version

%build


./configure --prefix=%{_prefix}  \
            --disable-debug      \
            --disable-static


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
%doc README ChangeLog INSTALL NEWS AUTHORS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%changelog
* Tue Jan 27 2009  - Thomas Wagner
- Initial spec
