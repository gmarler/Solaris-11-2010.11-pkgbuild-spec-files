#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Spec file for automated packaging of Masayuki Murayama's network drivers
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%define vfe_version 2.6.4
%define rf_version 2.6.2
%define ni_version 0.8.11
%define alta_version 2.6.3
%define tu_version 2.6.0b
%define bfe_version 2.6.1
%define tne_version 2.4.0a
%define ife_version 2.6.1
%define epfe_version 2.6.1
%define mtd_version 2.4.0
%define ae_version 2.6.1
%define tcfe_version 2.4.0
%define gani_version 2.6.3
%define vel_version 2.6.4
%define nfo_version 2.6.3
%define icpt_version 2.4.0
%define sige_version 2.6.2
%define em_version 2.4.0
%define myk_version 2.6.6
%define atge_version 2.6.3
%define jmge_version 2.6.1
%define urf_version 0.8.2
%define axf_version 0.8.2
%define upf_version 0.8.2

%define src_url http://homepage2.nifty.com/mrym3/taiyodo

Name:                SFEnicdrv
Summary:             Base package for Masayuki Murayama's Solaris NIC drivers
Version:             1.0
Source0:             %{src_url}/vfe-%{vfe_version}.tar.gz
Source1:             %{src_url}/rf-%{rf_version}.tar.gz

# ni may not work on sparc
Source2:             %{src_url}/ni-%{ni_version}.tar.gz
Source3:             %{src_url}/alta-%{alta_version}.tar.gz

# Replaces dnet which is still missing on sparc
# dnet had a number of other updates since this was written, though
Source4:             %{src_url}/tu-%{tu_version}.tar.gz
Source5:             %{src_url}/bfe-%{bfe_version}.tar.gz
Source6:             %{src_url}/tne-%{tne_version}.tar.gz
# Replaces spwr
Source7:             %{src_url}/epfe-%{epfe_version}.tar.gz
Source8:             %{src_url}/mtd-%{mtd_version}.tar.gz
# Replaces pcn
Source9:             %{src_url}/ae-%{ae_version}.tar.gz
Source10:            %{src_url}/gani-%{gani_version}.tar.gz
Source11:            %{src_url}/vel-%{vel_version}.tar.gz
Source12:            %{src_url}/icpt-%{icpt_version}.tar.gz
Source13:            %{src_url}/sige-%{sige_version}.tar.gz
Source14:            %{src_url}/myk-%{myk_version}.tar.gz
Source15:            %{src_url}/urf-%{urf_version}.tar.gz
Source16:            %{src_url}/axf-%{axf_version}.tar.gz
Source17:            %{src_url}/upf-%{upf_version}.tar.gz
# Replaces iprb
Source18:            %{src_url}/ife-%{ife_version}.tar.gz
# Replaces elxl
Source19:            %{src_url}/tcfe-%{tcfe_version}.tar.gz
# Replaces e1000g
Source20:            %{src_url}/em-%{em_version}.tar.gz
# Replaces nge and supports newer nForce chipsets
Source21:            %{src_url}/nfo-%{nfo_version}.tar.gz
Source22:            %{src_url}/atge-%{atge_version}.tar.gz
Source23:            %{src_url}/jmge-%{jmge_version}.tar.gz

# Template script used to generate post-install scripts for each driver.
Source100:           drvtestadd

# Script used to generate postinstall scripts.
Source101:           build_add_drv

# Common script called by each driver to remove the device association.
Source102:           drvrm

# Template etc/system file needed by the Makefiles when installing to
# alternate DESTDIR.
Source103:           etc_system

# Headers for building GLDv3 drivers outside of ON tree.
#Source104:           http://trisk.acm.jhu.edu/src/gldv3-headers-0.20090219.tar.bz2
Source104:           http://deadgerbil.com/~trisk/src/gldv3-headers-0.20090522.tar.bz2
Patch1:              nicdrv-01-em.diff
Patch2:              nicdrv-02-rf.diff
Patch3:              nicdrv-03-tu.diff
Patch4:              nicdrv-04-gani.diff
Patch5:              nicdrv-05-myk.diff
Patch6:              nicdrv-06-ife.diff
Patch7:              nicdrv-07-tcfe.diff
Patch8:              nicdrv-08-gldv3.diff
Patch9:              nicdrv-09-nfo.diff
Patch10:             nicdrv-10-atge.diff
Patch11:             nicdrv-11-jmge.diff
Patch12:             nicdrv-12-ae.diff
Patch13:             nicdrv-13-sige.diff

