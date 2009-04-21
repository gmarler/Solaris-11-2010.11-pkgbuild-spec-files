#
# spec file for package SFEbusybix
#
# includes module(s): busybox
#
%include Solaris.inc

Name:                    SFEbusybox
Summary:                 Tiny utilities for small and embedded systems  
Version:                 1.2.0
Source:                  http://www.busybox.net/downloads/busybox-1.2.0.tar.gz
Patch1:                  busybox-01.diff
URL:                     http://www.busybox.net
#SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SUNWcsu

%prep
%setup -q -n busybox-%version
%patch1 -p1


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`                                                   
if test "x$CPUS" = "x" -o $CPUS = 0; then                                                                     
    CPUS=1                                                                                                    
fi                                                                                                            
                                                                                                                  

gmake -j $CPUS                      

%install
mkdir -p $RPM_BUILD_ROOT/usr/bin                                                                                                                             
mv $RPM_BUILD_DIR/busybox-%version/busybox $RPM_BUILD_ROOT/usr/bin/      

%clean
rm -rf $RPM_BUILD_ROOT


%files                                                                                                                                                       
%dir %attr (0755, root, bin) %{_bindir}                                                                                                                      
%{_bindir}/*             

%changelog
* Tue Apr 21 2009 - Alexander R. Eremin eremin@milax.org
- Initial spec file. 
