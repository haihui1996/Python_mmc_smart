import ctypes


# 定义结构体类型

class sOWN_HealthInfo_NOTICES(ctypes.Structure):
    _fields_ = [

        ("u32Issuse_ErrLog", ctypes.c_uint, 1),

        ("u32Issuse_UECC", ctypes.c_uint, 1),

        ("u32Issuse_softdecode", ctypes.c_uint, 1),

        ("u32Issuse_RunTimeBad", ctypes.c_uint, 1),

        ("u32Issuse_WearLeveling", ctypes.c_uint, 1),

        ("u32Issuse_VDT", ctypes.c_uint, 1),

        ("u32IssuseRSV", ctypes.c_uint, 26),

        ("u32NoticesRSV", ctypes.c_uint * 1)

    ]


class sOWN_Root(ctypes.Structure):
    _fields_ = [

        ("u32RootFwVer", ctypes.c_uint),

        ("u32PORCnt", ctypes.c_uint),

        ("u32RootExchangeCnt", ctypes.c_uint),

        ("u32RootStatus", ctypes.c_uint)

    ]


class sOWN_NandFeature(ctypes.Structure):
    _fields_ = [

        ("u08FlashID", ctypes.c_ubyte * 6),

        ("u08CeCnt", ctypes.c_ubyte),

        ("u08LunPerCe", ctypes.c_ubyte),

        ("u08MultiPlane", ctypes.c_ubyte),

        ("u08Rsv3", ctypes.c_ubyte * 3),

        ("u16FBlkPerCe", ctypes.c_ushort),

        ("u16PagePerBlk", ctypes.c_ushort),

        ("u16StrPagePerBlk", ctypes.c_ushort),

        ("u16PageSize", ctypes.c_ushort),

        ("u08SectPerFPage", ctypes.c_ubyte),

        ("u08EccBits", ctypes.c_ubyte),

        ("u08EccBitTh", ctypes.c_ubyte),

        ("u08SpareSize", ctypes.c_ubyte),

        ("u08LdpcSoftDecodeMode", ctypes.c_ubyte),

        ("u08LdpcSoftDecodeType", ctypes.c_ubyte),

        ("u08LdpcParityLength", ctypes.c_ubyte),

        ("u08SpareLength", ctypes.c_ubyte),
        ("u32Cap", ctypes.c_uint)

    ]


class sOWN_ErrorInfo(ctypes.Structure):
    _fields_ = [

        ("u08ErrStatus", ctypes.c_ubyte),

        ("u08Rsv1", ctypes.c_ubyte * 3),

        ("u32RootEccUncCnt", ctypes.c_uint),

        ("u32ClusterEccUncCnt", ctypes.c_uint),

        ("u32RootSporCnt", ctypes.c_uint),
        ("u32ClusterSporCnt", ctypes.c_uint),

        ("u32TargetSporCnt", ctypes.c_uint),

        ("u32TargetSporDropDataCnt", ctypes.c_uint)

    ]


class sBlkPEInfo(ctypes.Structure):
    _fields_ = [

        ("u32MaxEraseCnt_SLC", ctypes.c_uint),

        ("u32MinEraseCnt_SLC", ctypes.c_uint),

        ("u32MaxEraseCnt_NOR", ctypes.c_uint),

        ("u32MinEraseCnt_NOR", ctypes.c_uint),

        ("u32MapMaxEraseCnt", ctypes.c_uint),

        ("u32MapMinEraseCnt", ctypes.c_uint)

    ]

