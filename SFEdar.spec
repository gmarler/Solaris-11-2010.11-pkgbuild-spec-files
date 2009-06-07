
# spec file for package SFEdar
#

##TODO## check if patch1 is still needed and if  -D__EXTENSIONS__ -DHAVE_GETOPT_IN_UNISTD_H=1 is enough

%define src_name dar

%include Solaris.inc

%define cc_is_gcc 1
%define _gpp /usr/sfw/bin/g++
%include base.inc

Name:                    SFEdar
Summary:                 dar - backs up directory trees and files to disks, floppy, CD-R(W), DVD-R(W), zip, jazz, etc.
URL:                     http://dar.linux.free.fr/
Version:                 2.3.9
Source:                  %{sf_download}/dar/dar-%{version}.tar.gz
Patch1:			dar-01-configure-detect-getopt-in-unistd.h.diff



SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires: SFEgcc
BuildRequries: SUNWbzip
Requires: SFEgccruntime
Requires: SUNWperl584core
Requires: SUNWbash
Requries: SUNWbzip

%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif



%prep
%setup -q -n dar-%version
%patch1 -p1

%build


export CFLAGS="%{optflags} -I%{gnu_inc} -D__EXTENSIONS__ -DHAVE_GETOPT_IN_UNISTD_H=1"
export CXXFLAGS="%{cxx_optflags} -I%{gnu_inc} -D__EXTENSIONS__ -DHAVE_GETOPT_IN_UNISTD_H=1"

#export LD=ld-wrapper
export LDFLAGS="%{_ldflags} %{gnu_lib_path}"

export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}   \
            --disable-gnugetopt \
            --enable-examples    \
            --disable-dar-static \
            --disable-static



make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/*la

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc ABOUT-NLS AUTHORS COPYING ChangeLog INSTALL LICENSING_EXCEPTION_FOR_OPENSSL NEWS README THANKS TODO
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%dir %attr (0755, root, bin) %{_includedir}
#%attr(755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{src_name}/*
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%if %build_l10n
%files l10n
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Sun Jun 07 2009 - Thomas Wagner
- C++ errors, switched to gcc(4.x) (no deep check why SunStudio C++ does not compile)
* Mon Jun 01 2009 - Thomas Wagner
- Initial spec
