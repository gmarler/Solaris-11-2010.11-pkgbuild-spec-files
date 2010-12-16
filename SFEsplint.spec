#
# spec file for package SFEsplint.spec
#
# includes module(s): splint
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name splint

Name:		SFEsplint
Version:	3.1.2
Summary:	An implementation of the lint program
Group:		Development/Tools
License:	GPLv2+
URL:		http://www.splint.org/
Source:		http://www.splint.org/downloads/%{src_name}-%{version}.src.tgz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWgawk

%description
Splint is a tool for statically checking C programs for coding errors and
security vulnerabilities. With minimal effort, Splint can be used as a
better lint. If additional effort is invested adding annotations to programs,
Splint can perform even stronger checks than can be done by any standard lint.


%prep
%setup -q -n %{src_name}-%{version}
chmod 644 doc/manual.pdf
cp -p src/.splintrc splintrc.demo

%build
export CC=gcc
export CXX=g++
export CFLAGS="%{optflags} -D__pid_t=pid_t"
export LDFLAGS="%{_ldflags}"
./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --mandir=%{_mandir}

make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}


%files
%defattr(-, root, bin)
%doc README doc/manual.pdf splintrc.demo
%{_bindir}/*
%{_mandir}/man1/*.1*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_datadir}/%{src_name}/


%changelog
* Thu Dec 16 2010 - Milan Jurik
- initial spec based on Fedora
