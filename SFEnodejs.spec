#
# spec file for package SFEnodejs
#
# includes module(s): nodejs
#
%include Solaris.inc

%define	src_version 0.2.0

Summary:	Asynchronous JavaScript Engine  
Name:		SFEnodejs  
Version:	0.2
License:	BSD  
Group:		Libraries  
URL:		http://nodejs.org/  
Source:		http://nodejs.org/dist/node-v%{src_version}.tar.gz  
Patch1:		nodejs-01-gcc.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

BuildRequires:	SFElibev-devel  
Requires:	SFElibev
BuildRequires:	SFEc-ares-devel
Requires:	SFEc-ares
Requires:	SUNWgccruntime

%description  
Node's goal is to provide an easy way to build scalable network  
programs. In the above example, the two second delay does not prevent  
the server from handling new requests. Node tells the operating system  
(through epoll, kqueue, /dev/poll, or select) that it should be  
notified when the 2 seconds are up or if a new connection is made --  
then it goes to sleep. If someone new connects, then it executes the  
callback, if the timeout expires, it executes the inner callback. Each  
connection is only a small heap allocation.  

%package devel  
Summary:	Development headers for nodejs  
Group:		Development/Libraries  

%description devel  
Development headers for nodejs.  

%prep  
%setup -q -n node-v%{src_version}  
%patch1 -p1

%build  
export CC=gcc
export CXX=g++

./configure --prefix=%{_prefix} \
	--shared-cares \
	--shared-libev \
	--shared-libev-includes=/usr/include/libev

make

%install  
rm -rf $RPM_BUILD_ROOT  
make install DESTDIR=$RPM_BUILD_ROOT

%clean  
rm -rf $RPM_BUILD_ROOT  
  
%files  
%defattr(-, root, bin)
%doc AUTHORS ChangeLog LICENSE
%{_bindir}/node
%{_bindir}/node-repl
%{_libdir}/node
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_mandir}/man1/node.1

%files devel  
%defattr(-, root, bin)  
%{_bindir}/node-waf
%{_includedir}/node  
%{_libdir}/node/wafadmin/  

%changelog  
* Thu Sep 07 2010 - Milan Jurik
- initial spec
