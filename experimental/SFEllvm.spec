#
# spec file for package SFEllvm
#
# includes module(s): llvm
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name llvm

Name:		SFEllvm
Version:	2.7
Summary:	The Low Level Virtual Machine (An Optimizing Compiler Infrastructure)
License:	University of Illinois/NCSA Open Source License
Vendor:x	None (open source)
Group:		Development/Compilers
URL:		http://llvm..org/
Source:		http://llvm.org/releases/%{version}/%{src_name}-%{version}.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
LLVM is a compiler infrastructure designed for compile-time, link-time, runtime,
and idle-time optimization of programs from arbitrary programming languages.
LLVM is written in C++ and has been developed since 2000 at the University of
Illinois and Apple. It currently supports compilation of C and C++ programs, 
using front-ends derived from GCC 4.0.1. A new front-end for the C family of
languages is in development. The compiler infrastructure
includes mirror sets of programming tools as well as libraries with equivalent
functionality.

%prep
%setup -q -n %{src_name}-%{version}

%build
export CC=gcc
export CXX=g++
./configure \
--prefix=%{_prefix} \
--bindir=%{_bindir} \
--datadir=%{_datadir} \
--includedir=%{_includedir} \
--libdir=%{_libdir} \
--enable-optimized \
--enable-assertions 
make tools-only

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc CREDITS.TXT LICENSE.TXT README.txt docs/*.{html,css,gif,jpg} docs/CommandGuide
%{_bindir}/*
%{_libdir}/*.o
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/llvm

%changelog
* Fri May 14 2010 - Milan Jurik
- Initial SFE import
* Fri Aug 04 2006 Reid Spencer
- Updates for release 1.8
* Fri Apr 07 2006 Reid Spencer
- Make the build be optimized+assertions
* Fri May 13 2005 Reid Spencer
- Minor adjustments for the 1.5 release
* Mon Feb 09 2003 Brian R. Gaeke
- Initial working version of RPM spec file.

