#
# spec file for package SFEre2c
#

%include Solaris.inc
Name:                    SFEre2c
Summary:                 re2c - tool for writing very fast and very flexible scanners
URL:                     http://re2c.org/
Version:                 0.13.5
Source:                  %{sf_download}/re2c/re2c-%{version}.tar.gz


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

#TODO: BuildReqirements:
#TODO: Reqirements:

%include default-depend.inc



%prep
%setup -q -n re2c-%version

%build

# CXXFLAGS='-library=stlport4')

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}   \
            --disable-static


make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%changelog
* Sat Mar 12 2009  - Thomas Wagner
- bump to 0.13.5
* Sat May 12 2007  - Thomas Wagner
- Initial spec
