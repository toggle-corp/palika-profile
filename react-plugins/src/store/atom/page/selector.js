import { createSelector } from 'reselect';

const emptyObject = {};
const emptyList = [];
const emptyFaramState = {
    faramValues: {},
    faramErrors: {},
    // pristine: true,
};

const generatorAddPageSelector = ({ page }) => page.generatorAdd || emptyObject;

export const generatorSelectorGP = createSelector(
    generatorAddPageSelector,
    page => page.generator || emptyObject,
);

export const exportStatusSelectorGP = createSelector(
    generatorAddPageSelector,
    page => page.exportStatus,
);

export const exportStateSelectorGP = createSelector(
    generatorAddPageSelector,
    page => page.exportState || emptyObject,
);

export const generatorErrorListSelectorGP = createSelector(
    generatorSelectorGP,
    generator => generator.errors || emptyList,
);

export const generatorGeoMetaSelectorGP = createSelector(
    generatorSelectorGP,
    generator => generator.geoMeta || emptyObject,
);

export const generatorProvinceListSelectorGP = createSelector(
    generatorGeoMetaSelectorGP,
    geoMeta => geoMeta.provinces || emptyList,
);

export const generatorDistrictListSelectorGP = createSelector(
    generatorGeoMetaSelectorGP,
    geoMeta => geoMeta.districts || emptyList,
);

export const generatorPalikaCodeListSelectorGP = createSelector(
    generatorGeoMetaSelectorGP,
    geoMeta => geoMeta.palikaCodes || emptyList,
);

export const exportFaramSelectorGP = createSelector(
    generatorAddPageSelector,
    page => page.generatorExport || emptyFaramState,
);

export const exportDistrictListSelectorGP = createSelector(
    exportFaramSelectorGP,
    generatorDistrictListSelectorGP,
    (
        { faramValues: { selectedProvince } },
        districts,
    ) => {
        if (selectedProvince && selectedProvince.length) {
            return districts.filter(
                district => (
                    selectedProvince.findIndex(
                        provinceId => provinceId === district.province,
                    ) !== -1
                ),
            );
        }
        return districts;
    },
);

export const exportPalikaListSelectorGP = createSelector(
    exportFaramSelectorGP,
    generatorPalikaCodeListSelectorGP,
    (
        { faramValues: { selectedProvince, selectedDistrict } },
        palikaCodes,
    ) => {
        if (selectedDistrict && selectedDistrict.length) {
            return palikaCodes.filter(
                palika => (
                    selectedDistrict.findIndex(
                        districtId => districtId === palika.district,
                    ) !== -1
                ),
            );
        } if (selectedProvince && selectedProvince.length) {
            return palikaCodes.filter(
                palika => (
                    selectedProvince.findIndex(
                        provinceId => provinceId === palika.province,
                    ) !== -1
                ),
            );
        }
        return palikaCodes;
    },
);
