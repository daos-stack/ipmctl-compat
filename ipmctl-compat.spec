Name:		ipmctl-compat
Version:	02.00.00.3885
Release:	1%{?dist}
Summary:	Utility for managing Intel Optane DC persistent memory modules
License:	BSD
URL:		https://github.com/intel/ipmctl
Source:		https://github.com/intel/ipmctl/archive/v%{version}/%{name}-%{version}.tar.gz
# https://bugzilla.redhat.com/show_bug.cgi?id=1628752
ExclusiveArch:	x86_64

Requires:	libipmctl-compat%{?_isa} = %{version}-%{release}
BuildRequires:	pkgconfig(libndctl)
BuildRequires:	cmake
%if 0%{?rhel} > 7
BuildRequires:	python3
%else
BuildRequires:	python
%endif
BuildRequires:	gcc
BuildRequires:	gcc-c++
%if 0%{?rhel} > 7
BuildRequires:	asciidoc
%else
BuildRequires:	asciidoctor
%endif
Conflicts:	ixpdimm-cli < 01.00.00.3000
Provides:	ipmctl = %{version}-%{release}
Provides:	ipmctl%{?_isa} = %{version}-%{release}


%description
Utility for managing Intel Optane DC persistent memory modules
Supports functionality to:
Discover DCPMMs on the platform.
Provision the platform memory configuration.
View and update the firmware on DCPMMs.
Configure data-at-rest security on DCPMMs.
Track health and performance of DCPMMs.
Debug and troubleshoot DCPMMs.

%prep
%setup -q -n ipmctl-%{version}

%package -n libipmctl-compat
Summary:	Library for Intel DCPMM management
Requires:	logrotate
Conflicts:	ixpdimm_sw < 01.00.00.3000
Conflicts:	libixpdimm-common < 01.00.00.3000
Conflicts:	libixpdimm-core < 01.00.00.3000
Conflicts:	libixpdimm-cli < 01.00.00.3000
Conflicts:	libixpdimm-cim < 01.00.00.3000
Conflicts:	libixpdimm < 01.00.00.3000
Conflicts:	ixpdimm-data < 01.00.00.3000
Provides:	libipmctl = %{version}-%{release}
Provides:	libipmctl%{?_isa} = %{version}-%{release}
Provides:	config(libipmctl) = %{version}-%{release} 


%description -n libipmctl-compat
An Application Programming Interface (API) library for managing Intel Optane DC
persistent memory modules.

%package -n libipmctl-compat-devel
Summary:	Development packages for libipmctl
Requires:	libipmctl-compat%{?_isa} = %{version}-%{release}
Conflicts:	ixpdimm-devel < 01.00.00.3000
Conflicts:	ixpdimm_sw-devel < 01.00.00.3000
Provides:	libipmctl-devel = %{version}-%{release}
Provides:	libipmctl-devel(x86-64) = %{version}-%{release}


%description -n libipmctl-compat-devel
API for development of Intel Optane DC persistent memory management utilities.

%build
%cmake -DBUILDNUM=%{version} -DCMAKE_INSTALL_PREFIX=/ \
    -DLINUX_PRODUCT_NAME=%{name} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
    -DCMAKE_INSTALL_BINDIR=%{_bindir} \
    -DCMAKE_INSTALL_DATAROOTDIR=%{_datarootdir} \
    -DCMAKE_INSTALL_MANDIR=%{_mandir} \
    -DCMAKE_INSTALL_LOCALSTATEDIR=%{_localstatedir} \
    -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
    -DRELEASE=ON \
    -DRPM_BUILD=ON
%if 0%{?rhel} > 7
%cmake_build
%else
%make_build
%endif

%install
%{!?_cmake_version: cd build}
%if 0%{?rhel} > 7
%cmake_install
%else
%make_install -f Makefile
%endif
# convert to -compat -- only really need the shared lib
rm -rf %{buildroot}{%{_bindir},%{_mandir},%{_datadir},%{_localstatedir},%{_sysconfdir}}/

%post -n libipmctl-compat -p /sbin/ldconfig

%postun -n libipmctl-compat -p /sbin/ldconfig

%files -n libipmctl-compat
%{_libdir}/libipmctl.so.4*
%doc LICENSE

%files -n libipmctl-compat-devel
%{_libdir}/libipmctl.so
%{_includedir}/nvm_types.h
%{_includedir}/nvm_management.h
%{_includedir}/export_api.h
%{_includedir}/NvmSharedDefs.h
%{_libdir}/pkgconfig/libipmctl.pc
%doc LICENSE

%changelog
* Mon Feb 13 2023 Brian J. Murrell <brian.murrell@intel.com> - 02.00.00.3885-1
- Initial package based on original ipmctl packaging
