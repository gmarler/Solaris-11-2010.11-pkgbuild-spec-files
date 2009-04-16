#
# NoCopyright 2009 - Gilles Dauphin (from Fedora 10)
#

%include Solaris.inc

%ifarch x86_64
%define java_arch amd64
%else
%define java_arch %{_arch}
%endif

%define src_version	2.8.1
%define src_name	R

Name:			SFER
Version:		2.8.1
Summary:		A language for data analysis and graphics
URL:			http://www.r-project.org
License:		GPLv2+
Group:			Applications/Math
Source:			ftp://cran.r-project.org/pub/R/src/base/R-2/R-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{src_version}-build
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
# TODO
#BuildRequires: tetex-latex, texinfo-tex 
BuildRequires: SUNWpng-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SFEreadline-devel
BuildRequires: SUNWncurses-devel
BuildRequires: SUNWj5dev

%description
R is a language and environment for statistical computing and graphics. 
R is similar to the award-winning S system, which was developed at 
Bell Laboratories by John Chambers et al. It provides a wide 
variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

%prep
%setup -q -n %{src_name}-%{version}
#%patch1 -p1 -b .filter-little-out

%build
# Add PATHS to Renviron for R_LIBS
echo 'R_LIBS=${R_LIBS-'"'%{_libdir}/R/library:%{_datadir}/R/library'"'}' >> etc/Renviron.in

export R_PDFVIEWER="%{_bindir}/xdg-open"
export R_PRINTCMD="lpr"
export R_BROWSER="%{_bindir}/xdg-open"

case "%{_target_cpu}" in
      x86_64|mips64|ppc64|powerpc64|sparc64|s390x)
          #export CC="gcc -m64"
          #export CXX="g++ -m64"
          export CC="cc -m64"
          export CXX="CC -m64"
          export F77="f95 -m64"
          export FC="f95 -m64"
      ;;
      ia64|alpha|sh*)
          export CC="gcc"
          export CXX="g++"
          export F77="f95"
          export FC="f95"
      ;;
      *)
          #export CC="gcc -m32"
          #export CXX="g++ -m32"
          export CC="cc -m32"
	 # because of foreign -Wno-long-long !!! Argh :(
          export ac_cv_prog_CC="cc -m32"
          export CXX="CC -m32"
          export F77="f95 -m32"
          export FC="f95 -m32"
      ;;    
esac

export FCFLAGS="%{optflags}"
( ./configure \
--prefix=%{_prefix}                 \
    --libexecdir=%{_libexecdir}         \
    --mandir=%{_mandir}                 \
    --datadir=%{_datadir}               \
    --infodir=%{_datadir}/info          \
    --with-system-zlib --with-system-bzlib --with-system-pcre \
    --with-lapack \
    --with-tcl-config=%{_libdir}/tclConfig.sh \
    --with-tk-config=%{_libdir}/tkConfig.sh \
    --enable-R-shlib \
    --with-iconv=no \
    rdocdir=%{_docdir}/R-%{version} \
    rincludedir=%{_includedir}/R \
    rsharedir=%{_datadir}/R) \
 | grep -A30 'R is now' - > CAPABILITIES
make 
(cd src/nmath/standalone; make)
#make check-all
make pdf
make info

#  TODO
# Convert to UTF-8
#for i in doc/manual/R-intro.info doc/manual/R-FAQ.info-1 doc/FAQ doc/manual/R-exts.info-1; do
#  iconv -f iso-8859-1 -t utf-8 -o $i{.utf8,}
#  mv $i{.utf8,}
#done

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install install-info install-pdf
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir.old
install -p CAPABILITIES ${RPM_BUILD_ROOT}%{_docdir}/R-%{version}

#Install libRmath files
(cd src/nmath/standalone; make install DESTDIR=${RPM_BUILD_ROOT})

mkdir -p $RPM_BUILD_ROOT%{_datadir}/R/library

