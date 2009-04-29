#
# NoCopyright 2009 - Gilles Dauphin 
#

%include Solaris.inc

%ifarch x86_64
%define java_arch amd64
%else
%define java_arch %{_arch}
%endif

%define packname	e1071
%define packrel		19

Name:			SFER-%{packname}
Version:		1.5
Summary:		Misc Functions of the Department of Statistics (e1071), TU Wien
URL:			http://cran.cict.fr/web/packages/e1071/index.html
License:		GPLv2+
SUNW_Copyright: 	%{name}.copyright
Group:			Applications/Math
Source:			http://cran.cict.fr/src/contrib/%{packname}_%{version}-%{packrel}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-build
Requires: SPROcc
Requires: SPROcmpl
Requires: SPROf90
Requires: SPROftool
Requires: SUNWpng
Requires: SUNWjpg
Requires: SFEreadline
Requires: SFEblas
Requires: SUNWTcl
Requires: SUNWncurses
Requires: SUNWpcre
Requires: SUNWzlib
Requires: SUNWTk
Requires: SFElapack
Requires: SUNWxwrtl
Requires: SUNWbzip
Requires: SUNWgnome-base-libs
Requires: SUNWTiff
Requires: SUNWj5rt
Requires: SFER
# TODO
#BuildRequires: tetex-latex, texinfo-tex 
BuildRequires: SUNWpng-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SFEreadline-devel
BuildRequires: SUNWncurses-devel
BuildRequires: SUNWj5dev

Meta(info.upstream):		cran.cict.fr
Meta(info.maintainer):		Gilles Dauphin
Meta(info.repository_url):	http://cran.cict.fr/src/contrib

%description
Functions for latent class analysis, short time Fourier transform, fuzzy clustering,
support vector machines, shortest path computation, bagged clustering, 
naive Bayes classifier, ...


%prep
#%setup -q -n %{packname}-%{version}
%setup -q -c -n %{packname}
#%patch1 -p1 -b .filter-little-out

%build

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/R/library
%{_bindir}/R CMD INSTALL  %{packname} -l $RPM_BUILD_ROOT%{_libdir}/R/library 
# Clean up in advance of check
#test -d %{packname}/src && (cd %{packname}/src; rm -f *.o *.so)
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
- inital config 
