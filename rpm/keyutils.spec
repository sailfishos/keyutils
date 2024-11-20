%define libapivermajor 1
%define libapiversion %{libapivermajor}.10

Name:    keyutils
Version: 1.6.3
Release: 1
Summary: Linux Key Management Utilities
License: GPLv2+ and LGPLv2+
Url:   https://github.com/sailfishos/keyutils
Source0: keyutils-%{version}.tar.gz
Requires: %{name}-libs = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Utilities to control the kernel key management facility and to provide
a mechanism by which the kernel call back to user space to get a key
instantiated.

%package libs
Summary: Key utilities library

%description libs
This package provides a wrapper library for the key management facility system
calls.

%package libs-devel
Summary: Development package for building Linux key management utilities
Requires: %{name}-libs = %{version}-%{release}

%description libs-devel
This package provides headers and libraries for building key utilities.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
make \
	NO_ARLIB=1 \
	ETCDIR=%{_sysconfdir} \
	LIBDIR=%{_libdir} \
	USRLIBDIR=%{_libdir} \
	BINDIR=%{_bindir} \
	SBINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	INCLUDEDIR=%{_includedir} \
	SHAREDIR=%{_datadir}/%{name} \
	RELEASE=.%{release} \
	NO_GLIBC_KEYERR=1 \
	CFLAGS="-Wall $RPM_OPT_FLAGS" \
	LDFLAGS="%{?__global_ldflags}"

%install
make \
	NO_ARLIB=1 \
	DESTDIR=$RPM_BUILD_ROOT \
	ETCDIR=%{_sysconfdir} \
	LIBDIR=%{_libdir} \
	USRLIBDIR=%{_libdir} \
	BINDIR=%{_bindir} \
	SBINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	INCLUDEDIR=%{_includedir} \
	SHAREDIR=%{_datadir}/%{name} \
	install

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%doc README
%license LICENCE.GPL
%config(noreplace) %{_sysconfdir}/*
%{_bindir}/keyctl
%{_sbindir}/key.dns_resolver
%{_sbindir}/request-key
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_mandir}/man7/*

%files libs
%license LICENCE.LGPL
%{_libdir}/libkeyutils.so.%{libapiversion}
%{_libdir}/libkeyutils.so.%{libapivermajor}

%files libs-devel
%{_libdir}/libkeyutils.so
%{_includedir}/keyutils.h
%{_libdir}/pkgconfig/libkeyutils.pc
%{_mandir}/man3/*
