#
# NoCopyright 2009 - Gilles Dauphin (from Fedora 10)
#

%include Solaris.inc

%ifarch x86_64
%define java_arch amd64
%else
%define java_arch %{_arch}
%endif

%define packname	MachineLearning
%define packrel		23

Name:			SFER-%{packname}
Version:		0.0
Summary:		CRAN Task View: Machine Learning & Statistical Learning
URL:			http://www.r-project.org/contrib/main/Descriptions/Matrix.html
License:		GPLv2+
SUNW_Copyright: 	%{name}.copyright
Group:			Applications/Math
#Source:			http://cran.cict.fr/src/contrib/Archive/%{packname}/%{packname}_%{version}-%{packrel}.tar.gz
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
Requires: SFER-Matrix
Requires: SFER-ctv
# TODO
#BuildRequires: tetex-latex, texinfo-tex 
BuildRequires: SUNWpng-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SFEreadline-devel
BuildRequires: SUNWncurses-devel
BuildRequires: SUNWj5dev

Meta(info.upstream):		cran.r-projet.org
Meta(info.maintainer):		Gilles Dauphin
Meta(info.repository_url):	ftp://cran.r-project.org/pub/

%description
Several add-on packages implement ideas and methods developed at the borderline
between computer science and statistics - this field of research is usually 
referred to as machine learning.

%prep
#%setup -q -n %{packname}-%{version}
%setup -q -c -n %{packname}
#%patch1 -p1 -b .filter-little-out

%build

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/R/library
export ac_cv_prog_CC="cc -m32"
%{_bindir}/R --no-save <<EOF
library(ctv)
install.views("MachineLearning",repos="http://cran.cict.fr/", lib="$RPM_BUILD_ROOT%{_libdir}/R/library")
update.packages(repos="http://cran.cict.fr/",ask=FALSE)
EOF


#%{_bindir}/R CMD INSTALL  %{packname} -l $RPM_BUILD_ROOT%{_libdir}/R/library 
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
#%dir %{_libdir}/R/library/%{packname}
#%{_libdir}/R/library/%{packname}/*
%dir %{_libdir}/R/library/BPHO
%dir %{_libdir}/R/library/CoxBoost
%dir %{_libdir}/R/library/ElemStatLearn
%dir %{_libdir}/R/library/GAMBoost
%dir %{_libdir}/R/library/MASS
%dir %{_libdir}/R/library/ROCR
%dir %{_libdir}/R/library/TWIX
%dir %{_libdir}/R/library/arules
%dir %{_libdir}/R/library/boost
%dir %{_libdir}/R/library/caret
%dir %{_libdir}/R/library/class
%dir %{_libdir}/R/library/e1071
%dir %{_libdir}/R/library/earth
%dir %{_libdir}/R/library/elasticnet
%dir %{_libdir}/R/library/gafit
%dir %{_libdir}/R/library/glmpath
%dir %{_libdir}/R/library/grplasso
%dir %{_libdir}/R/library/ipred
%dir %{_libdir}/R/library/klaR
%dir %{_libdir}/R/library/lars
%dir %{_libdir}/R/library/lasso2
%dir %{_libdir}/R/library/mboost
%dir %{_libdir}/R/library/mvpart
%dir %{_libdir}/R/library/nnet
%dir %{_libdir}/R/library/pamr
%dir %{_libdir}/R/library/party
%dir %{_libdir}/R/library/penalized
%dir %{_libdir}/R/library/predbayescor
%dir %{_libdir}/R/library/randomForest
%dir %{_libdir}/R/library/randomSurvivalForest
%dir %{_libdir}/R/library/rdetools
%dir %{_libdir}/R/library/relaxo
%dir %{_libdir}/R/library/rgenoud
%dir %{_libdir}/R/library/rpart
%dir %{_libdir}/R/library/spatial
%dir %{_libdir}/R/library/svmpath
%dir %{_libdir}/R/library/tree
%dir %{_libdir}/R/library/varSelRF
%{_libdir}/R/library/*/*

# TODO
# cut in packages
#     *  arules
#    * BayesTree
#    * boost
#    * BPHO
#    * caret
#    * CoxBoost
#    * e1071 (core)
#    * earth
#    * elasticnet
#    * ElemStatLearn
#    * gafit
#    * GAMBoost
#    * gbm (core)
#    * glmnet
#    * glmpath
#    * grplasso
#    * ipred
#    * kernlab (core)
#    * klaR
#    * lars
#    * lasso2
#    * mboost (core)
#    * mvpart
#    * pamr
#    * party
#    * penalized
#    * predbayescor
#    * randomForest (core)
#    * randomSurvivalForest
#    * rdetools
#    * relaxo
#    * rgenoud
#    * ROCR
#    * rpart (core)
#    * RWeka
#    * svmpath
#    * tgp
#    * tree
#    * TWIX
#    * varSelRF
#    * VR (core)
# THOSE are on ERROR
#> 1: In install.packages(pkgs, repos = views[[i]]$repository, ...) :
#>   installation of package 'rJava' had non-zero exit status
#> 2: In install.packages(pkgs, repos = views[[i]]$repository, ...) :
#>   installation of package 'BayesTree' had non-zero exit status
#> 3: In install.packages(pkgs, repos = views[[i]]$repository, ...) :
#>   installation of package 'gbm' had non-zero exit status
#> 4: In install.packages(pkgs, repos = views[[i]]$repository, ...) :
#>   installation of package 'glmnet' had non-zero exit status
#> 5: In install.packages(pkgs, repos = views[[i]]$repository, ...) :
#>   installation of package 'kernlab' had non-zero exit status
#> 6: In install.packages(pkgs, repos = views[[i]]$repository, ...) :
#>   installation of package 'tgp' had non-zero exit status
#> 7: In install.packages(pkgs, repos = views[[i]]$repository, ...) :
#>   installation of package 'RWeka' had non-zero exit status
#> > update.packages(repos="http://cran.cict.fr/",ask=FALSE)


%changelog
* Thu Apr 22 2009 - Gilles Dauphin
- inital config 