# Fix exec bits
chmod +x $RPM_BUILD_ROOT%{_datadir}/R/sh/help-links.sh $RPM_BUILD_ROOT%{_datadir}/R/sh/echo.sh
chmod -x $RPM_BUILD_ROOT%{_libdir}/R/library/mgcv/CITATION ${RPM_BUILD_ROOT}%{_docdir}/R-%{version}/CAPABILITIES

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755, root, sys)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/R
%{_bindir}/Rscript
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/info
%dir %attr (0755, root, bin) %{_datadir}/man
%dir %attr (0755, root, bin) %{_datadir}/man/man1
%dir %attr (0755, root, other) %{_datadir}/R
%dir %attr (0755, root, other) %{_datadir}/R/encodings
%{_datadir}/R/encodings/*
%dir %attr (0755, root, other) %{_datadir}/R/java
%{_datadir}/R/java/*
%dir %attr (0755, root, other) %{_datadir}/R/library
%dir %attr (0755, root, other) %{_datadir}/R/licenses
%{_datadir}/R/licenses/*
%dir %attr (0755, root, other) %dir %{_datadir}/R/locale
%dir %attr (0755, root, other) %{_datadir}/R/locale/de
%dir %attr (0755, root, other) %{_datadir}/R/locale/en*
%dir %attr (0755, root, other) %{_datadir}/R/locale/es*
%dir %attr (0755, root, other) %{_datadir}/R/locale/fr
%dir %attr (0755, root, other) %{_datadir}/R/locale/it
%dir %attr (0755, root, other) %{_datadir}/R/locale/ja
%dir %attr (0755, root, other) %{_datadir}/R/locale/ko
%dir %attr (0755, root, other) %{_datadir}/R/locale/pt*
%dir %attr (0755, root, other) %{_datadir}/R/locale/ru
%dir %attr (0755, root, other) %{_datadir}/R/locale/zh*
%{_datadir}/R/locale/*/*
%dir %attr (0755, root, other) %{_datadir}/R/make
%{_datadir}/R/make/*
%dir %attr (0755, root, other) %{_datadir}/R/perl
%{_datadir}/R/perl/*
%dir %attr (0755, root, other) %{_datadir}/R/R
%{_datadir}/R/R/*
%dir %attr (0755, root, other) %{_datadir}/R/sh/
%{_datadir}/R/sh/*
%dir %attr (0755, root, other) %{_datadir}/R/texmf/
%{_datadir}/R/texmf/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libRmath.so
%{_libdir}/libRmath.a
%dir %attr (0755, root, bin) %dir %{_libdir}/R
%dir %attr (0755, root, bin) %{_libdir}/R/bin
%{_libdir}/R/bin/*
%dir %attr (0755, root, sys) %{_libdir}/R/etc
%{_libdir}/R/etc/*
%dir %attr (0755, root, bin) %{_libdir}/R/lib
%{_libdir}/R/lib/*
# Have to break this out for the translations
%dir %attr (0755, root, bin) %{_libdir}/R/library
%{_libdir}/R/library/R.css
# base
%dir %{_libdir}/R/library/base/
%{_libdir}/R/library/base/CITATION
%{_libdir}/R/library/base/CONTENTS
%{_libdir}/R/library/base/demo/
%{_libdir}/R/library/base/DESCRIPTION
%{_libdir}/R/library/base/help/
%{_libdir}/R/library/base/html/
%{_libdir}/R/library/base/INDEX
%{_libdir}/R/library/base/latex/
%{_libdir}/R/library/base/man/
%{_libdir}/R/library/base/Meta/
%dir %{_libdir}/R/library/base/po/
%{_libdir}/R/library/base/po/de/
%{_libdir}/R/library/base/po/en*/
%{_libdir}/R/library/base/po/fr/
%{_libdir}/R/library/base/po/it/
%{_libdir}/R/library/base/po/ja/
%{_libdir}/R/library/base/po/ko/
%{_libdir}/R/library/base/po/pt*/
%{_libdir}/R/library/base/po/ru/
%{_libdir}/R/library/base/po/zh*/
%{_libdir}/R/library/base/R/
%{_libdir}/R/library/base/R-ex/
# boot
%dir %{_libdir}/R/library/boot/
%{_libdir}/R/library/boot/CITATION
%{_libdir}/R/library/boot/CONTENTS
%{_libdir}/R/library/boot/data/
%{_libdir}/R/library/boot/DESCRIPTION
%{_libdir}/R/library/boot/help/
%{_libdir}/R/library/boot/html/
%{_libdir}/R/library/boot/INDEX
%{_libdir}/R/library/boot/latex/
%{_libdir}/R/library/boot/man/
%{_libdir}/R/library/boot/Meta/
%{_libdir}/R/library/boot/NAMESPACE
%dir %{_libdir}/R/library/boot/po/
%{_libdir}/R/library/boot/po/en*/
%{_libdir}/R/library/boot/po/fr/
%{_libdir}/R/library/boot/po/ru/
%{_libdir}/R/library/boot/R/
%{_libdir}/R/library/boot/R-ex/
# class
%dir %{_libdir}/R/library/class/
%{_libdir}/R/library/class/CITATION
%{_libdir}/R/library/class/CONTENTS
%{_libdir}/R/library/class/DESCRIPTION
%{_libdir}/R/library/class/help/
%{_libdir}/R/library/class/html/
%{_libdir}/R/library/class/INDEX
%{_libdir}/R/library/class/latex/
%{_libdir}/R/library/class/libs/
%{_libdir}/R/library/class/LICENCE
%{_libdir}/R/library/class/man/
%{_libdir}/R/library/class/Meta/
%{_libdir}/R/library/class/NAMESPACE
%{_libdir}/R/library/class/NEWS
%dir %{_libdir}/R/library/class/po/
%{_libdir}/R/library/class/po/en*/
%{_libdir}/R/library/class/po/fr/
%{_libdir}/R/library/class/R/
%{_libdir}/R/library/class/R-ex/
# cluster
%dir %{_libdir}/R/library/cluster/
%{_libdir}/R/library/cluster/CITATION
%{_libdir}/R/library/cluster/CONTENTS
%{_libdir}/R/library/cluster/data/
%{_libdir}/R/library/cluster/DESCRIPTION
%{_libdir}/R/library/cluster/help/
%{_libdir}/R/library/cluster/html/
%{_libdir}/R/library/cluster/INDEX
%{_libdir}/R/library/cluster/latex/
%{_libdir}/R/library/cluster/libs/
%{_libdir}/R/library/cluster/man/
%{_libdir}/R/library/cluster/Meta/
%{_libdir}/R/library/cluster/NAMESPACE
%{_libdir}/R/library/cluster/R/
%{_libdir}/R/library/cluster/R-ex/
# codetools
%dir %{_libdir}/R/library/codetools/
%{_libdir}/R/library/codetools/CONTENTS
%{_libdir}/R/library/codetools/DESCRIPTION
%{_libdir}/R/library/codetools/help/
%{_libdir}/R/library/codetools/html/
%{_libdir}/R/library/codetools/INDEX
%{_libdir}/R/library/codetools/latex/
%{_libdir}/R/library/codetools/man/
%{_libdir}/R/library/codetools/Meta/
%{_libdir}/R/library/codetools/NAMESPACE
%{_libdir}/R/library/codetools/R/
%{_libdir}/R/library/codetools/R-ex/
# datasets
%dir %{_libdir}/R/library/datasets/
%{_libdir}/R/library/datasets/CONTENTS
%{_libdir}/R/library/datasets/data/
%{_libdir}/R/library/datasets/DESCRIPTION
%{_libdir}/R/library/datasets/help/
%{_libdir}/R/library/datasets/html/
%{_libdir}/R/library/datasets/INDEX
%{_libdir}/R/library/datasets/latex/
%{_libdir}/R/library/datasets/man/
%{_libdir}/R/library/datasets/Meta/
%{_libdir}/R/library/datasets/R/
%{_libdir}/R/library/datasets/R-ex/
# foreign
%dir %{_libdir}/R/library/foreign/
%{_libdir}/R/library/foreign/CONTENTS
%{_libdir}/R/library/foreign/COPYING
%{_libdir}/R/library/foreign/DESCRIPTION
%{_libdir}/R/library/foreign/files/
%{_libdir}/R/library/foreign/help/
%{_libdir}/R/library/foreign/html/
%{_libdir}/R/library/foreign/INDEX
%{_libdir}/R/library/foreign/latex/
%{_libdir}/R/library/foreign/libs/
%{_libdir}/R/library/foreign/LICENCE
%{_libdir}/R/library/foreign/man/
%{_libdir}/R/library/foreign/Meta/
%{_libdir}/R/library/foreign/NAMESPACE
%dir %{_libdir}/R/library/foreign/po/
%{_libdir}/R/library/foreign/po/en*/
%{_libdir}/R/library/foreign/po/fr/
%{_libdir}/R/library/foreign/R/
%{_libdir}/R/library/foreign/R-ex/
# graphics
%dir %{_libdir}/R/library/graphics/
%{_libdir}/R/library/graphics/CONTENTS
%{_libdir}/R/library/graphics/demo/
%{_libdir}/R/library/graphics/DESCRIPTION
%{_libdir}/R/library/graphics/help/
%{_libdir}/R/library/graphics/html/
%{_libdir}/R/library/graphics/INDEX
%{_libdir}/R/library/graphics/latex/
%{_libdir}/R/library/graphics/man/
%{_libdir}/R/library/graphics/Meta/
%{_libdir}/R/library/graphics/NAMESPACE
%dir %{_libdir}/R/library/graphics/po/
%{_libdir}/R/library/graphics/po/de/
%{_libdir}/R/library/graphics/po/en*/
%{_libdir}/R/library/graphics/po/fr/
%{_libdir}/R/library/graphics/po/it/
%{_libdir}/R/library/graphics/po/ja/
%{_libdir}/R/library/graphics/po/ko/
%{_libdir}/R/library/graphics/po/ru/
%{_libdir}/R/library/graphics/po/zh*/
%{_libdir}/R/library/graphics/R/
%{_libdir}/R/library/graphics/R-ex/
# grDevices
%dir %{_libdir}/R/library/grDevices
%{_libdir}/R/library/grDevices/afm/
%{_libdir}/R/library/grDevices/CONTENTS
%{_libdir}/R/library/grDevices/DESCRIPTION
%{_libdir}/R/library/grDevices/enc/
%{_libdir}/R/library/grDevices/help/
%{_libdir}/R/library/grDevices/html/
%{_libdir}/R/library/grDevices/INDEX
%{_libdir}/R/library/grDevices/latex/
%{_libdir}/R/library/grDevices/libs/
%{_libdir}/R/library/grDevices/man/
%{_libdir}/R/library/grDevices/Meta/
%{_libdir}/R/library/grDevices/NAMESPACE
%dir %{_libdir}/R/library/grDevices/po/
%{_libdir}/R/library/grDevices/po/de/
%{_libdir}/R/library/grDevices/po/en*/
%{_libdir}/R/library/grDevices/po/fr/
%{_libdir}/R/library/grDevices/po/it/
%{_libdir}/R/library/grDevices/po/ja/
%{_libdir}/R/library/grDevices/po/ko/
%{_libdir}/R/library/grDevices/po/ru/
%{_libdir}/R/library/grDevices/po/zh*/
%{_libdir}/R/library/grDevices/R/
%{_libdir}/R/library/grDevices/R-ex/
# grid
%dir %{_libdir}/R/library/grid/
%{_libdir}/R/library/grid/CONTENTS
%{_libdir}/R/library/grid/DESCRIPTION
%{_libdir}/R/library/grid/doc/
%{_libdir}/R/library/grid/help/
%{_libdir}/R/library/grid/html/
%{_libdir}/R/library/grid/INDEX
%{_libdir}/R/library/grid/latex/
%{_libdir}/R/library/grid/libs/
%{_libdir}/R/library/grid/man/
%{_libdir}/R/library/grid/Meta/
%{_libdir}/R/library/grid/NAMESPACE
%dir %{_libdir}/R/library/grid/po/
%{_libdir}/R/library/grid/po/de/
%{_libdir}/R/library/grid/po/en*/
%{_libdir}/R/library/grid/po/fr*/
%{_libdir}/R/library/grid/po/it/
%{_libdir}/R/library/grid/po/ja/
%{_libdir}/R/library/grid/po/ko/
%{_libdir}/R/library/grid/po/pt*/
%{_libdir}/R/library/grid/po/ru/
%{_libdir}/R/library/grid/po/zh*/
%{_libdir}/R/library/grid/R/
%{_libdir}/R/library/grid/R-ex/
# KernSmooth
%dir %{_libdir}/R/library/KernSmooth/
%{_libdir}/R/library/KernSmooth/CONTENTS
%{_libdir}/R/library/KernSmooth/DESCRIPTION
%{_libdir}/R/library/KernSmooth/help/
%{_libdir}/R/library/KernSmooth/html/
%{_libdir}/R/library/KernSmooth/INDEX
%{_libdir}/R/library/KernSmooth/latex/
%{_libdir}/R/library/KernSmooth/libs/
%{_libdir}/R/library/KernSmooth/LICENCE
%{_libdir}/R/library/KernSmooth/man/
%{_libdir}/R/library/KernSmooth/Meta/
%{_libdir}/R/library/KernSmooth/NAMESPACE
%{_libdir}/R/library/KernSmooth/R/
%{_libdir}/R/library/KernSmooth/R-ex/
# lattice
%dir %{_libdir}/R/library/lattice/
%{_libdir}/R/library/lattice/CONTENTS
%{_libdir}/R/library/lattice/COPYING
%{_libdir}/R/library/lattice/data/
%{_libdir}/R/library/lattice/demo/
%{_libdir}/R/library/lattice/DESCRIPTION
%{_libdir}/R/library/lattice/help/
%{_libdir}/R/library/lattice/html/
%{_libdir}/R/library/lattice/INDEX
%{_libdir}/R/library/lattice/latex/
%{_libdir}/R/library/lattice/libs/
%{_libdir}/R/library/lattice/man/
%{_libdir}/R/library/lattice/Meta/
%{_libdir}/R/library/lattice/NAMESPACE
%{_libdir}/R/library/lattice/NEWS
%{_libdir}/R/library/lattice/R/
%{_libdir}/R/library/lattice/R-ex/
# MASS
%dir %{_libdir}/R/library/MASS/
%{_libdir}/R/library/MASS/CITATION
%{_libdir}/R/library/MASS/CONTENTS
%{_libdir}/R/library/MASS/data/
%{_libdir}/R/library/MASS/DESCRIPTION
%{_libdir}/R/library/MASS/help/
%{_libdir}/R/library/MASS/html/
%{_libdir}/R/library/MASS/INDEX
%{_libdir}/R/library/MASS/latex/
%{_libdir}/R/library/MASS/libs/
%{_libdir}/R/library/MASS/LICENCE
%{_libdir}/R/library/MASS/man/
%{_libdir}/R/library/MASS/Meta/
%{_libdir}/R/library/MASS/NAMESPACE
%{_libdir}/R/library/MASS/NEWS
%dir %{_libdir}/R/library/MASS/po
%{_libdir}/R/library/MASS/po/en*/
%{_libdir}/R/library/MASS/po/fr/
%{_libdir}/R/library/MASS/R/
%{_libdir}/R/library/MASS/R-ex/
%{_libdir}/R/library/MASS/scripts/
# methods
%dir %{_libdir}/R/library/methods/
%{_libdir}/R/library/methods/CONTENTS
%{_libdir}/R/library/methods/DESCRIPTION
%{_libdir}/R/library/methods/help/
%{_libdir}/R/library/methods/html/
%{_libdir}/R/library/methods/INDEX
%{_libdir}/R/library/methods/latex/
%{_libdir}/R/library/methods/libs/
%{_libdir}/R/library/methods/man/
%{_libdir}/R/library/methods/Meta/
%{_libdir}/R/library/methods/NAMESPACE
%dir %{_libdir}/R/library/methods/po/
%{_libdir}/R/library/methods/po/de/
%{_libdir}/R/library/methods/po/en*/
%{_libdir}/R/library/methods/po/fr/
%{_libdir}/R/library/methods/po/ja/
%{_libdir}/R/library/methods/po/ko/
%{_libdir}/R/library/methods/po/pt*/
%{_libdir}/R/library/methods/po/ru/
%{_libdir}/R/library/methods/po/zh*/
%{_libdir}/R/library/methods/R/
%{_libdir}/R/library/methods/R-ex/
# mgcv
%dir %{_libdir}/R/library/mgcv/
%{_libdir}/R/library/mgcv/CITATION
%{_libdir}/R/library/mgcv/CONTENTS
%{_libdir}/R/library/mgcv/DESCRIPTION
%{_libdir}/R/library/mgcv/help/
%{_libdir}/R/library/mgcv/html/
%{_libdir}/R/library/mgcv/INDEX
%{_libdir}/R/library/mgcv/latex/
%{_libdir}/R/library/mgcv/libs/
%{_libdir}/R/library/mgcv/man/
%{_libdir}/R/library/mgcv/Meta/
%{_libdir}/R/library/mgcv/NAMESPACE
%{_libdir}/R/library/mgcv/R/
%{_libdir}/R/library/mgcv/R-ex/
# nlme
%dir %{_libdir}/R/library/nlme/
%{_libdir}/R/library/nlme/CITATION
%{_libdir}/R/library/nlme/CONTENTS
%{_libdir}/R/library/nlme/COPYING
%{_libdir}/R/library/nlme/data/
%{_libdir}/R/library/nlme/DESCRIPTION
%{_libdir}/R/library/nlme/help/
%{_libdir}/R/library/nlme/html/
%{_libdir}/R/library/nlme/INDEX
%{_libdir}/R/library/nlme/latex/
%{_libdir}/R/library/nlme/libs/
%{_libdir}/R/library/nlme/LICENCE
%{_libdir}/R/library/nlme/man/
%{_libdir}/R/library/nlme/Meta/
%{_libdir}/R/library/nlme/mlbook/
%{_libdir}/R/library/nlme/NAMESPACE
%dir %{_libdir}/R/library/nlme/po/
%{_libdir}/R/library/nlme/po/en*/
%{_libdir}/R/library/nlme/po/fr/
%{_libdir}/R/library/nlme/R/
%{_libdir}/R/library/nlme/R-ex/
%{_libdir}/R/library/nlme/scripts/
# nnet
%dir %{_libdir}/R/library/nnet/
%{_libdir}/R/library/nnet/CITATION
%{_libdir}/R/library/nnet/CONTENTS
%{_libdir}/R/library/nnet/DESCRIPTION
%{_libdir}/R/library/nnet/help/
%{_libdir}/R/library/nnet/html/
%{_libdir}/R/library/nnet/INDEX
%{_libdir}/R/library/nnet/latex/
%{_libdir}/R/library/nnet/libs/
%{_libdir}/R/library/nnet/LICENCE
%{_libdir}/R/library/nnet/man/
%{_libdir}/R/library/nnet/Meta/
%{_libdir}/R/library/nnet/NAMESPACE
%{_libdir}/R/library/nnet/NEWS
%dir %{_libdir}/R/library/nnet/po
%{_libdir}/R/library/nnet/po/en*/
%{_libdir}/R/library/nnet/po/fr/
%{_libdir}/R/library/nnet/R/
%{_libdir}/R/library/nnet/R-ex/
# rpart
%dir %{_libdir}/R/library/rpart/
%{_libdir}/R/library/rpart/CONTENTS
%{_libdir}/R/library/rpart/data/
%{_libdir}/R/library/rpart/DESCRIPTION
%{_libdir}/R/library/rpart/help/
%{_libdir}/R/library/rpart/html/
%{_libdir}/R/library/rpart/INDEX
%{_libdir}/R/library/rpart/latex/
%{_libdir}/R/library/rpart/libs/
%{_libdir}/R/library/rpart/LICENCE
%{_libdir}/R/library/rpart/man/
%{_libdir}/R/library/rpart/Meta/
%{_libdir}/R/library/rpart/NAMESPACE
%dir %{_libdir}/R/library/rpart/po
%{_libdir}/R/library/rpart/po/en*/
%{_libdir}/R/library/rpart/po/fr/
%{_libdir}/R/library/rpart/po/ru/
%{_libdir}/R/library/rpart/R/
%{_libdir}/R/library/rpart/R-ex/
# spatial
%dir %{_libdir}/R/library/spatial/
%{_libdir}/R/library/spatial/CITATION
%{_libdir}/R/library/spatial/CONTENTS
%{_libdir}/R/library/spatial/DESCRIPTION
%{_libdir}/R/library/spatial/help/
%{_libdir}/R/library/spatial/html/
%{_libdir}/R/library/spatial/INDEX
%{_libdir}/R/library/spatial/latex/
%{_libdir}/R/library/spatial/libs/
%{_libdir}/R/library/spatial/LICENCE
%{_libdir}/R/library/spatial/man/
%{_libdir}/R/library/spatial/Meta/
%{_libdir}/R/library/spatial/NAMESPACE
%{_libdir}/R/library/spatial/NEWS
%dir %{_libdir}/R/library/spatial/po
%{_libdir}/R/library/spatial/po/en*/
%{_libdir}/R/library/spatial/po/fr/
%{_libdir}/R/library/spatial/ppdata/
%{_libdir}/R/library/spatial/PP.files
%{_libdir}/R/library/spatial/R/
%{_libdir}/R/library/spatial/R-ex/
# splines
%dir %{_libdir}/R/library/splines/
%{_libdir}/R/library/splines/CONTENTS
%{_libdir}/R/library/splines/DESCRIPTION
%{_libdir}/R/library/splines/help/
%{_libdir}/R/library/splines/html/
%{_libdir}/R/library/splines/INDEX
%{_libdir}/R/library/splines/latex/
%{_libdir}/R/library/splines/libs/
%{_libdir}/R/library/splines/man/
%{_libdir}/R/library/splines/Meta/
%{_libdir}/R/library/splines/NAMESPACE
%dir %{_libdir}/R/library/splines/po
%{_libdir}/R/library/splines/po/de/
%{_libdir}/R/library/splines/po/en*/
%{_libdir}/R/library/splines/po/fr/
%{_libdir}/R/library/splines/po/ja/
%{_libdir}/R/library/splines/po/ko/
%{_libdir}/R/library/splines/po/pt*/
%{_libdir}/R/library/splines/po/ru/
%{_libdir}/R/library/splines/po/zh*/
%{_libdir}/R/library/splines/R/
%{_libdir}/R/library/splines/R-ex/
# stats
%dir %{_libdir}/R/library/stats/
%{_libdir}/R/library/stats/CONTENTS
%{_libdir}/R/library/stats/COPYRIGHTS.modreg
%{_libdir}/R/library/stats/demo/
%{_libdir}/R/library/stats/DESCRIPTION
%{_libdir}/R/library/stats/help/
%{_libdir}/R/library/stats/html/
%{_libdir}/R/library/stats/INDEX
%{_libdir}/R/library/stats/latex/
%{_libdir}/R/library/stats/libs/
%{_libdir}/R/library/stats/man/
%{_libdir}/R/library/stats/Meta/
%{_libdir}/R/library/stats/NAMESPACE
%dir %{_libdir}/R/library/stats/po
%{_libdir}/R/library/stats/po/de/
%{_libdir}/R/library/stats/po/en*/
%{_libdir}/R/library/stats/po/fr/
%{_libdir}/R/library/stats/po/it/
%{_libdir}/R/library/stats/po/ja/
%{_libdir}/R/library/stats/po/ko/
%{_libdir}/R/library/stats/po/pt*/
%{_libdir}/R/library/stats/po/ru/
%{_libdir}/R/library/stats/po/zh*/
%{_libdir}/R/library/stats/R/
%{_libdir}/R/library/stats/R-ex/
%{_libdir}/R/library/stats/SOURCES.ts
# stats4
%dir %{_libdir}/R/library/stats4/
%{_libdir}/R/library/stats4/CONTENTS
%{_libdir}/R/library/stats4/DESCRIPTION
%{_libdir}/R/library/stats4/help/
%{_libdir}/R/library/stats4/html/
%{_libdir}/R/library/stats4/INDEX
%{_libdir}/R/library/stats4/latex/
%{_libdir}/R/library/stats4/man/
%{_libdir}/R/library/stats4/Meta/
%{_libdir}/R/library/stats4/NAMESPACE
%dir %{_libdir}/R/library/stats4/po
%{_libdir}/R/library/stats4/po/de/
%{_libdir}/R/library/stats4/po/en*/
%{_libdir}/R/library/stats4/po/fr/
%{_libdir}/R/library/stats4/po/it/
%{_libdir}/R/library/stats4/po/ja/
%{_libdir}/R/library/stats4/po/ko/
%{_libdir}/R/library/stats4/po/pt*/
%{_libdir}/R/library/stats4/po/ru/
%{_libdir}/R/library/stats4/po/zh*/
%{_libdir}/R/library/stats4/R/
%{_libdir}/R/library/stats4/R-ex/
# survival
%dir %{_libdir}/R/library/survival/
%{_libdir}/R/library/survival/CONTENTS
%{_libdir}/R/library/survival/COPYING
%{_libdir}/R/library/survival/data/
%{_libdir}/R/library/survival/DESCRIPTION
%{_libdir}/R/library/survival/help/
%{_libdir}/R/library/survival/html/
%{_libdir}/R/library/survival/INDEX
%{_libdir}/R/library/survival/latex/
%{_libdir}/R/library/survival/libs/
%{_libdir}/R/library/survival/man/
%{_libdir}/R/library/survival/Meta/
%{_libdir}/R/library/survival/NAMESPACE
%{_libdir}/R/library/survival/R/
%{_libdir}/R/library/survival/R-ex/
%{_libdir}/R/library/survival/survival.ps*
# tcltk
%dir %{_libdir}/R/library/tcltk/
%{_libdir}/R/library/tcltk/CONTENTS
%{_libdir}/R/library/tcltk/demo/
%{_libdir}/R/library/tcltk/DESCRIPTION
%{_libdir}/R/library/tcltk/exec/
%{_libdir}/R/library/tcltk/help/
%{_libdir}/R/library/tcltk/html/
%{_libdir}/R/library/tcltk/INDEX
%{_libdir}/R/library/tcltk/latex/
%{_libdir}/R/library/tcltk/libs/
%{_libdir}/R/library/tcltk/man/
%{_libdir}/R/library/tcltk/Meta/
%{_libdir}/R/library/tcltk/NAMESPACE
%dir %{_libdir}/R/library/tcltk/po/
%{_libdir}/R/library/tcltk/po/de/
%{_libdir}/R/library/tcltk/po/en*/
%{_libdir}/R/library/tcltk/po/fr/
%{_libdir}/R/library/tcltk/po/it/
%{_libdir}/R/library/tcltk/po/ja/
%{_libdir}/R/library/tcltk/po/ko/
%{_libdir}/R/library/tcltk/po/pt*/
%{_libdir}/R/library/tcltk/po/ru/
%{_libdir}/R/library/tcltk/po/zh*/
%{_libdir}/R/library/tcltk/R/
%{_libdir}/R/library/tcltk/R-ex/
# tools
%dir %{_libdir}/R/library/tools/
%{_libdir}/R/library/tools/CONTENTS
%{_libdir}/R/library/tools/DESCRIPTION
%{_libdir}/R/library/tools/help/
%{_libdir}/R/library/tools/html/
%{_libdir}/R/library/tools/INDEX
%{_libdir}/R/library/tools/latex/
%{_libdir}/R/library/tools/libs/
%{_libdir}/R/library/tools/man/
%{_libdir}/R/library/tools/Meta/
%{_libdir}/R/library/tools/NAMESPACE
%dir %{_libdir}/R/library/tools/po
%{_libdir}/R/library/tools/po/de/
%{_libdir}/R/library/tools/po/en*/
%{_libdir}/R/library/tools/po/fr/
%{_libdir}/R/library/tools/po/it/
%{_libdir}/R/library/tools/po/ja/
%{_libdir}/R/library/tools/po/ko/
%{_libdir}/R/library/tools/po/pt*/
%{_libdir}/R/library/tools/po/ru/
%{_libdir}/R/library/tools/po/zh*/
%{_libdir}/R/library/tools/R/
%{_libdir}/R/library/tools/R-ex/
# utils
%dir %{_libdir}/R/library/utils/
%{_libdir}/R/library/utils/CONTENTS
%{_libdir}/R/library/utils/DESCRIPTION
%{_libdir}/R/library/utils/help/
%{_libdir}/R/library/utils/html/
%{_libdir}/R/library/utils/iconvlist
%{_libdir}/R/library/utils/INDEX
%{_libdir}/R/library/utils/latex/
%{_libdir}/R/library/utils/man/
%{_libdir}/R/library/utils/Meta/
%{_libdir}/R/library/utils/misc/
%{_libdir}/R/library/utils/NAMESPACE
%dir %{_libdir}/R/library/utils/po
%{_libdir}/R/library/utils/po/de/
%{_libdir}/R/library/utils/po/en*/
%{_libdir}/R/library/utils/po/fr/
%{_libdir}/R/library/utils/po/ja/
%{_libdir}/R/library/utils/po/ko/
%{_libdir}/R/library/utils/po/ru/
%{_libdir}/R/library/utils/po/zh*/
%{_libdir}/R/library/utils/R/
%{_libdir}/R/library/utils/R-ex/
%{_libdir}/R/library/utils/Sweave/
%{_libdir}/R/modules
%{_libdir}/R/COPYING
%{_libdir}/R/NEWS
%{_libdir}/R/SVN-REVISION
%{_infodir}/R-*.info*
%{_mandir}/man1/*
%{_docdir}/R-%{version}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/Rmath.h
%dir %attr (0755, root, bin) %{_includedir}/R
%{_includedir}/R/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/libR.pc
%{_libdir}/pkgconfig/libRmath.pc


%clean
rm -rf ${RPM_BUILD_ROOT};

#%post
# Create directory entries for info files
# (optional doc files, so we must check that they are installed)
#for doc in admin exts FAQ intro lang; do
#   file=%{_infodir}/R-${doc}.info.gz
#   if [ -e $file ]; then
#      /sbin/install-info ${file} %{_infodir}/dir 2>/dev/null || :
#   fi
#done
#/sbin/ldconfig
#R CMD javareconf \
#    JAVA_HOME=%{_jvmdir}/jre \
#    JAVA_CPPFLAGS='-I%{_jvmdir}/java/include\ -I%{_jvmdir}/java/include/linux' \
#    JAVA_LIBS='-L%{_jvmdir}/jre/lib/%{java_arch}/server \
#    -L%{_jvmdir}/jre/lib/%{java_arch}\ -L%{_jvmdir}/java/lib/%{java_arch} \
#    -L/usr/java/packages/lib/%{java_arch}\ -L/lib\ -L/usr/lib\ -ljvm' \
#    JAVA_LD_LIBRARY_PATH=%{_jvmdir}/jre/lib/%{java_arch}/server:%{_jvmdir}/jre/lib/%{java_arch}:%{_jvmdir}/java/lib/%{java_arch}:/usr/java/packages/lib/%{java_arch}:/lib:/usr/lib \
#    > /dev/null 2>&1 || exit 0

# Update package indices
#%__cat %{_libdir}/R/library/*/CONTENTS > %{_docdir}/R-%{version}/html/search/index.txt 2>/dev/null
# Don't use .. based paths, substitute RHOME
#sed -i "s!../../..!%{_libdir}/R!g" %{_docdir}/R-%{version}/html/search/index.txt

