# TODO
# - patch for vserver vfs_unlink
#
# Conditional build:
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	up		# don't build UP module
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
%bcond_without	vserver		# build with vserver patches
%bcond_with	grsec_kernel	# build for kernel-grsecurity
#
%if %{without kernel}
%undefine	with_dist_kernel
%endif
#
%if %{with kernel} && %{with dist_kernel} && %{with grsec_kernel}
%define	alt_kernel	grsecurity
%endif
#
%ifarch sparc
%undefine	with_smp
%endif

#define		_snap	20060916-2203
%define         _rel    0.1
#
Summary:	A Stackable Unification File System
Summary(pl.UTF-8):	Stakowalny, unifikujący system plików
Name:		unionfs
Version:	1.3
Release:	%{?_snap:0.%(echo %{_snap} | tr - _).}%{_rel}
License:	GPL v2
Group:		Base/Kernel
#Source0:	ftp://ftp.fsl.cs.sunysb.edu/pub/unionfs/snapshots/%{name}-%{_snap}.tar.gz
Source0:	ftp://ftp.fsl.cs.sunysb.edu/pub/unionfs/%{name}-%{version}.tar.gz
# Source0-md5:	af5106f29fb0ddb12b028f522fa0463c
Patch0:		%{name}-build.patch
#Patch1:		%{name}-vserver.patch
URL:		http://www.filesystems.org/project-unionfs.html
%if %{with kernel} && %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.17
BuildRequires:	kernel%{_alt_kernel}-module-build < 3:2.6.18
BuildRequires:	rpmbuild(macros) >= 1.330
%endif
BuildRequires:	libuuid-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Unionfs is a stackable unification file system, which can appear to
merge the contents of several directories (branches), while keeping
their physical content separate. Unionfs is useful for unified source
tree management, merged contents of split CD-ROM, merged separate
software package directories, data grids, and more. Unionfs allows any
mix of read-only and read-write branches, as well as insertion and
deletion of branches anywhere in the fan-out.

%description -l pl.UTF-8
Unionfs to stakowalny, unifikujący system plików, potrafiący łączyć
zawartość kilku katalogów (gałęzi), zachowując oddzielnie ich fizyczną
zawartość. Unionfs jest przydatny do zarządzania połączonym drzewem
źródeł, połączoną zawartością podzielonych CD-ROM-ów, połączonymi
oddzielnymi katalogami z pakietami programów, tabelami danych itp.
Unionfs pozwala na dowolne mieszanie gałęzi tylko do odczytu oraz do
odczytu i zapisu, a także wstawianie i usuwanie gałęzi w dowolnym
miejscu.

%package -n kernel%{_alt_kernel}-fs-unionfs
Summary:	Linux driver for unionfs
Summary(pl.UTF-8):	Sterownik Linuksa dla unionfs
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel%{_alt_kernel}-fs-unionfs
Linux driver for unionfs.

%description -n kernel%{_alt_kernel}-fs-unionfs -l pl.UTF-8
Sterownik Linuksa dla unionfs.

%package -n kernel%{_alt_kernel}-smp-fs-unionfs
Summary:	Linux SMP driver for unionfs
Summary(pl.UTF-8):	Sterownik Linuksa SMP dla unionfs
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Provides:	kernel%{_alt_kernel}-unionfs = %{version}-%{_rel}@%{_kernel_ver_str}

%description -n kernel%{_alt_kernel}-smp-fs-unionfs
Linux SMP driver unionfs.

%description -n kernel%{_alt_kernel}-smp-fs-unionfs -l pl.UTF-8
Sterownik Linuksa SMP dla unionfs.

%prep
%setup -q %{?_snap:-n %{name}-%{_snap}}
%patch0 -p1
#%{?with_vserver:%patch1 -p1}

%build
%if %{with kernel}
%build_kernel_modules -m unionfs \
	EXTRACFLAGS="-DUNIONFS_NDEBUG -DUNIONFS_XATTR"
%endif

%if %{with userspace}
%{__make} utils \
	CC="%{__cc}" \
	UNIONFS_OPT_CFLAG="%{rpmcflags} %{rpmldflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -m unionfs -d kernel/fs
%endif

%if %{with userspace}
%{__make} install-utils \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel%{_alt_kernel}-fs-unionfs
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-fs-unionfs
%depmod %{_kernel_ver}

%post -n kernel%{_alt_kernel}-smp-fs-unionfs
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-fs-unionfs
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS INSTALL README
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
%endif

%if %{with kernel}
%if %{with up} || %{without dist_kernel}
%files -n kernel%{_alt_kernel}-fs-unionfs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/fs/*.ko*
%endif

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-fs-unionfs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/fs/*.ko*
%endif
%endif
