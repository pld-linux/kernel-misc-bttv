#
# TODO: UP/SMP (if this spec is useful for something now?)
#
# Conditional build:
%bcond_without  dist_kernel	# without kernel from distribution
#
%define		no_install_post_compress_modules	1

%define		_orig_name	bttv
Summary:	BrookTree TV tuner driver
Summary(pl):	Sterownik dla kart TV na chipsecie BrookTree
Name:		kernel-misc-bttv
Version:	0.9.13
Release:	1@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://www.strusel007.de/linux/bttv/%{_orig_name}-%{version}.tar.gz
# Source0-md5:	1505d9de8ca4afcd774f00d4bc42c8b9
URL:		http://www.strusel007.de/linux/bttv/
ExclusiveArch:	%{ix86}
#Requires:	i2c
PreReq:		modutils
#BuildRequires:	i2c-devel
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRequires:	kernel-module-build
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kernel modules which add support for TV cards based on BrookTree BT
848 and 878 chips.

%description -l pl
Modu³y j±dra dodaj±ce obs³ugê kart TV na uk³adach BrookTree BT 848 i
878.

%package -n kernel-smp-misc-bttv
Summary:	Kernel SMP modules for BrookTree TV tuner
Summary(pl):	Modu³y SMP j±dra do obs³ugi tunerów TV BrookTree
Group:		Base/Kernel
Release:	%{release}@%{_kernel_ver_str}
PreReq:		modutils >= 2.4.6-4
#Requires:	%{name} = %{version}
Obsoletes:	bttv

%description -n kernel-smp-misc-bttv
Kernel SMP modules which add support for TV cards based on BrookTree BT
848 and 878 chips.

%description -n kernel-smp-misc-bttv -l pl
Modu³y SMP j±dra dodaj±ce obs³ugê kart TV na uk³adach BrookTree BT 848 i
878.

%package devel
Summary:	Header files for bttv
Summary(pl):	Pliki nag³ówkowe bttv
Group:		Development

%description devel
Header files for bttv.

%description devel -l pl
Pliki nag³ówkowe bttv.

%prep
%setup	-q -n %{_orig_name}-%{version}

%build
install -d build-done/{UP,SMP}
ln -sf %{_kernelsrcdir}/config-up .config
rm -rf include
install -d include/{linux,config}
ln -sf %{_kernelsrcdir}/include/linux/autoconf.h include/linux/autoconf.h
ln -sf %{_kernelsrcdir}/asm-%{_arch} include/asm
touch include/config/MARKER
%{__make} -C %{_kernelsrcdir} SUBDIRS=$PWD O=$PWD V=1 modules
mv *.ko build-done/UP/

%{__make} -C %{_kernelsrcdir} SUBDIRS=$PWD O=$PWD V=1 mrproper

ln -sf %{_kernelsrcdir}/config-smp .config
rm -rf include
install -d include/{linux,config}
ln -sf %{_kernelsrcdir}/include/linux/autoconf.h include/linux/autoconf.h
ln -sf %{_kernelsrcdir}/asm-%{_arch} include/asm
touch include/config/MARKER
%{__make} -C %{_kernelsrcdir} SUBDIRS=$PWD O=$PWD V=1 modules

mv *.ko build-done/SMP/

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/misc

cp build-done/UP/* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/misc
cp build-done/SMP/* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/misc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-misc-bttv
%depmod %{_kernel_ver}

%postun	-n kernel-misc-bttv
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-bttv
%depmod %{_kernel_ver}

%postun	-n kernel-smp-misc-bttv
%depmod %{_kernel_ver}

%files -n kernel-misc-bttv
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/misc/*

%files -n kernel-smp-misc-bttv
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/misc/*

#%files devel
#%defattr(644,root,root,755)
#/usr/src/linux/drivers/char/*