# This could fail if there are no noarch R libraries on the system.
#%__cat %{_datadir}/R/library/*/CONTENTS >> %{_docdir}/R-%{version}/html/search/index.txt 2>/dev/null || exit 0
# Don't use .. based paths, substitute /usr/share/R
#sed -i "s!../../..!/usr/share/R!g" %{_docdir}/R-%{version}/html/search/index.txt


#%preun core
#if [ $1 = 0 ]; then
#   # Delete directory entries for info files (if they were installed)
#   for doc in admin exts FAQ intro lang; do
#      file=%{_infodir}/R-${doc}.info.gz
#      if [ -e ${file} ]; then
#         /sbin/install-info --delete R-${doc} %{_infodir}/dir 2>/dev/null || :
#      fi
#   done
#fi
#
#%postun core -p /sbin/ldconfig

#%post java
#R CMD javareconf \
#    JAVA_HOME=%{_jvmdir}/jre \
#    JAVA_CPPFLAGS='-I%{_jvmdir}/java/include\ -I%{_jvmdir}/java/include/linux' \
#    JAVA_LIBS='-L%{_jvmdir}/jre/lib/%{java_arch}/server \
#    -L%{_jvmdir}/jre/lib/%{java_arch}\ -L%{_jvmdir}/java/lib/%{java_arch} \
#    -L/usr/java/packages/lib/%{java_arch}\ -L/lib\ -L/usr/lib\ -ljvm' \
#    JAVA_LD_LIBRARY_PATH=%{_jvmdir}/jre/lib/%{java_arch}/server:%{_jvmdir}/jre/lib/%{java_arch}:%{_jvmdir}/java/lib/%{java_arch}:/usr/java/packages/lib/%{java_arch}:/lib:/usr/lib \
#    > /dev/null 2>&1 || exit 0

#%post java-devel
#R CMD javareconf \
#    JAVA_HOME=%{_jvmdir}/jre \
#    JAVA_CPPFLAGS='-I%{_jvmdir}/java/include\ -I%{_jvmdir}/java/include/linux' \
#    JAVA_LIBS='-L%{_jvmdir}/jre/lib/%{java_arch}/server \
#    -L%{_jvmdir}/jre/lib/%{java_arch}\ -L%{_jvmdir}/java/lib/%{java_arch} \
#    -L/usr/java/packages/lib/%{java_arch}\ -L/lib\ -L/usr/lib\ -ljvm' \
#    JAVA_LD_LIBRARY_PATH=%{_jvmdir}/jre/lib/%{java_arch}/server:%{_jvmdir}/jre/lib/%{java_arch}:%{_jvmdir}/java/lib/%{java_arch}:/usr/java/packages/lib/%{java_arch}:/lib:/usr/lib \
#    > /dev/null 2>&1 || exit 0

%changelog
* Thu Apr 16 2009 - Gilles Dauphin
- inital config (from fedora)
