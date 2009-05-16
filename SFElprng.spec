#
# spec file for package SFElprng
#

%define src_name        lprng
%include Solaris.inc

%define lprngsubdir %{src_name}

%define option_with_gnu_pathlayout %{?_with_gnu_pathlayout:1}%{?!_with_gnu_pathlayout:0}

# choose from /usr/gnu/bin and /usr/lprng/bin, 
# (which is similar to SUNWcupsu with /usr/lib/cups/bin)
# note: binaries live in /usr/gnu/bin or /usr/lib/lprng/bin

# note: path layout may chance in the future, so check them when reinstalling SFElprng

# note: prepared to fit into the print-system-select system for solaris-print and cups-print

%if %option_with_gnu_pathlayout
%include usr-gnu.inc
%else
%define _subdir     %{lprngsubdir}
%define _prefix	    %{_basedir}/%{_subdir}
%define _bindir     %{_basedir}/lib/%{_subdir}/bin
%define _sbindir    %{_basedir}/lib/%{_subdir}/sbin
%define _libdir     %{_basedir}/lib/%{_subdir}
%define _libexecdir %{_basedir}/lib/%{_subdir}
%define _datadir    %{_basedir}/%{_subdir}/share
##%define _sysconfdir	   /etc/%{_subdir}
%define _localstatedir     /var/%{_subdir}
%endif




Name:                   SFE%{src_name}
Summary:                LPRng - enhanced printer spooler RFC1179
URL:                    http://www.lprng.com/
Version:                3.8.A
Source:                 http://%{sf_mirror}/sourceforge/%{src_name}/LPRng-%{version}.tar.gz
Source2:                lprng.xml

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%include default-depend.inc

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc



%prep
%setup -q -n LPRng-%version

#SMF manifest
cp %{SOURCE2} .
perl -w -pi.bak -e "s,\@\@LPRNGSBINDIR\@\@,%{_sbindir}," lprng.xml
perl -w -pi.bak -e "s,\@\@LPRNGMANPATH\@\@,%{_mandir}," lprng.xml



%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}    \
            --bindir=%{_bindir}    \
            --sbindir=%{_sbindir}  \
            --mandir=%{_mandir}    \
            --sysconfdir=%{_sysconfdir} \
            --libexecdir=%{_libexecdir}      \
            --datadir=%{_datadir}   \
            --disable-static

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/spool/lpd

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp lprng.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}


%post -n SFElprng-root

if [ -f /lib/svc/share/smf_include.sh ] ; then
    . /lib/svc/share/smf_include.sh
    smf_present
    if [ $? -eq 0 ]; then
       /usr/sbin/svccfg import /var/svc/manifest/site/lprng.xml
    fi
fi

exit 0

%preun -n SFElprng-root
if [  -f /lib/svc/share/smf_include.sh ] ; then
    . /lib/svc/share/smf_include.sh
    smf_present
    if [ $? -eq 0 ]; then
       if [ `svcs  -H -o STATE svc:/site/lprng:default` != "disabled" ]; then
           svcadm disable svc:/site/lprng:default
       fi
    fi
fi


%postun -n SFElprng-root

if [ -f /lib/svc/share/smf_include.sh ] ; then
    . /lib/svc/share/smf_include.sh
    smf_present
    if [ $? -eq 0 ] ; then
       /usr/sbin/svccfg export svc:/site/lprng:default > /dev/null 2>&1
       if [ $? -eq 0 ] ; then
           /usr/sbin/svccfg delete -f svc:/site/lprng:default
       fi
    fi
fi
exit 0

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, bin)
%doc README ChangeLog INSTALL NEWS TODO ABOUT-NLS.LPRng CHANGES CONTRIBUTORS COPYRIGHT KERBEROS_configuration LICENSE MIT_configure README.SSL.SECURITY STANDARD_configuration 
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/filters/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/printcap.sample
%defattr (-, root, bin)
%attr (0755, root, bin) %dir %{_sysconfdir}/lpd
%{_sysconfdir}/lpd/*
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%{_localstatedir}/*
%class(manifest) %attr(0444, root, sys)/var/svc/manifest/site/lprng.xml



%changelog
* Sat May 16 2009 - Thomas Wagner
- adjust %doc section
* Sun Oct 18 2008  - Thomas Wagner
- default to gnu paths
* Sun Oct 13 2008  - Thomas Wagner
- Initial spec
