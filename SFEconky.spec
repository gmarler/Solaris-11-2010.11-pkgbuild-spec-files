#
# spec file for package SFEconky
#
# includes module(s): conky
#
%include Solaris.inc

Name:                    SFEnetsurf
Summary:                 Small gtk web browser  
Version:                 2.0
Source:                  http://www.netsurf-browser.org/downloads/releases/netsurf-2.0-src.tar.gz
Patch1:                  netsurf-01.diff
URL:                     http://www.netsurf-browser.org
#SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%define svn_url1 	svn://svn.netsurf-browser.org/trunk/libnsbmp
%define svn_url2 	svn://svn.netsurf-browser.org/trunk/libnsgif
%define svn_url3 	svn://svn.netsurf-browser.org/trunk/libparserutils
%define svn_url4 	svn://svn.netsurf-browser.org/trunk/hubbub
%define svn_url5 	svn://svn.netsurf-browser.org/trunk/libharu

%include default-depend.inc

Requires: SUNWcsu

%prep
%setup -q -n conky-%version
%patch1 -p1



export CFLAGS="%optflags -I/usr/X11/include"
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib -lX11"

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`                                                   
if test "x$CPUS" = "x" -o $CPUS = 0; then                                                                     
    CPUS=1                                                                                                    
fi                                                                                                            
                                                                                                                  

./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --x-includes=/usr/X11/include \
            --x-libraries=/usr/X11/lib

make -j $CPUS                      

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, sys) /usr/share

%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/conky
%{_sysconfdir}/conky/*


%changelog
* Thu Apr 9 2009 - Alexander R. Eremin eremin@milax.org
- Initial spec file.