URL:                 http://homepage2.nifty.com/mrym3/taiyodo/eng/
SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package vfe
Summary:       NIC driver for VIA Rhine family fast ethernet chipset 
Version:       %{vfe_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package rf
Summary:       NIC driver for Realtek RTL 8129 / 8139 / 810x family fast ethernet chipset
Version:       %{rf_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package ni
Summary:       NIC (ni/pcni) driver for NE2000 compatible PCI/PCMCIA/PnP ISA ethernet cards
Version:       %{ni_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package alta
Summary:       NIC driver for Sundance Technology ST201, IC Plus IP100A fast ethernet chipset
Version:       %{alta_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package tu
Summary:       NIC driver for 2114x fast ethernet chipset
Version:       %{tu_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package bfe
Summary:       NIC driver for bcm4401 fast ethernet chipset
Version:       %{bfe_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package tne
Summary:       NIC driver for TI ThunderLAN fast ethernet chipset
Version:       %{tne_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package epfe
Summary:       NIC driver for SMSC epic fast ethernet chipset series
Version:       %{epfe_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package mtd
Summary:       NIC driver for Myson mtd803 fast ethernet chipset
Version:       %{mtd_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package ae
Summary:       NIC driver for AMD am79c97x PCNET ethernet chipset series
Version:       %{ae_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package gani
Summary:       NIC driver for Realtek rtl8169 rtl8110 rtl8168 rtl8101 PCI/PCI-Express GbE chipset
Version:       %{gani_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package vel
Summary:       NIC driver for VIA VT6122 GbE chipset
Version:       %{vel_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package nfo
Summary:       NIC driver for NVIDIA nForce chipset built-in ethernet controller
Version:       %{nfo_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package icpt
Summary:       NIC driver for IC Plus ip1000a GbE chipset
Version:       %{icpt_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package sige
Summary:       NIC driver for SiS integrated fast/gigabit ethernet controller sis190/sis191
Version:       %{sige_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package myk
Summary:       NIC driver for marvell PCI-E GbE controller yukon2
Version:       %{myk_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package urf
Summary:       NIC driver for Realtek rtl8150 usb1.x to fast ethernet controller
Version:       %{urf_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package axf
Summary:       NIC driver for ASIX AX88172 usb2.0 to fast ethernet controller
Version:       %{axf_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package upf
Summary:       NIC driver for ADMtek Pegasus family usb1.x to fast ethernet controller
Version:       %{upf_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package ife
Summary:       NIC driver for intel 8255x fast ethernet chipset
Version:       %{ife_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package tcfe
Summary:       NIC driver for 3Com cardbus/PCI fast ethernet cards
Version:       %{tcfe_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package em
Summary:       NIC driver for intel gigabit ethernet controller 8254x
Version:       %{em_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package atge
Summary:       NIC driver for Attansic L1/L2 and Atheros AR81 ethernet controller
Version:       %{atge_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%package jmge
Summary:       NIC driver for JMicron JMC250/260 PCI-E ethernet controller
Version:       %{jmge_version}
SUNW_BaseDir:  /
%include default-depend.inc
Requires: %{name}
Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr

%prep
%setup -c -n %{name}-%{version}
%setup -T -D -a 1
%setup -T -D -a 2
%setup -T -D -a 3
%setup -T -D -a 4
%setup -T -D -a 5
%setup -T -D -a 6
%setup -T -D -a 7
%setup -T -D -a 8
%setup -T -D -a 9
%setup -T -D -a 10
%setup -T -D -a 11
%setup -T -D -a 12
%setup -T -D -a 13
%setup -T -D -a 14
%setup -T -D -a 15
%setup -T -D -a 16
%setup -T -D -a 17
%setup -T -D -a 18
%setup -T -D -a 19
%setup -T -D -a 20
%setup -T -D -a 21
%setup -T -D -a 22
%setup -T -D -a 23
%setup -T -D -a 104
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0
%patch8 -p0
%patch9 -p0
%patch10 -p0
%patch11 -p0
%patch12 -p0
%patch13 -p0

for src in %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} \
	%{SOURCE6} %{SOURCE7} %{SOURCE8} %{SOURCE9} %{SOURCE10} %{SOURCE11} \
	%{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} %{SOURCE16} %{SOURCE17} \
	%{SOURCE18} %{SOURCE19} %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23}
do
	drvdir=`basename ${src} | sed 's/\.tar\.gz//'`
	# use newest GEM 2.6 code if possible, else 2.4 from em
	case "$drvdir" in
		em-*|bfe-*) # GEM code donors
		# WARNING: update patch8 if changing donors!
		;;
		# these drivers have a GEM 2.4 interface, consider updating
		*-2.4.*)
		rm -f $drvdir/gem.c $drvdir/gem.h
		cp em-*/gem.c em-*/gem.h $drvdir
		;;
		*-2.6.*)
		rm -f $drvdir/gem.c $drvdir/gem.h
		cp bfe-*/gem.c bfe-*/gem.h $drvdir
		;;
	esac
done

%build

if [ "x`basename $CC`" != xgcc ]
then
	ccext="suncc"
else
	ccext="gcc"
fi

if [ "x`uname -r`" = "x5.10" ]
then
	gld="2"
else
	gld="3"
fi

#
# Build all the drivers
#
cp %{SOURCE101} .
for src in %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} \
	%{SOURCE6} %{SOURCE7} %{SOURCE8} %{SOURCE9} %{SOURCE10} %{SOURCE11} \
	%{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} %{SOURCE16} %{SOURCE17} \
	%{SOURCE18} %{SOURCE19} %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23}
do
	drvdir=`basename ${src} | sed 's/\.tar\.gz//'`
	cd $drvdir
	rm Makefile
	if [ -f Makefile.config_gld3 -a "$gld" = "3" ]; then
		rm -f Makefile.config
		# some configs don't use ONUTSDIR
		cat Makefile.config_gld3 | sed "s,/home/mrym/opensolaris/usr/src/uts,${PWD}/../gldv3-headers,g" > Makefile.config
		# some configs don't have all the new magic
		cat >> Makefile.config <<EOF
CFGFLAGS += \
	    -Unotdef -UNEVER -UGEM_GCC_RUNTIME \
	    -UGEM_COMPAT -USANITY -UGEM_CONFIG_FMA -UMODULE \
	    -UGEM_CONFIG_RX_DIRECT -DGEM_CONFIG_TX_DIRECT \
	    -DCONFIG_PM
EOF
	fi
		

	# Patch Makefile to remove hard dependency on a file in /etc
	# to allow specifying an alternate DESTDIR later.
	#
	cat Makefile.%{_arch64}_${ccext} | sed 's/\/etc\/system/system/g' > Makefile
	make clean
	make \
	 ONUTSDIR="${PWD}/../gldv3-headers" \
	 OFLAGS_GCC="-O2 -march=pentium -D__INLINE__=inline" \
	 OFLAGS_SUNCC="-xO4 -xprefetch=auto -D__INLINE__=inline -Wu,-xmodel=kernel" \
	 AFLAGS_SUNCC_AMD64="-m64 -Di86pc -xchip=opteron -xmodel=kernel"

	#
	# Patch all the adddrv.sh scripts. We change all the calls to add_drv
	# to our own script to capture all the device aliases and generate
	# postinstall scripts that check for pre-existing driver associations
	# before calling add_drv.
	#
	cp ../build_add_drv .
	chmod +x ./build_add_drv
	drv=`echo $drvdir | cut -f1 -d"-"`
	if [ "$drv" = "em" ]
	then
		cat adddrv.sh | sed 's/\/usr\/sbin\/add_drv/\.\/build_add_drv/' \
			| sed 's/\/usr\/sbin\/update_drv/\.\/build_add_drv/' \
			| sed 's/exit 1//' > adddrv_.sh
	elif [ "$drv" = "ni" ]
	then
		cat addni.sh | sed 's/\/usr\/sbin\/add_drv/\.\/build_add_drv/' \
			| sed 's/\/usr\/sbin\/update_drv/\.\/build_add_drv/' \
			> adddrv_1.sh
		cat addpcni.sh | sed 's/\/usr\/sbin\/add_drv/\.\/build_add_drv/' \
			| sed 's/\/usr\/sbin\/update_drv/\.\/build_add_drv/' \
			> adddrv_2.sh
	else
		cat adddrv.sh | sed 's/\/usr\/sbin\/add_drv/\.\/build_add_drv/' \
			| sed 's/\/usr\/sbin\/update_drv/\.\/build_add_drv/' \
			> adddrv_.sh
	fi
	[ -f ./adddrv_.sh ] && chmod +x ./adddrv_.sh
	[ -f ./adddrv_1.sh ] && chmod +x ./adddrv_1.sh
	[ -f ./adddrv_2.sh ] && chmod +x ./adddrv_2.sh
	cp %{SOURCE100} ../${drv}.postinst

	[ -f ./adddrv_.sh ] && ./adddrv_.sh >> ../${drv}.postinst
	[ -f ./adddrv_1.sh ] && ./adddrv_1.sh >> ../${drv}.postinst
	[ -f ./adddrv_2.sh ] && ./adddrv_2.sh >> ../${drv}.postinst
	cp /tmp/__aliases__ ../${drv}.aliases

	cd ..
done

%install

rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/doc
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/doc/nicdrv
mkdir -p ${RPM_BUILD_ROOT}/kernel/drv
mkdir -p ${RPM_BUILD_ROOT}/kernel/drv/%{_arch64}
mkdir -p ${RPM_BUILD_ROOT}/%{_localstatedir}/nicdrv/scripts
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}
cp %{SOURCE102} ${RPM_BUILD_ROOT}/%{_localstatedir}/nicdrv/scripts

for src in %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} \
	%{SOURCE6} %{SOURCE7} %{SOURCE8} %{SOURCE9} %{SOURCE10} %{SOURCE11} \
	%{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} %{SOURCE16} %{SOURCE17} \
	%{SOURCE18} %{SOURCE19} %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23}
do
	drvdir=`basename ${src} | sed 's/\.tar\.gz//'`
	cd $drvdir
	drv=`echo $drvdir | cut -f1 -d"-"`
	mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/doc/nicdrv/${drv}
	cp README* ${RPM_BUILD_ROOT}%{_datadir}/doc/nicdrv/${drv}
	for al in `cat ../${drv}.aliases`
	do
		echo "${drv} ${al}" >> ${RPM_BUILD_ROOT}%{_datadir}/doc/nicdrv/aliases
	done

	# Patch Makefile.common install rules to allow specifying a DESTDIR
	#
	if [ ! -f Makefile.common.orig ]
	then
		mv Makefile.common Makefile.common.orig
	fi
	cat Makefile.common.orig | \
		sed 's/\${INSTALLDIR32}/\${DESTDIR}\/\${INSTALLDIR32}/' | \
		sed 's/\${INSTALLDIR64}/\${DESTDIR}\/\${INSTALLDIR64}/' | \
		sed 's/^\/etc\/system/system/g' | \
		sed 's/\/etc/\${DESTDIR}\/etc/g' \
		> Makefile.common

	# First install to a subdirectory in the RPM_BUILD_ROOT to allow
	# building a per-driver file list, since we generate one package
	# for each driver.
	#
	mkdir -p ${RPM_BUILD_ROOT}/${drv}/kernel/drv
	mkdir -p ${RPM_BUILD_ROOT}/${drv}/kernel/drv/%{_arch64}
	mkdir -p ${RPM_BUILD_ROOT}/${drv}%{_sysconfdir}

	cp %{SOURCE103} ${RPM_BUILD_ROOT}/${drv}%{_sysconfdir}/system
	make install DESTDIR="${RPM_BUILD_ROOT}/${drv}"
	rm -f ${RPM_BUILD_ROOT}/${drv}%{_sysconfdir}/system

	# Build the driver's file list
	#
	(cd ${RPM_BUILD_ROOT}/${drv}; find * -type d) | \
		sed 's/^/%dir %attr \(0755, root, sys\) \//' > ../${drv}.files
	(cd ${RPM_BUILD_ROOT}/${drv}; find * -type f) | egrep -v "\.conf$" | \
		sed 's/^/%attr \(0755, root, sys\) \//' >> ../${drv}.files
	(cd ${RPM_BUILD_ROOT}/${drv}; find * -type f) | egrep "\.conf$" | \
		sed 's/^/%attr \(0644, root, sys\) \//' >> ../${drv}.files

	# Clean up the sub-directory
	#
	rm -rf ${RPM_BUILD_ROOT}/${drv}
	cp %{SOURCE103} ${RPM_BUILD_ROOT}/%{_sysconfdir}/system

	# Now install into RPM_BUILD_ROOT
	#
	make install DESTDIR="${RPM_BUILD_ROOT}"
	rm -f ${RPM_BUILD_ROOT}/%{_sysconfdir}/system
	cp ../${drv}.postinst ${RPM_BUILD_ROOT}/%{_localstatedir}/nicdrv/scripts
	cd ..
done

%clean
rm -rf $RPM_BUILD_ROOT

# We are calling external postinstall scripts since there is no way in an
# RPM spec file to include a generated script in the %post directives.
#
%post vfe
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/vfe.postinst

%postun vfe
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} vfe

%post rf
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/rf.postinst

%postun rf
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} rf

%post ni
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/ni.postinst

%postun ni
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} ni

%post alta
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/alta.postinst

%postun alta
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} alta

%post tu
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/tu.postinst

%postun tu
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} tu

%post bfe
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/bfe.postinst

%postun bfe
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} bfe

%post tne
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/tne.postinst

%postun tne
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} tne

%post epfe
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/epfe.postinst

%postun epfe
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} epfe

%post mtd
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/mtd.postinst

%postun mtd
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} mtd

%post ae
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/ae.postinst

%postun ae
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} ae

%post gani
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/gani.postinst

%postun gani
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} gani

%post vel
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/vel.postinst

%postun vel
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} vel

%post nfo
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/nfo.postinst

%postun nfo
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} nfo

