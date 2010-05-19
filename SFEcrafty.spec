#
# spec file for package SFEcrafty
#
# includes module(s): crafty
#
%include Solaris.inc

Name:                    SFEcrafty
Summary:                 Crafty chess engine  
Version:                 23.2
Source:                  http://www.craftychess.com/crafty-%{version}.zip
URL: 			 http://www.craftychess.com/
#SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SUNWcsu

%prep
%setup -q -n crafty-%version 


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`                                                   
if test "x$CPUS" = "x" -o $CPUS = 0; then                                                                     
    CPUS=1                                                                                                    
fi                                                                                                            

make -j $CPUS solaris-gcc                      

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mv $RPM_BUILD_DIR/crafty-%version/crafty $RPM_BUILD_ROOT/%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* May 2010 - Gilles Dauphin
- %files update, move to %_bindir
* Sun May 09 2010 - Milan Jurik
- update to 23.2
* Wed Apr 15 2009 - Alexander R. Eremin eremin@milax.org
- Initial spec file.
