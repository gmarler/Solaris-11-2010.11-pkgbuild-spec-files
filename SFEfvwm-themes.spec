#
# spec file for package SFEfvwm.spec
#
# includes module(s): fvwm
#
%include Solaris.inc

%include base.inc
%use themes = fvwm-themes.spec

Name:                   SFEfvwm-themes
Summary:                %{themes.summary}
Version:                %{themes.version}
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEfvwm

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%{base_arch}
%themes.prep -d %name-%version/%{base_arch}

%build
%themes.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%themes.install -d %name-%version/%{base_arch}

%post
( echo 'fvwm-themes-config --site --reset';
  echo 'fvwm-themes-menuapp --site --build-menus --remove-popup';
  echo 'fvwm-themes-images --ft-install --gnome';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_mandir}
%dir %attr (0755, root, sys) %{_datadir}
%defattr (-, root, other)
%{_datadir}/fvwm

%changelog
* Aug 2009 - Gilles Dauphin
- /usr/share/fvwm attribute is same as SFEfvwm.spec
* Fri Apr 27 2006 - dougs@truemail.co.th
- Initial version
