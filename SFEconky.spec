#
# spec file for package SFEconky
#
# includes module(s): conky
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

Name:                    SFEconky
Summary:                 Light-weight system monitor for X  
Version:                 1.5.1
Source:                  http://prdownloads.sourceforge.net/conky/conky-1.5.1.tar.gz
Patch1:                  conky-01.diff
URL:                     http://conky.sourceforge.net/
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SUNWcsu
BuildRequires: SUNWgcc

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
export CC=/usr/sfw/bin/gcc

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
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/conky
%{_sysconfdir}/conky/*


%changelog
* Tue Apr 06 2010 - Milan Jurik
- small cleanup
* Thu Apr 9 2009 - Alexander R. Eremin eremin@milax.org
- Initial spec file.
