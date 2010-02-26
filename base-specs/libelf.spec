#
# Copyright (c) 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

Name:                libelf
Summary:             A Library to Manipulate ELf Files
Version:             0.8.10
Source:              http://prdownloads.sourceforge.net/mcj/libelf-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
export CFLAGS="%optflags"
export CXXFLAGS="%{gcc_cxx_optflags}"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"
export PERL_PATH=/usr/perl5/bin/perl
#export LDFLAGS="%{_ldflags} -L%{_libdir} -R%{_libdir} $LDFLAGS"

./configure --prefix=$RPM_BUILD_ROOT%{_prefix}	\
	    --bindir=%{_bindir}	\
	    --libdir=$RPM_BUILD_ROOT%{_libdir}	\
	    --mandir=%{_mandir}	\
            --enable-shared 

gmake -j$CPUS

%install
make install

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Feb 25 2010 - jchoi42@pha.jhu.edu
- Initial spec
