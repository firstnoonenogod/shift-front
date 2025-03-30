export default defineNuxtPlugin(nuxtApp => {
  // Thailand zip code utility
  const thZipCodes = {
    // Example data - this would be expanded in a real application
    "bangkok": ["10100", "10110", "10120", "10130", "10140"],
    "chiang_mai": ["50000", "50100", "50200", "50300"],
    "phuket": ["83000", "83100", "83110", "83120", "83130"]
  };

  const zipCodeUtil = {
    // Get all zip codes for a province
    getZipCodesForProvince(province) {
      return thZipCodes[province.toLowerCase()] || [];
    },
    
    // Check if a zip code is valid for Thailand
    isValidThaiZipCode(zipCode) {
      if (!zipCode || zipCode.length !== 5) return false;
      return /^\d{5}$/.test(zipCode);
    },
    
    // Get province from zip code (simplified implementation)
    getProvinceFromZipCode(zipCode) {
      for (const [province, codes] of Object.entries(thZipCodes)) {
        if (codes.includes(zipCode)) {
          return province;
        }
      }
      return null;
    }
  };

  return {
    provide: {
      zipCode: zipCodeUtil
    }
  };
});