__FTL_Statistics_TAG__ = int(0x5aaa555a)
class sOWN_HealthInfo_FTL_Statistics(ctypes.Structure):
    _fields_ = [

        ("u32FTL_StaTAG", ctypes.c_uint),

        ("u16BadCnt", ctypes.c_ushort),

        ("u08WAF_Integer", ctypes.c_ubyte),

        ("u08WAF_Decimal", ctypes.c_ubyte),

        ("u32RetryCnt", ctypes.c_uint),

        ("u32SoftDecodeCnt", ctypes.c_uint),

        ("u32EccUncCnt", ctypes.c_uint),

        ("u32RefreshCnt", ctypes.c_uint),

        ("u32ReadDisturbCnt", ctypes.c_uint),

        ("u32MapRefreshCnt", ctypes.c_uint),

        ("u32VDETCnt", ctypes.c_uint),

        ("u32GCTotalCnt", ctypes.c_uint),

        ("u32GCWLCnt", ctypes.c_uint),

        ("u32GCClusterCnt", ctypes.c_uint),

        ("u32GCReclaimCnt", ctypes.c_uint),

        ("u32GCUrgentCnt", ctypes.c_uint),

        ("u32GCIdleCnt", ctypes.c_uint),

        ("u16FreeBlkCnt_SLC", ctypes.c_ushort),

        ("u16FreeBlkCnt_NOR", ctypes.c_ushort),

        ("u32ScanBlockCnt", ctypes.c_uint),

        ("u32EmmcTrimCnt", ctypes.c_uint),

        ("u16HelthCMD0Time", ctypes.c_ushort),

        ("u16HelthGCMaxTime", ctypes.c_ushort),

        ("u16HelthApplyTime", ctypes.c_ushort),

        ("u16HelthEraseDiff", ctypes.c_ushort),

        ("u32GcStopMergeCnt", ctypes.c_uint),

        ("u32Rev", ctypes.c_uint * 11)

    ]

__HEALTH_TAG__ = int(0xaa55)
class sOWN_HealthReport(ctypes.Structure):
    _fields_ = [

        ("u32HealthTags", ctypes.c_uint),

        ("u32EventTrackCnt", ctypes.c_uint),

        ("sNoticeIssuse", sOWN_HealthInfo_NOTICES),

        ("sRoot", sOWN_Root),

        ("sNandFeature", sOWN_NandFeature),

        ("sErrorInfo", sOWN_ErrorInfo),

        ("sPE", sBlkPEInfo),

        ("sFTLStatistics", sOWN_HealthInfo_FTL_Statistics),

        ("u08Rsv4", ctypes.c_ubyte * 778),

        ("u16EndTag", ctypes.c_ushort)

    ]


    def smart_info_decode(self):
        """
        Decodes smart information and returns a dictionary containing various statistics.

        :return: A dictionary containing smart information.
        """
        mmc_smart = {"GitCommit": hex(self.sRoot.u32RootFwVer),
                     "POR次数": self.sRoot.u32PORCnt,
                     "Root更换次数": self.sRoot.u32RootExchangeCnt,
                     "FTL标志": hex(self.sFTLStatistics.u32FTL_StaTAG),
                     "原始坏块数": self.sFTLStatistics.u16BadCnt,
                     "WAF": (self.sFTLStatistics.u08WAF_Integer * 100 + self.sFTLStatistics.u08WAF_Decimal) / 100,
                     "重读次数": self.sFTLStatistics.u32RetryCnt,
                     "软解码次数": self.sFTLStatistics.u32SoftDecodeCnt,
                     "ECC错误次数": self.sFTLStatistics.u32EccUncCnt,
                     "Refresh标记次数": self.sFTLStatistics.u32RefreshCnt,
                     "读干扰触发次数": self.sFTLStatistics.u32ReadDisturbCnt,
                     "映射表HECC次数": self.sFTLStatistics.u32MapRefreshCnt,
                     "VDET次数": self.sFTLStatistics.u32VDETCnt,
                     "GC总次数": self.sFTLStatistics.u32GCTotalCnt,
                     "磨损均衡次数": self.sFTLStatistics.u32GCWLCnt,
                     "GCCluster次数": self.sFTLStatistics.u32GCClusterCnt,
                     "GCReclaim次数": self.sFTLStatistics.u32GCReclaimCnt,
                     "GCUrgent次数": self.sFTLStatistics.u32GCUrgentCnt,
                     "GCIdle次数": self.sFTLStatistics.u32GCIdleCnt,
                     "SLC空闲块数量": self.sFTLStatistics.u16FreeBlkCnt_SLC,
                     "TLC空闲块数量": self.sFTLStatistics.u16FreeBlkCnt_NOR,
                     "扫描次数": self.sFTLStatistics.u32ScanBlockCnt,
                     "Trim次数": self.sFTLStatistics.u32EmmcTrimCnt,
                     "CMD0最大耗时": self.sFTLStatistics.u16HelthCMD0Time,
                     "GC最大耗时": self.sFTLStatistics.u16HelthGCMaxTime,
                     "Apply最大耗时": self.sFTLStatistics.u16HelthApplyTime,
                     "PE最大差值": self.sFTLStatistics.u16HelthEraseDiff,
                     "GC意外中止次数": self.sFTLStatistics.u32GcStopMergeCnt}

        return mmc_smart
