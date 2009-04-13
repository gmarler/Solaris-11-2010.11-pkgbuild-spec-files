#
# spec file for package SFEconky
#
# includes module(s): conky
#
%include Solaris.inc

Name:                    SFEconky
Summary:                 Light-weight system monitor for X  
Version:                 1.5.1
Source:                  http://prdownloads.sourceforge.net/conky/conky-1.5.1.tar.gz
Patch1:                  Conky-01.diff
URL:                     http://conky.sourceforge.net/
#SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

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
mkdir -p $RPM_BUILD_ROOT/etc/conky
cp data/conky.conf $RPM_BUILD_ROOT/etc/conky.conf

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
%attr(0644, root, sys) %{_sysconfdir}/data/conky.conf
%dir %attr (0755, root, sys) %{_sysconfdir}/conky
%{_sysconfdir}/conky/*


%changelog
* Thu Apr 9 2009 - Alexander R. Eremin eremin@milax.org
- Initial spec file.
