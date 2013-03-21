%define _default_patch_fuzz 2

Name: corosync
Summary: The Corosync Cluster Engine and Application Programming Interfaces
Version: 1.2.3
Release: 21%{?dist}.1
License: BSD
Group: System Environment/Base
URL: http://ftp.corosync.org
Source0: ftp://ftp:user@ftp.corosync.org/downloads/%{name}-%{version}/%{name}-%{version}.tar.gz

Patch0: revision-2770-backported.patch
Patch1: revision-2785.patch
Patch2: revision-2799.patch
Patch3: revision-2801.patch
Patch4: revision-2814.patch
Patch5: revision-2923.patch
Patch6: revision-2924.patch
Patch7: revision-2925.patch
Patch8: revision-2926.patch
Patch9: revision-2927.patch
Patch10: revision-2928.patch
Patch11: revision-2929.patch
Patch12: revision-2930.patch
Patch13: revision-2931.patch
Patch14: revision-2932.patch
patch15: revision-2934.patch
patch16: revision-2935.patch
Patch17: revision-2936.patch
Patch18: revision-2937.patch
Patch19: revision-2938.patch
Patch20: revision-2945.patch
Patch21: revision-2947.patch
Patch22: revision-2951.patch
Patch23: revision-2952.patch
Patch24: revision-2954.patch
Patch25: revision-2965.patch
Patch26: revision-2966.patch
Patch27: revision-2967.patch
Patch28: revision-2968.patch
Patch29: revision-2969.patch
Patch30: revision-2971.patch
Patch31: revision-2973.patch
Patch32: revision-2975.patch
Patch33: revision-2977.patch
Patch34: revision-2978.patch
Patch35: revision-2985.patch
Patch36: revision-2987.patch
Patch37: revision-2989.patch
Patch38: revision-2998.patch
Patch39: revision-2999.patch
Patch40: revision-3000.patch
Patch41: revision-3003.patch
Patch42: revision-3004.patch
Patch43: revision-3006.patch
Patch44: revision-3013.patch
Patch45: revision-3023.patch
Patch46: revision-3040.patch
# Future patches are from the git tree
Patch47: 0001-Handle-delayed-multicast-packets-that-occur-with-swi.patch

ExclusiveArch: i686 x86_64

# Runtime bits
Requires: corosynclib = %{version}-%{release}
Requires(pre): /usr/sbin/useradd
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Conflicts: openais <= 0.89, openais-devel <= 0.89

# Build bits

BuildRequires: autoconf automake
BuildRequires: nss-devel
BuildRequires: libibverbs-devel librdmacm-devel

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%prep
%setup -q -n %{name}-%{version}
%patch0
%patch1
%patch2
%patch3
%patch4
%patch5
%patch6
%patch7
%patch8
%patch9
%patch10
%patch11
%patch12
%patch13
%patch14
%patch15
%patch16
%patch17
%patch18
%patch19
%patch20
%patch21
%patch22
%patch23
%patch24
%patch25
%patch26
%patch27
%patch28
%patch29
%patch30
%patch31
%patch32
%patch33
%patch34
%patch35
%patch36
%patch37
%patch38
%patch39
%patch40
%patch41
%patch42
%patch43
%patch44
%patch45
%patch46
%patch47 -p1

%build
./autogen.sh
export ibverbs_CFLAGS=-I/usr/include/infiniband \
export ibverbs_LIBS=-libverbs \
export rdmacm_CFLAGS=-I/usr/include/rdma \
export rdmacm_LIBS=-lrdmacm \
%{configure} \
	--enable-nss \
	--enable-rdma \
	--with-initddir=%{_initddir}
make %{_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}
mkdir -p -m 0700 %{buildroot}/%{_localstatedir}/log/cluster