%post icpt
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/icpt.postinst

%postun icpt
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} icpt

%post sige
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/sige.postinst

%postun sige
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} sige

%post myk
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/myk.postinst

%postun myk
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} myk

%post urf
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/urf.postinst

%postun urf
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} urf

%post axf
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/axf.postinst

%postun axf
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} axf

%post upf
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/upf.postinst

%postun upf
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} upf

%post ife
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/ife.postinst

%postun ife
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} ife

%post tcfe
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/tcfe.postinst

%postun tcfe
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} tcfe

%post em
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/em.postinst

%postun em
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} em

%post atge
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/atge.postinst

%postun atge
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} atge

%post jmge
. ${BASEDIR:=}%{_localstatedir}/nicdrv/scripts/jmge.postinst

%postun jmge
BASEDIR=${BASEDIR:=/}
${BASEDIR}%{_localstatedir}/nicdrv/scripts/drvrm ${BASEDIR} jmge


%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0700, root, bin) %{_localstatedir}/nicdrv/scripts/drvrm

%files vfe -f vfe.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/vfe.postinst

%files rf -f rf.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/rf.postinst

%files ni -f ni.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/ni.postinst

%files alta -f alta.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/alta.postinst

%files tu -f tu.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/tu.postinst

%files bfe -f bfe.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/bfe.postinst

