export const UserType = {
    ADMIN: 'Admin',
    PLANLAMA: 'Planlama',
    SATIS_PAZARLAMA: 'Satış/Pazarlama',
    KALITE_KONTROL: 'Kalite kontrol',
    DEPO: 'Depo'
};

export const MachineType = {
    PRESS: 'press',
    OVALAMA: 'ovalama',
    KAPLAMA: 'kaplama',
};

export const MachineVariation = {
    CH3: 'CH3',
    CH5: 'CH5',
    CH5S: 'CH5S',
    CH5L: 'CH5L',
    CH6: 'CH6',
    KAPLAMA_TEDARIKCISI: 'Kaplama Tedarikcisi',
};

export const SiparisState = {
    PLANLAMA: 'Planlama',
    IMALAT: 'İmalat',
    SIPARIS_TAMAMLANDI: 'Sipariş Tamamlandı'
};

export const Materials = {
    STEEL_20MnB4: "20MnB4",
    STEEL_15B2: "15B2",
    STEEL_CQ15: "CQ15",
    STEEL_SAE100GC: "SAE100GC",
    STAINLESS_304Cu: "304Cu(Paslanmaz)",
    DIRECT_CEZIM: "Direct Çezim",
    STEEL_23MnB4: "23MnB4"
};

export const QualityTypes = {
    GRADE_48: "4.8",
    GRADE_68: "6.8",
    GRADE_88: "8.8",
    GRADE_108: "10.8",
    CARBONHIDRATION: "Karbonhidrasyon"
};

export const KaplamaTypes = {
    ZINC_PLATING: "Çinko Kaplama",
    ZINC_NICKEL_CLEAR_PLATING: "Çinko Nikel Şeffaf Kaplama",
    NICKEL_PLATING: "Nikel Kaplama",
    ZINC_NICKEL_BLACK_PLATING: "Çinko Nikel Siyah Kaplama",
    ZINC_BLACK_PLATING: "Çinko Siyah Kaplama",
    JANJAN_PLATING: "Janjan Kaplama",
    GEOMET_PLATING: "Geomet Kaplama",
    YELLOW_PLATING: "Sarı Kaplama"
};

export const ProcessState = {
    BASLAMADI: 'Başlamadı',
    CALISIYOR: 'Çalışıyor',
    BEKLEMEDE: 'Beklemede',
    BITTI: 'Bitti',
};

export const ProcessTransitions = {
    'Başlamadı': [ ProcessState.BASLAMADI, ProcessState.CALISIYOR ],
    'Çalışıyor': [ ProcessState.CALISIYOR, ProcessState.BEKLEMEDE, ProcessState.BITTI ],
    'Beklemede': [ ProcessState.BEKLEMEDE, ProcessState.CALISIYOR, ProcessState.BITTI ],
    'Bitti': [ ProcessState.BITTI ],
}