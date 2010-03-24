#
# spec file for package SFExosd
#

# Note: builds only with  gcc !

%include Solaris.inc
Name:                    SFExosd
Summary:                 xosd - simple library to display shaped text on X Display
Group:                   Utility
URL:                     http://freshmeat.net/redir/xosd/12072/url_homepage/libxosd
Version:                 2.2.14
Source:                  http://downloads.sourceforge.net/project/libxosd/libxosd/xosd-%{version}/xosd-%{version}.tar.gz
Patch1:			 xosd-01-configure-with-bash.diff

SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

#TODO: BuildReqirements:
#TODO: Reqirements:

%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n xosd-%version
%patch1 -p1

%build


CC=/usr/sfw/bin/gcc CXX=/usr/sfw/bin/g++ ./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}   \
            --disable-static


make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#empty directories (xmms):
test -d $RPM_BUILD_ROOT/opt && rm -r $RPM_BUILD_ROOT/opt

rm -r $RPM_BUILD_ROOT/%{_libdir}/*la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, other) %{_datadir}/xosd
%{_datadir}/xosd/*
%dir %attr (0755, root, other) %{_docdir}

%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Mars 24 2010 - Gilles Dauphin
- download URL
* Sat Feb 21 2009 - Thomas Wagner
- add patch1 configure with bash otherwise shell syntax error around BMP_GENERAL_PLUGIN_DIR=$
- fix %{_docdir} attributes in %files
* Tue Dec 23 2008 - Thomas Wagner
- %doc adjusted - pkgbuild starting with 1.3.3 honours %doc and all files must be listed exactly
* Tue Dec 16, 2008 - Gilles Dauphin
- comment %doc , files does not exist
* Thu May 31 2007  - Thomas Wagner
- force compiler to gcc.
- conditional rm -r $RPM_BUILD_ROOT/opt (really needed?)
- builds only with gcc
* Thu Apr 07 2007  - Thomas Wagner
- Initial spec
