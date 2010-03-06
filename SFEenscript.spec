#
# spec file for package SFEenscript.spec
#

%include Solaris.inc

%define version 1.6.5
# Letter fits on A4. The reverse is not true.
# The default in this spec is letter for this reason.
# To build with A4 as the default:
# pkgtool build SFEenscript --define 'media a4'
%if %{!?media:1}
	%define media %{!?media:"letter"}
%endif

Name:                    SFEenscript
Summary:                 enscript
Version:                 %{version}
Source:                  http://ftp.gnu.org/gnu/enscript/enscript-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SUNWperl584core
Requires:                SUNWlibmsr
Requires:                SUNWflexruntime
BuildRequires:           SUNWflexlex

Requires:                %{name}-root

%package root
Summary:                 SFEenscript - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -c
cd %sname-%version

%build
cd %sname-%version
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-threads=solaris    \
            --with-media=%{media}
make

%install
rm -rf $RPM_BUILD_ROOT
cd %sname-%version
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_infodir}

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/enscript
#%attr (0755, root, bin) %{_infodir}
%attr (0755, root, bin) %{_mandir}/man1

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%changelog
* Sun Mar 05 2010 - matt@greenviolet.net
- Initial spec file.
