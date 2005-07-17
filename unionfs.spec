# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
Summary:	A Stackable Unification File System
Name:		unionfs
Version:	1.0.12a
%define         _rel    0.1
Release:        %{_rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	ftp://ftp.fsl.cs.sunysb.edu/pub/unionfs/unionfs-%{version}.tar.gz
# Source0-md5:	6d7f0b7e111d40cd8799510c6a9eca92
URL:		http://www.filesystems.org/project-unionfs.html
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.153
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Unionfs is a stackable unification file system, which can appear to
merge the contents of several directories (branches), while keeping
their physical content separate.  Unionfs is useful for unified source
tree management, merged contents of split CD-ROM, merged separate
software package directories, data grids, and more.  Unionfs allows
any mix of read-only and read-write branches, as well as insertion and
deletion of branches anywhere in the fan-out.

%package -n kernel-unionfs
Summary:	Linux driver for unionfs
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Provides:	kernel-unionfs = %{version}-%{_rel}@%{_kernel_ver_str}

%description -n kernel-unionfs
Linux driver for unionfs

%package -n kernel-smp-unionfs
Summary:	Linux SMP driver for unionfs
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Provides:	kernel-unionfs = %{version}-%{_rel}@%{_kernel_ver_str}

%description -n kernel-smp-unionfs
Linux SMP driver unionfs

%prep
%setup -q

%build
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{config,linux}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	touch include/config/MARKER
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	mv unionfs{,-$cfg}.ko
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/fs
install unionfs-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/fs/unionfs.ko
%if %{with smp} && %{with dist_kernel}
install unionfs-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/fs/unionfs.ko
%endif

%{__make} install-utils \
	PREFIX=$RPM_BUILD_ROOT/usr \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel-unionfs
%depmod %{_kernel_ver}

%postun -n kernel-unionfs
%depmod %{_kernel_ver}

%post -n kernel-smp-unionfs
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-unionfs
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS INSTALL README
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*

%files -n kernel-unionfs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/fs/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-unionfs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/fs/*.ko*
%endif
