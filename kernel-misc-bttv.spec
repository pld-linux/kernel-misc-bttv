#
# TODO: UP/SMP (if this spec is useful for something now?)
#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
#
%define		no_install_post_compress_modules	1

%define		_orig_name	bttv
Summary:	BrookTree TV tuner driver
Summary(pl.UTF-8):   Sterownik dla kart TV na chipsecie BrookTree
Name:		kernel-misc-bttv
Version:	0.9.13
Release:	1
License:	GPL
Group:		Base/Kernel
Source0:	http://www.strusel007.de/linux/bttv/%{_orig_name}-%{version}.tar.gz
# Source0-md5:	1505d9de8ca4afcd774f00d4bc42c8b9
URL:		http://www.strusel007.de/linux/bttv/
#BuildRequires:	i2c-devel
BuildRequires:	kernel-module-build
BuildRequires:	rpmbuild(macros) >= 1.118
#Requires:	i2c
Requires:	modutils
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kernel modules which add support for TV cards based on BrookTree BT
848 and 878 chips.

%description -l pl.UTF-8
Moduły jądra dodające obsługę kart TV na układach BrookTree BT 848 i
878.

%package -n kernel-smp-misc-bttv
Summary:	Kernel SMP modules for BrookTree TV tuner
Summary(pl.UTF-8):   Moduły SMP jądra do obsługi tunerów TV BrookTree
Release:	%{release}@%{_kernel_ver_str}
Group:		Base/Kernel
#Requires:	%{name} = %{version}
Requires:	modutils >= 2.4.6-4
Obsoletes:	bttv

%description -n kernel-smp-misc-bttv
Kernel SMP modules which add support for TV cards based on BrookTree
BT 848 and 878 chips.

%description -n kernel-smp-misc-bttv -l pl.UTF-8
Moduły SMP jądra dodające obsługę kart TV na układach BrookTree BT 848
i 878.

%package devel
Summary:	Header files for bttv
Summary(pl.UTF-8):   Pliki nagłówkowe bttv
Group:		Development

%description devel
Header files for bttv.

%description devel -l pl.UTF-8
Pliki nagłówkowe bttv.

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
%doc CARDLIST Changes Insmod-options README* Sound-FAQ Specs Cards
/lib/modules/%{_kernel_ver}/kernel/drivers/misc/*

%files -n kernel-smp-misc-bttv
%defattr(644,root,root,755)
%doc CARDLIST Changes Insmod-options README* Sound-FAQ Specs Cards
/lib/modules/%{_kernel_ver}smp/kernel/drivers/misc/*

#%files devel
#%defattr(644,root,root,755)
#%{_kernelsrcdir}/drivers/char/*
