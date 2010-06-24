#
# spec file for package SFEmanifold
#
#

%include Solaris.inc

%define  src_name Manifold
%define  python_version  2.6


Name:                    SFEmanifold
Summary:                 manifold - create Solaris SMF manifest by asking simple questions
Version:                 0.2.0
License:                 MIT
Group:                   Development/Tools
URL:                     http://code.google.com/p/manifold/
Source:                  http://pypi.python.org/packages/source/M/Manifold/Manifold-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-python26-libs
Requires: SUNWPython26
Requires: SFEpython26-genshi.spec
BuildRequires: SUNWgnome-python26-libs-devel
BuildRequires: SUNWPython26-devel
BuildRequires: SFEpython26-genshi.spec

%description
Manifold helps you quickly and easily create Solaris SMF manifest XML files for your services by answering a few questions about how it needs to be configured.

Manifold requires Python and the Genshi template package.

Example: (taken from the  URL http://code.google.com/p/manifold/)
Use manifold to create a manifest (XML) file for memcached:

$ manifold memcached.xml

The service category (example: 'site' or '/application/database') [site] 

The name of the service, which follows the service category
   (example: 'myapp') [] memcached

The version of the service manifest (example: '1') [1] 

The human readable name of the service
   (example: 'My service.') [] Memcached

Can this service run multiple instances (yes/no) [no] ? yes

Enter value for instance_name (example: default) [default] 

Full path to a config file; leave blank if no config file
  required (example: '/etc/myservice.conf') [] 

The full command to start the service; may contain
  '%{config_file}' to substitute the configuration file
   (example: '/usr/bin/myservice %{config_file}') [] /opt/memcached/bin/memcached -d

The full command to stop the service; may specify ':kill' to let
  SMF kill the service processes automatically
   (example: '/usr/bin/myservice_ctl stop' or ':kill' to let SMF kill
  the service processes automatically) [:kill] 

Choose a process management model:
  'wait'      : long-running process that runs in the foreground (default)
  'contract'  : long-running process that daemonizes or forks itself
                (i.e. start command returns immediately)
  'transient' : short-lived process, performs an action and ends quickly
   [wait] contract

Does this service depend on the network being ready (yes/no) [yes] ? 

Should the service be enabled by default (yes/no) [no] ? 

The user to change to when executing the
  start/stop/refresh methods (example: 'webservd') [] webservd

The group to change to when executing the
  start/stop/refresh methods (example: 'webservd') [] webservd

Manifest written to memcached.xml
You can validate the XML file with ßvccfg validate memcached.xml"
And create the SMF service with ßvccfg import memcached.xml"

%prep
%setup -q -n %src_name-%version

%build
python%{python_version} ./setup.py build 

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages
#python%{python_version} setup.py clean install --prefix=$RPM_BUILD_ROOT/usr

PYTHONPATH=$RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages
python%{python_version} ./setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix} \
        --no-compile

## Fix some annoying hardcoded paths
#b=`echo $RPM_BUILD_ROOT | sed 's/\\//\\\\\\//g'` 
#perl -pi -e 's/'$b'//g' $RPM_BUILD_ROOT/usr/lib/python2.6/site-packages/manifold/paths.py


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_bindir}
%{_bindir}/manifold
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/*

%changelog
* Thu Jun 24 2010 - Thomas Wagner
- initial spec
