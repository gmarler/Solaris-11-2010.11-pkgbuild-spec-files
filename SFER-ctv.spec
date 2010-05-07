#
# NoCopyright 2009 - Gilles Dauphin (from Fedora 10)
#

%include Solaris.inc

%ifarch x86_64
%define java_arch amd64
%else
%define java_arch %{_arch}
%endif

%define packname	ctv
%define packrel		6

Name:			SFER-%{packname}
Version:		0.5
Summary:		CRAN Task Views
URL:			http://cran.cict.fr/web/packages/ctv/index.html
License:		GPLv2+
SUNW_Copyright: 	%{name}.copyright
Group:			Applications/Math
Source:			http://cran.cict.fr/src/contrib/%{packname}_%{version}-%{packrel}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-build
Requires: SFER
# TODO
#BuildRequires: tetex-latex, texinfo-tex 

Meta(info.upstream):		cran.r-projet.org
Meta(info.maintainer):		Gilles Dauphin
Meta(info.repository_url):	ftp://cran.r-project.org/pub/

%description
This package accompanies J. Fox, An R and S-PLUS Companion to Applied
Regression, Sage, 2002. The package contains mostly functions for applied
regression, linear models, and generalized linear models, with an emphasis on
regression diagnostics, particularly graphical diagnostic methods.  There are
also some utility functions. With some exceptions, it does not duplicate
capabilities in the basic distribution of R, nor in widely used packages.
Where relevant, the functions in car are consistent with na.action = na.omit
or na.exclude.


%prep
#%setup -q -n -c %{packname}-%{version}
%setup -q -c -n  %{packname}
#%patch1 -p1 -b .filter-little-out

%build

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/R/library
%{_bindir}/R CMD INSTALL  %{packname} -l $RPM_BUILD_ROOT%{_libdir}/R/library 
# Clean up in advance of check
test -d %{packname}/src && (cd %{packname}/src; rm -f *.o *.so)
rm -rf $RPM_BUILD_ROOT%{_libdir}/R/library/R.css

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755, root, sys)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %dir %{_libdir}/R
%dir %attr (0755, root, bin) %{_libdir}/R/library
#%{_libdir}/R/library/R.css
%dir %{_libdir}/R/library/%{packname}
%{_libdir}/R/library/%{packname}/*


%changelog
* Thu Apr 22 2009 - Gilles Dauphin
- inital config (from fedora)
