#
# spec file for package SFEcrafty
#
# includes module(s): crafty
#
%include Solaris.inc

Name:                    SFEcrafty
Summary:                 Crafty chess engine  
Version:                 23.0
Source:                  http://www.craftychess.com/crafty-23.0.zip
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
mkdir -p $RPM_BUILD_ROOT/usr/bin
mv $RPM_BUILD_DIR/crafty-%version/crafty $RPM_BUILD_ROOT/usr/bin/

%clean
rm -rf $RPM_BUILD_ROOT

%files                                                                                                        
%dir %attr (0755, root, bin) %{_bindir}                                                                       
%{_bindir}/*                                                                                                  

%changelog
%changelog                                                                                                    
* Wed Apr 15 2009 - Alexander R. Eremin eremin@milax.org                                                       
- Initial spec file.