## tree fixup
# drop static libs
rm -f %{buildroot}%{_libdir}/*.a
# drop docs and html docs for now
rm -rf %{buildroot}%{_docdir}/*

%clean
rm -rf %{buildroot}

%description
This package contains the Corosync Cluster Engine Executive, several default
APIs and libraries, default configuration files, and an init script.

%post
/sbin/chkconfig --add corosync || :

%preun
if [ $1 -eq 0 ]; then
	/sbin/service corosync stop &>/dev/null || :
	/sbin/chkconfig --del corosync || :
fi

%files
%defattr(-,root,root,-)
%doc LICENSE SECURITY
%{_sbindir}/corosync
%{_sbindir}/corosync-keygen
%{_sbindir}/corosync-objctl
%{_sbindir}/corosync-cfgtool
%{_sbindir}/corosync-fplay
%{_sbindir}/corosync-pload
%{_sbindir}/corosync-cpgtool
%{_sbindir}/corosync-quorumtool
%{_bindir}/corosync-blackbox
%dir %{_sysconfdir}/corosync
%dir %{_sysconfdir}/corosync/service.d
%dir %{_sysconfdir}/corosync/uidgid.d
%config(noreplace) %{_sysconfdir}/corosync/corosync.conf.example
%{_initddir}/corosync
%dir %{_libexecdir}/lcrso
%{_libexecdir}/lcrso/coroparse.lcrso
%{_libexecdir}/lcrso/objdb.lcrso
%{_libexecdir}/lcrso/service_cfg.lcrso
%{_libexecdir}/lcrso/service_cpg.lcrso
%{_libexecdir}/lcrso/service_evs.lcrso
%{_libexecdir}/lcrso/service_confdb.lcrso
%{_libexecdir}/lcrso/service_pload.lcrso
%{_libexecdir}/lcrso/quorum_votequorum.lcrso
%{_libexecdir}/lcrso/quorum_testquorum.lcrso
%{_libexecdir}/lcrso/vsf_quorum.lcrso
%{_libexecdir}/lcrso/vsf_ykd.lcrso
%dir %{_localstatedir}/lib/corosync
%dir %{_localstatedir}/log/cluster
%{_mandir}/man8/corosync_overview.8*
%{_mandir}/man8/corosync.8*
%{_mandir}/man8/corosync-blackbox.8*
%{_mandir}/man8/corosync-objctl.8*
%{_mandir}/man8/corosync-keygen.8*
%{_mandir}/man8/corosync-cfgtool.8*
%{_mandir}/man8/corosync-cpgtool.8*
%{_mandir}/man8/corosync-fplay.8*
%{_mandir}/man8/corosync-pload.8*
%{_mandir}/man8/corosync-quorumtool.8*
%{_mandir}/man5/corosync.conf.5*


%package -n corosynclib
Summary: The Corosync Cluster Engine Libraries
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description -n corosynclib
This package contains corosync libraries.

%files -n corosynclib
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/libcfg.so.*
%{_libdir}/libcpg.so.*
%{_libdir}/libconfdb.so.*
%{_libdir}/libevs.so.*
%{_libdir}/libtotem_pg.so.*
%{_libdir}/liblogsys.so.*
%{_libdir}/libcoroipcc.so.*
%{_libdir}/libcoroipcs.so.*
%{_libdir}/libquorum.so.*
%{_libdir}/libvotequorum.so.*
%{_libdir}/libpload.so.*
%{_libdir}/libsam.so.*

%post -n corosynclib -p /sbin/ldconfig

%postun -n corosynclib -p /sbin/ldconfig

%package -n corosynclib-devel
Summary: The Corosync Cluster Engine Development Kit
Group: Development/Libraries
Requires: corosynclib = %{version}-%{release}
Requires: pkgconfig
Provides: corosync-devel = %{version}
Obsoletes: corosync-devel < 0.92-7

%description -n corosynclib-devel
This package contains include files and man pages used to develop using
The Corosync Cluster Engine APIs.

%files -n corosynclib-devel
%defattr(-,root,root,-)
%doc LICENSE README.devmap
%dir %{_includedir}/corosync/
%{_includedir}/corosync/cs_config.h
%{_includedir}/corosync/corodefs.h
%{_includedir}/corosync/coroipc_types.h
%{_includedir}/corosync/coroipcs.h
%{_includedir}/corosync/coroipcc.h
%{_includedir}/corosync/cfg.h
%{_includedir}/corosync/confdb.h
%{_includedir}/corosync/corotypes.h
%{_includedir}/corosync/cpg.h
%{_includedir}/corosync/evs.h
%{_includedir}/corosync/hdb.h
%{_includedir}/corosync/list.h
%{_includedir}/corosync/mar_gen.h
%{_includedir}/corosync/sam.h
%{_includedir}/corosync/swab.h
%{_includedir}/corosync/quorum.h
%{_includedir}/corosync/votequorum.h
%dir %{_includedir}/corosync/totem/
%{_includedir}/corosync/totem/coropoll.h
%{_includedir}/corosync/totem/totem.h
%{_includedir}/corosync/totem/totemip.h
%{_includedir}/corosync/totem/totempg.h
%dir %{_includedir}/corosync/lcr/
%{_includedir}/corosync/lcr/lcr_ckpt.h
%{_includedir}/corosync/lcr/lcr_comp.h
%{_includedir}/corosync/lcr/lcr_ifact.h
%dir %{_includedir}/corosync/engine
%{_includedir}/corosync/engine/config.h
%{_includedir}/corosync/engine/coroapi.h
%{_includedir}/corosync/engine/logsys.h
%{_includedir}/corosync/engine/objdb.h
%{_includedir}/corosync/engine/quorum.h
%{_libdir}/libcfg.so
%{_libdir}/libcpg.so
%{_libdir}/libconfdb.so
%{_libdir}/libevs.so
%{_libdir}/libtotem_pg.so
%{_libdir}/liblogsys.so
%{_libdir}/libcoroipcc.so
%{_libdir}/libcoroipcs.so
%{_libdir}/libquorum.so
%{_libdir}/libvotequorum.so
%{_libdir}/libpload.so
%{_libdir}/libsam.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/cpg_*3*
%{_mandir}/man3/evs_*3*
%{_mandir}/man3/confdb_*3*
%{_mandir}/man3/votequorum_*3*
%{_mandir}/man3/sam_*3*
%{_mandir}/man8/cpg_overview.8*
%{_mandir}/man8/evs_overview.8*
%{_mandir}/man8/confdb_overview.8*
%{_mandir}/man8/logsys_overview.8*
%{_mandir}/man8/votequorum_overview.8*
%{_mandir}/man8/coroipc_overview.8*
%{_mandir}/man8/sam_overview.8*

%changelog
* Tue Jan 11 2011 Steven Dake <sdake@edhat.com> 1.2.3-21.1
- Resolves: rhbz#638592
- merge upstream commit bab4945b57c150301c034085f3ce7b4187b6c864
-  Works around problem where some switch hardware delays multicast
-  packets compared to the unicast token.  This would result in messages
-  being retransmitted when no retransmission was necessary.

* Tue Sep 7 2010 Steven Dake <sdake@redhat.com> 1.2.3-21
- Resolves: rhbz#630106
- merge upstream revision 3040 - change stop level from 20 to 80.

* Wed Aug 18 2010 Steven Dake <sdake@redhat.com> 1.2.3-20
- Resolves: rhbz#623790
- properly apply patch from 1.2.3-19

* Tue Aug 17 2010 Steven Dake <sdake@redhat.com> 1.2.3-19
- Resolves: rhbz#623790
- Add upstream revision 3023 - Properly detect server failure instead of falsely
  detecting during a configuration change.

* Tue Aug 3 2010 Steven Dake <sdake@redhat.com> 1.2.3-18
- Resolves: rhbz#619565
- Add upstream revision 3013 - dont cancel token retransmit timeout on receipt
  of a multicast message.

* Tue Jul 27 2010 Steven Dake <sdake@redhat.com> 1.2.3-17
- Resolves: rhbz#618570
- Add upstream revision 3006 - Remove consensus timeout floor check that leads
  to exit in two node clusters with smaller consensus timeouts.

* Thu Jul 22 2010 Angus Salkeld <asalkeld@redhat.com> 1.2.3-16
- Resolves: rhbz#579126
- Add upstream revision 3004 - Fix merge error with revision 3001.
- Add upstream revision 3003 - Fix problem where flow control could lock
  up ipc under very heavy load in very rare circumstances.
* Mon Jul 19 2010 Steven Dake <sdake@redhat.com> 1.2.3-15
- Resolves: rhbz#611676
- Add upstream revision 3000 - ensure aborts happen even if the currently
  running sync engine doesn't have an abort operation.
- Add upstream revision 2999 - reset internal variable in syncv2 on
  configuration change.

* Mon Jul 19 2010 Steven Dake <sdake@redhat.com> 1.2.3-14
- Resolves: rhbz#615203
- Add upstream revision 2998 - Fix logging_daeon cofig parser code.

* Wed Jul 14 2010 Steven Dake <sdake@redhat.com> 1.2.3-13
- Resolves: rhbz#614219
- Add upstream revision 2989 - Don't reset the token timer when a retransmitted
  token is received.  Only reset when a token is received.

* Wed Jul 7 2010 Steven dake <sdake@redhat.com> 1.2.3-12
- Resolves: rhbz#612292
- Add upstream revision 2987 - speed up connection process as a result of
  performance regression in upstream revision 2973.

* Tue Jul 6 2010 Steven Dake <sdake@redhat.com> 1.2.3-11
- Resolves: rhbz#580741
- Resolves: rhbz#605313
- Add upstream revision 2985 - fix fail list fault that occurs in very rare
  circumstances.
- Add upstream revision 2977 - fix mutex deadlock that occurs during cman
  reload.

* Tue Jul 6 2010 Steven Dake <sdake@redhat.com> 1.2.3-10
- Resolves: rhbz#583844
- Add upstream trunk revision 2814 - fix syncing of cpg downlist in certain circumstances
- Add upstream trunk revision 2785 - fix syncing of cpg downlist in certain circumstances.
- Add upstream trunk revision 2801 - fix syncing of cpg downlist in certain circumstances.
 
* Wed Jun 30 2010 Steven Dake <sdake@redhat.com> 1.2.3-9
- Resolves: rbhz#606463
- Add upstream revision 2978 - use freopen as to not cause glibc/fork to
  segfault in some rare circumstances when using pacemaker.

* Tue Jun 29 2010 Steven Dake <sdake@redhat.com> 1.2.3-8
- Resolves: rhbz#609198
- Add upstream revision 2975 - properly size all buffers used to describe the
  file names to PATH_MAX used in mappings in ipc layer.

* Tue Jun 29 2010 Steven dake <sdake@redhat.com> 1.2.3-7
- Resolves: rhbz#607738
- Add upstream revision 2973 - if /dev/shm is full, ipc clients will bus error - return error instead

* Mon Jun 28 2010 Steven Dake <sdake@redhat.com> 1.2.3-6
- Resolves: rhbz#596550
- Resolves: rhbz#606335
- Resolves: rhbz#607480
- Resolves: rhbz#607292
- Add upstream revision 2965 - add a man page for corosync-blackbox
- Add upstream revision 2966 - add a man page for corosync
- Add upstream revision 2967 - Add makefile and specfile changes to support 2965/2966
- Add upstream revision 2968 - remove use of pathconf which can fail resulting in segfault
- Add upstream revision 2969 - remove use of pathconf which can fail resulting in segfault
- Add upstream revision 2971 - add /var/log/cluster as owned directory and change example config file to log in /var/log/cluster

*Mon Jun 28 2010 Steven Dake <sdake@redhat.com> 1.2.3-5
- Reverts: rhbz#583844
- Revert trunk revision 2814 - fix syncing of cpg downlist in certain circumstances
- Revert upstream trunk revision 2785 - fix syncing of cpg downlist in certain circumstances.
- Revert upstream trunk revision 2801 - fix syncing of cpg downlist in certain circumstances.

* Tue Jun 22 2010 Steven Dake <sdake@redhat.com> 1.2.3-4
- Resolves: rhbz#583844
- Add trunk revision 2814 - fix syncing of cpg downlist in certain circumstances

* Mon Jun 21 2010 Steven Dake <sdake@redhat.com> 1.2.3-3
- Resolves: rhbz#600118
- Resolves: rhbz#606463
- Resolves: rhbz#583844
- Resolves: rhbz#605860
- Resolves: rhbz#605860
- Add upstream trunk revision 2785 - fix syncing of cpg downlist in certain circumstances.
- Add upstream trunk revision 2799 - fix problem where blackbox data isn't written during sos requests
- Add upstream trunk revision 2801 - fix syncing of cpg downlist in certain circumstances.
- Add upstream revision 2951 - fix segfault in fork() inside pacemaker service engine.
- Add upstream revision 2952 - fix problem where corosync deadlocks on single cpu system in spinlock call
- Add upstream revision 2954 - fix problem where totem stats updater triggers segfault when it's timer expires during shutdown

* Tue Jun 15 2010 Steven Dake <sdake@redhat.com> 1.2.3-2
- Resolves: rhbz#603886
- Resolves: rhbz#601018
- Resolves: rhbz#600068
- Resolves: rhbz#600043
- Resolves: rhbz#598680
- Resolves: rhbz#601011
- Resolves: rhbz#596550
- Resolves: rhbz#596552
- Resolves: rhbz#596405
- Resolves: rhbz#594924
- Resolves: rhbz#583844
- Add upstream revision 2947 - send CPG_REASON_PROCDOWN instead of
  CPG_REASON_LEAVE on proces exit.
- Add upstream revision 2945 - object_key_iter can dereference an invalid
  pointer
- Add upstream revision 2938 - have logsys use file mapped backing properly as
  intended
- Add upstream revision 2937 - handle sem_wait interrupted by signal properly
- Add upstream revision 2936 - fix fail to recv logic which happens rarely on
  high loss networks
- Add upstream revision 2935 - fix last_aru logic
- Add upstream revision 2934 - evs service fails to deliver messages
- Add upstream revision 2932 - Add man page for corosync-quorumtool
- Add upstream revision 2931 - Add man page for corosync-pload
- Add upstream revision 2930 - Add man page for corosync-fplay
- Add upstream revision 2929 - Add man page for corosync-cpgtool
- Add upstream revision 2928 - Add man page for corosync-cfgtool
- Add upstream revision 2927 - Add man page for corosync-keygen
- Add upstream revision 2926 - Update of corosync_overview man page
- Add upstream revision 2925 - resolve undefined behavior caused by sem_wait
  interruption by signals in coroipc
- Add upstream revision 2924 - Resolve problem where errant memcpy() operation
  sets incorrect scheduling parameters
- Add upstream revision 2923 - corosync won't build without corosync already
  intalled

* Wed May 19 2010 Steven dake <sdake@redhat.com> 1.2.3-1
- Resolves: rhbz#583800
- Rebase to upstream 1.2.3.
- Resolves 43 errors found with coverity.
- Fixes defects with totemsrp in 90% multicast message loss cases found
  through a field deployment.

* Sun May 16 2010 Steven Dake <sdake@redhat.com> 1.2.2-1
- Resolves: rhbz#583800
- Resolves: rhbz#553375
- Resolves: rhbz#582947
- Resolves: rhbz#553375
- Rebase to upstream 1.2.2.
- Add upstream trunk revision 2770 to add cpg_model_initialize api.

* Wed May 12 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.1-5
- Resolves: rhbz#590983
- Do not build corosync on ppc and ppc64

* Tue Mar 23 2010 Steven Dake <sdake@redhat.com> 1.2.1-4
- Resolves: rhbz#574516
- Rebase to upstream 1.2.1.

* Thu Feb 25 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.0-3
- Resolves: rhbz#567995
- Do not build corosync on s390 and s390x

* Tue Jan 12 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.0-2
- Resolves: rhbz#554855
- Do not build IB support on s390 and s390x

* Tue Dec  8 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.0-1
- New upstream release
- Use global instead of define
- Update Source0 url
- Use more %name macro around
- Cleanup install section. Init script is now installed by upstream
- Cleanup whitespace
- Don't deadlock between package upgrade and corosync condrestart
- Ship service.d config directory
- Fix Conflicts vs Requires
- Ship new sam library and man pages

* Fri Oct 23 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.1.2-1
- New upstream release fixes major regression on specific loads

* Wed Oct 21 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.1.1-1
- New upstream release

* Fri Sep 25 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.1.0-1
- New upstream release
- spec file updates:
  * enable IB support
  * explicitly define built-in features at configure time

* Tue Sep 22 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.0.1-1
- New upstream release
- spec file updates:
  * use proper configure macro

* Tue Jul 28 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.0.0-3
- spec file updates:
  * more consistent use of macros across the board
  * fix directory ownership

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul  8 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.0.0-1
- New upstream release

* Thu Jul  2 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.100-1
- New upstream release

* Sat Jun 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.98-1
- New upstream release
- spec file updates:
  * Drop corosync-trunk patch and alpha tag.
  * Fix alphatag vs buildtrunk handling.
  * Drop requirement on ais user/group and stop creating them.
  * New config file locations from upstream: /etc/corosync/corosync.conf.

* Wed Jun 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.97-1.svn2233
- spec file updates:
  * Update to svn version 2233 to include library linking fixes

* Wed Jun 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.97-1.svn2232
- New upstream release
- spec file updates:
  * Drop pkgconfig fix that's now upstream
  * Update to svn version 2232
  * Define buildtrunk if we are using svn snapshots
  * BuildRequires: nss-devel to enable nss crypto for network communication
  * Force autogen invokation if buildtrunk is defined
  * Whitespace cleanup
  * Stop shipping corosync.conf in favour of a generic example
  * Update file list

* Mon Mar 30 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.95-2
- Backport svn commit 1913 to fix pkgconfig files generation
  and unbreak lvm2 build.

* Tue Mar 24 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.95-1
- New upstream release
- spec file updates:
  * Drop alpha tag
  * Drop local patches (no longer required)
  * Allow to build from svn trunk by supporting rpmbuild --with buildtrunk 
  * BuildRequires autoconf automake if building from trunk
  * Execute autogen.sh if building from trunk and if no configure is available
  * Switch to use rpm configure macro and set standard install paths
  * Build invokation now supports _smp_mflags
  * Remove install section for docs and use proper doc macro instead
  * Add tree fixup bits to drop static libs and html docs (only for now)
  * Add LICENSE file to all subpackages
  * libraries have moved to libdir. Drop ld.so.conf.d corosync file
  * Update BuildRoot usage to preferred versions/names

* Tue Mar 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-5.svn1797
- Update the corosync-trunk patch for real this time.

* Tue Mar 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-4.svn1797
- Import fixes from upstream:
  * Cleanup logsys format init around to use default settings (1795)
  * logsys_format_set should use its own internal copy of format_buffer (1796)
  * Add logsys_format_get to logsys API (1797)
- Cherry pick svn1807 to unbreak CPG.

* Mon Mar  9 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-3.svn1794
- Import fixes from upstream:
  * Add reserve/release feature to totem message queue space (1793)
  * Fix CG shutdown (1794)

* Fri Mar  6 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-2.svn1792
- Import fixes from upstream:
  * Fix uninitialized memory. Spotted by valgrind (1788)
  * Fix logsys_set_format by updating the right bits (1789)
  * logsys: re-add support for timestamp  (1790)
  * Fix cpg crash (1791)
  * Allow logsys_format_set to reset to default (1792)

* Tue Mar  3 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-1
- New upstream release.
- Drop obsolete patches.
- Add soname bump patch that was missing from upstream.

* Wed Feb 25 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.93-4
- Add Makefile fix to install all corosync tools (commit r1780)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.93-2
- Rename gcc-4.4 patch to match svn commit (r1767).
- Backport patch from trunk (commit r1774) to fix quorum engine.

* Thu Feb 19 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.93-1
- New upstream release.
- Drop alphatag from spec file.
- Drop trunk patch.
- Update Provides for corosynclib-devel.
- Backport gcc-4.4 build fix from trunk.

* Mon Feb  2 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.92-7.svn1756
- Update to svn trunk at revision 1756 from upstream.
- Add support pkgconfig to devel package.
- Tidy up spec files by re-organazing sections according to packages.
- Split libraries from corosync to corosynclib.
- Rename corosync-devel to corosynclib-devel.
- Comply with multiarch requirements (libraries).

* Tue Jan 27 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.92-6.svn1750
- Update to svn trunk at revision 1750 from upstream.
- Include new quorum service in the packaging.

* Mon Dec 15 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.92-5.svn1709
- Update to svn trunk at revision 1709 from upstream.
- Update spec file to include new include files.

* Wed Dec 10 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.92-4.svn1707
- Update to svn trunk at revision 1707 from upstream.
- Update spec file to include new lcrso services and include file.

* Mon Oct 13 2008 Dennis Gilmore <dennis@ausil.us> - 0.92-3
- remove ExclusiveArch line

* Fri Sep 24 2008 Steven Dake <sdake@redhat.com> - 0.92-2
- Add conflicts for openais and openais-devel packages older then 0.90.

* Wed Sep 24 2008 Steven Dake <sdake@redhat.com> - 0.92-1
- New upstream release corosync-0.92.

* Sun Aug 24 2008 Steven Dake <sdake@redhat.com> - 0.91-3
- move logsys_overview.8.* to devel package.
- move shared libs to main package.

* Wed Aug 20 2008 Steven Dake <sdake@redhat.com> - 0.91-2
- use /sbin/service instead of calling init script directly.
- put corosync-objctl man page in the main package.
- change all initrddir to initddir for fedora 10 guidelines.

* Thu Aug 14 2008 Steven Dake <sdake@redhat.com> - 0.91-1
- First upstream packaged version of corosync for rawhide review.
