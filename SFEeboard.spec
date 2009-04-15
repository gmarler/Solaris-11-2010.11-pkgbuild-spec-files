#
# spec file for package SFEeboard
#
# includes module(s): eboard
#
%include Solaris.inc

Name:                    SFEeboard
Summary:                 GTK+ chess interface for Unix-like systems  
Version:                 1.1.1
Source:                  http://prdownloads.sourceforge.net/eboard/eboard-1.1.1.tar.bz2
Patch1:                  eboard-01.diff
URL:                     http://www.bergo.eng.br/eboard/
#SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SUNWcsu

%prep
%setup -q -n eboard-%version
%patch1 -p1



export CFLAGS="%optflags -I/usr/X11/include"
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib -lX11"

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`                                                   
if test "x$CPUS" = "x" -o $CPUS = 0; then                                                                     
    CPUS=1                                                                                                    
fi                                                                                                            
                                                                                                                  

./configure --prefix=%{_prefix} \
            --datadir=%{_datadir} \
	    --mandir=%{_mandir}

gmake -j $CPUS                      

%install
gmake install DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT/usr/man $RPM_BUILD_ROOT/usr/share/man 
%clean
rm -rf $RPM_BUILD_ROOT

%files                                                                                                        
%dir %attr (0755, root, bin) %{_bindir}                                                                       
%{_bindir}/*                                                                                                  
%dir %attr (0755, root, sys) %{_datadir}                                                                      
%dir %attr (0755, root, other) %{_datadir}/eboard                                                             
%{_datadir}/eboard/*                                                                                             
%defattr (-, root, other)                        
%dir %attr(0755, root, bin) %{_mandir}                                                                        
%{_mandir}/man*/*   

%changelog
%changelog                                                                                                    
* Wed Apr 15 2009 - Alexander R. Eremin eremin@milax.org                                                       
- Initial spec file.