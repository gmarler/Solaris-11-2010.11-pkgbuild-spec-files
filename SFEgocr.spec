#
# spec file for package SFEgocr
#
#
%include Solaris.inc

Name:		SFEgocr
Summary:	GOCR Optical Character Recognition package.
Version:	0.49
URL:		http://jocr.sourceforge.net/
Source:		http://www-e.uni-magdeburg.de/jschulen/ocr/gocr-%{version}.tar.gz
Group:		Graphics
License:	GPL
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SUNWcsu

%prep
%setup -q -n gocr-%{version}

%description
GOCR is an optical character recognition program. 
It reads images in many formats  and outputs a text file.
Possible image formats are pnm, pbm, pgm, ppm, some pcx and
tga image files. Other formats like pnm.gz, pnm.bz2, png, jpg, tiff, gif,
bmp will be automatically converted using the netpbm-progs, gzip and bzip2
via unix pipe.
A simple graphical frontend written in tcl/tk and some
sample files (you need transfig for the sample files) are included.
Gocr is also able to recognize and translate barcodes.
You do not have to train the program or store large font bases.
Simply call gocr from the command line and get your results.



%build
CFLAGS="%{optflags}" \
LDFLAGS="%{_ldflags}" \
./configure --prefix=%{_prefix} \
	--bindir=%{_bindir}	\
	--mandir=%{_mandir}

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr(0755, root, sys) %{_datadir}
%{_mandir}

%changelog
* Tue Nov 30 2010 - Milan Jurik
- bump to 0.49
* Sat Feb 2 2008 - pradhap (at) gmail.com
- Initial gocr spec file
