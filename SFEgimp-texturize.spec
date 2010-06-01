#
# spec file for package SFEgimp-texturize
#
# includes module(s): gimp-texturize
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

Name:		SFEgimp-texturize
Summary:	Cross-platform development framework/toolkit
Group:		Applications/Graphics
Version:	2.1
Source:		%{sf_download}/gimp-texturize/texturize-%{version}_src.tgz
License:	GPLv2
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-img-editor-devel
Requires: SUNWgnome-img-editor
BuildRequires: SUNWgnome-common-devel

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}
%endif

%prep
%setup -q -n gimp-texturize

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="$optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%arch_ldadd %ldadd ${EXTRA_LDFLAGS}"
./configure \
    --prefix=%{_prefix}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
# FIXME
#mv $RPM_BUILD_ROOT%{_libdir}/locale $RPM_BUILD_ROOT%{_datadir}

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gimp/*/plug-ins/texturize
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gimp-texturize

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Jun 02 2010 - Milan Jurik
- bump to 2.1
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Change LDFLAGS to work for gcc.
* Sun Feb 11 2007 - laca@sun.com
- Initial spec