%files tne -f tne.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/tne.postinst

%files epfe -f epfe.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/epfe.postinst

%files mtd -f mtd.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/mtd.postinst

%files ae -f ae.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/ae.postinst

%files gani -f gani.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/gani.postinst

%files vel -f vel.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/vel.postinst

%files nfo -f nfo.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/nfo.postinst

%files icpt -f icpt.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/icpt.postinst

%files sige -f sige.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/sige.postinst

%files myk -f myk.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/myk.postinst

%files urf -f urf.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/urf.postinst

%files axf -f axf.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/axf.postinst

%files upf -f upf.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/upf.postinst

%files ife -f ife.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/ife.postinst

%files tcfe -f tcfe.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/tcfe.postinst

%files em -f em.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/em.postinst

%files atge -f atge.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/atge.postinst


%files jmge -f jmge.files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv
%dir %attr (0755, root, bin) %{_localstatedir}/nicdrv/scripts
%attr (0644, root, bin) %{_localstatedir}/nicdrv/scripts/jmge.postinst

%changelog
* Sun May 31 2009 - Albert Lee <trisk@forkgnu.org>
- Update GLDv3 headers to 20090522 version (snv_116)
* Thu Feb 19 2009 - Albert Lee
- Update to vfe-2.6.4, rf-2.6.2, alta-2.6.3, bfe-2.6.1, ife-2.6.1, epfe-2.6.1,
  ae-2.6.1, gani-2.6.3, vel-2.6.4, nfo-2.6.3, myk-2.6.6, atge-2.6.3
- Add jmge driver
- Update GLD headers for Crossbow - requires b106 or later due to 6784639
- Fix GLDv3/Crossbow support for several drivers
- Update patch8 to fix GEM 2.4 and 2.6 bugs
* Sat Dec 20 2008 - Thomas Wagner
- corrected package name for atge (was Intel -> now Attansic L1/L2 and Atheros AR81)
* Sun Nov 30 2008 - Thomas Wagner
- Add atge driver
* Sat Jun 07 2008 - trisk@acm.jhu.edu
- Use driver version numbers in SFEnicdrv-* packages
- Update to vel-2.6.0, sige-2.6.2, myk-2.6.0
- Add nfo driver
* Tue Mar 26 2008 - trisk@acm.jhu.edu
- Fix compilation on amd64
* Sat Mar 22 2008 - trisk@acm.jhu.edu
- Add patch8 to fix GLDv3 compilation
- Use newer gem code for drivers
- Build GLDv3 versions when available
- Update compiler options
* Sun Feb 10 2008 - moinak.ghosh@sun.com
- Initial spec.
